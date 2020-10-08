import argparse
import contextlib
import logging
import tempfile
from pathlib import Path

from ccm_extensions import ExtendedCluster, CqlSchema

from compare_dumps import flush_dump_compare
from utils import default_jar_path, add_strategy_jar

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def cluster_directory(path):
    path = Path(path)

    if path.exists():
        if not path.is_dir():
            raise argparse.ArgumentTypeError(f'"{path}" must be a directory.')

        if next(path.iterdir(), None) is not None:
            raise argparse.ArgumentTypeError(f'"{path}" must be an empty directory.')

    return path


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('cassandra_version', type=str, help="version of Cassandra to run", metavar="CASSANDRA_VERSION")

    parser.add_argument('--cluster-directory', type=cluster_directory, help="location to install Cassandra. Must be empty or not exist. (default is a temporary directory)")
    parser.add_argument('--keep-cluster-directory', type=bool, help="don't delete the cluster directory on exit")
    parser.add_argument('--keep-cluster-running', type=bool, help="don't stop the cluster on exit (implies --keep-cluster-directory)")

    parser.add_argument('-s', '--schema', type=CqlSchema.ArgType, help="CQL schema to apply (default: %(default)s)", default=str(CqlSchema.default_schema_path()))
    parser.add_argument('-j', '--strategy-jar', type=Path, help="location of the everywhere-strategy jar (default: %(default)s)", default=str(default_jar_path()))

    args = parser.parse_args()

    if args.cluster_directory is None:
        args.cluster_directory = Path(tempfile.mkdtemp()) / "test-cluster"
        logger.info('Cluster directory is: %s', args.cluster_directory)

    dump_dir = args.cluster_directory / "dumps"
    logger.info('Dump directory is: %s', dump_dir)

    logger.info('EverywhereStrategy JAR is: %s', args.strategy_jar)

    with contextlib.ExitStack() as defer:
        logger.info('Setting up Cassandra cluster.')

        ccm_cluster = ExtendedCluster(
            cluster_directory=args.cluster_directory,
            cassandra_version=args.cassandra_version,
            # topology={"dc1": {"dc1-rack-a": 1, "dc1-rack-b": 1, "dc1-rack-c": 1}, "dc2": {"dc2-rack-a": 1, "dc2-rack-b": 1, "dc2-rack-c": 1}},
            topology={"dc1": {"dc1-rack-a": 1, "dc1-rack-b": 1}},
            delete_cluster_on_stop=not args.keep_cluster_directory,
        )

        if not args.keep_cluster_running:
            defer.push(ccm_cluster)

        add_strategy_jar(args.cluster_directory, args.strategy_jar)

        # node = ccm_cluster.nodelist()[0]
        #
        # launch_bin = node.get_launch_bin()
        # args = [launch_bin, '-f']
        # env = node.get_env()
        #
        # extension.append_to_server_env(node, env)
        #
        # os.execve(launch_bin, args, env)

        logger.info('Starting cluster.')
        ccm_cluster.start()

        logger.info('Applying CQL schema.')
        ccm_cluster.apply_schema(args.schema)

        node = ccm_cluster.nodelist()[0]

        print(node.nodetool('status -- example').stdout)

        flush_dump_compare(ccm_cluster.nodelist(), dump_dir)
