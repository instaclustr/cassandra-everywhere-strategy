# this e2e test:
# - spins up a multi-node DSE cluster
# - applies a simple schema: a single keyspace with EverywhereStrategy and inserts some data into a table (see schema.yaml)
# - spins up a multi-node Cassandra cluster as a 2nd DC to the DSE cluster
# - runs nodetool rebuild
# - flushes SSTables to disk
# - forces a major compaction
# - dumps all SSTables from all nodes to JSON
# - compares JSON contents (set comparison)

import argparse
import contextlib
import logging
import os
import tempfile
from pathlib import Path

from ccm_extensions import ExtendedCluster, CqlSchema, ExtendedDseCluster

from compare_dumps import flush_dump_compare
from utils import default_jar_path, add_strategy_jar

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)



def nodetool_status(cluster):
    node = cluster.nodelist()[0]
    return node.nodetool('status -- example').stdout


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('cassandra_version', type=str, help="version of Cassandra to run", metavar="CASSANDRA_VERSION")
    parser.add_argument('dse_version', type=str, help="version of DSE Cassandra to run", metavar="DSE_VERSION")

    parser.add_argument('--keep-cluster-directory', type=bool, help="don't delete the cluster directory on exit")
    parser.add_argument('--keep-cluster-running', type=bool, help="don't stop the cluster on exit (implies --keep-cluster-directory)")

    parser.add_argument('-s', '--schema', type=CqlSchema.ArgType, help="CQL schema to apply (default: %(default)s)", default=str(CqlSchema.default_schema_path()))
    parser.add_argument('-j', '--strategy-jar', type=Path, help="location of the everywhere-strategy jar (default: %(default)s)", default=str(default_jar_path()))

    args = parser.parse_args()

    cluster_name = 'test-cluster'

    base_dir = Path(tempfile.mkdtemp())

    cassandra_directory = base_dir / 'cassandra' / cluster_name
    dse_directory = base_dir / 'dse' / cluster_name
    dump_dir = base_dir / 'dumps'
    logger.info('Cassandra directory is: %s', cassandra_directory)
    logger.info('DSE directory is: %s', dse_directory)
    logger.info('Dump directory is: %s', dump_dir)

    os.makedirs(cassandra_directory)
    os.makedirs(dse_directory)
    os.makedirs(dump_dir)

    logger.info('EverywhereStrategy JAR is: %s', args.strategy_jar)

    with contextlib.ExitStack() as defer:
        logger.info('Setting up DSE cluster.')
        dse_cluster = ExtendedDseCluster(
            cluster_directory=dse_directory,
            cassandra_version=args.dse_version,
            topology={"dse_dc": {"dse_dc-rack-a": 1, "dse_dc-rack-b": 1, "dse_dc-rack-c": 1}},
            delete_cluster_on_stop=not args.keep_cluster_directory
        )

        if not args.keep_cluster_running:
            defer.push(dse_cluster)

        # needed for DSE 6.8
        # for node in dse_cluster.nodelist():
        #     node.set_configuration_options({'metadata_directory': node.get_path()})

        logger.info('Starting DSE cluster.')
        dse_cluster.start()

        logger.info('Applying CQL schema.')
        dse_cluster.apply_schema(args.schema)

        logger.info('DSE nodetool status:\n' + nodetool_status(dse_cluster))

        logger.info('Setting up Cassandra cluster.')

        class CassandraCluster(ExtendedCluster):
            def create_node(self, jmx_port, remote_debug_port, *args, **kwargs):
                return super().create_node(*args,
                                    jmx_port=str(int(jmx_port)+1000),  # why is this a string??? why?!?
                                    remote_debug_port='0' if remote_debug_port == '0' else str(int(remote_debug_port)+1000),  # why is this a string??? why?!?
                                    **kwargs)

            def get_seeds(self):
                return [n.network_interfaces['storage'][0] for n in dse_cluster.nodelist()]

        cassandra_cluster = CassandraCluster(
            cluster_directory=cassandra_directory,
            cassandra_version=args.cassandra_version,
            topology={"cassandra_dc": {"cassandra_dc-rack-a": 1, "cassandra_dc-rack-b": 1, "cassandra_dc-rack-c": 1}},
            # topology={"cassandra_dc": {"cassandra_dc-rack-a": 1}},
            ipformat='127.0.1.%d',
            delete_cluster_on_stop=not args.keep_cluster_directory
        )

        if not args.keep_cluster_running:
            defer.push(cassandra_cluster)

        add_strategy_jar(cassandra_directory, args.strategy_jar)

        logger.info('Starting Cassandra cluster.')
        cassandra_cluster.start()

        for node in cassandra_cluster.nodelist():
            node.nodetool('rebuild --keyspace example -- dse_dc')

        logger.info('Cassandra nodetool status:\n' + nodetool_status(cassandra_cluster))

        flush_dump_compare(dse_cluster.nodelist() + cassandra_cluster.nodelist(), dump_dir)
