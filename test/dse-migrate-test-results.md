# DSE → Cassandra Migration Test Results

[`dse-migrate-test.py`](dse-migrate-test.py) leverages CCM to perform a test in-place DSE → Cassandra migration.
The Cassandra nodes have the Instaclustr `EverywhereStrategy` installed.

The test is successful if the `sstabledump` outputs are represent the same data.
See [`compare_dumps.py`](compare_dumps.py) for the logic used to compare JSON dumps.

Below is the logging output from a test run.

    ./dse-migrate-test.py --keep-cluster-directory true 3.11.6 5.1.7
    INFO:__main__:Cassandra directory is: /var/folders/3w/vwfv50057mq0z3jx1d7h56240000gn/T/tmpz719h5y2/cassandra/test-cluster
    INFO:__main__:DSE directory is: /var/folders/3w/vwfv50057mq0z3jx1d7h56240000gn/T/tmpz719h5y2/dse/test-cluster
    INFO:__main__:Dump directory is: /var/folders/3w/vwfv50057mq0z3jx1d7h56240000gn/T/tmpz719h5y2/dumps
    INFO:__main__:EverywhereStrategy JAR is: /Users/adam/Projects/everywhere-strategy/target/instaclustr-everywhere-strategy-1.0-SNAPSHOT.jar
    INFO:__main__:Setting up DSE cluster.
    INFO:__main__:Starting DSE cluster.
    INFO:__main__:Applying CQL schema.
    WARNING:cassandra.cluster:Cluster.__init__ called with contact_points specified, but no load_balancing_policy. In the next major version, this will raise an error; please specify a load-balancing policy. (contact_points = [<DefaultEndPoint: 127.0.0.1:9042>, <DefaultEndPoint: 127.0.0.2:9042>, <DefaultEndPoint: 127.0.0.3:9042>], lbp = None)
    DEBUG:cassandra.cluster:Connecting to cluster, contact points: [<DefaultEndPoint: 127.0.0.1:9042>, <DefaultEndPoint: 127.0.0.2:9042>, <DefaultEndPoint: 127.0.0.3:9042>]; protocol version: 66
    DEBUG:cassandra.pool:Host 127.0.0.1:9042 is now marked up
    DEBUG:cassandra.pool:Host 127.0.0.2:9042 is now marked up
    DEBUG:cassandra.pool:Host 127.0.0.3:9042 is now marked up
    DEBUG:cassandra.cluster:[control connection] Opening new connection to 127.0.0.1:9042
    DEBUG:cassandra.connection:Sending initial options message for new connection (4392158672) to 127.0.0.1:9042
    DEBUG:cassandra.io.libevreactor:Starting libev event loop
    DEBUG:cassandra.connection:Defuncting connection (4392158672) to 127.0.0.1:9042: <Error from server: code=000a [Protocol error] message="Invalid or unsupported protocol version (66); supported versions are (3/v3, 4/v4, 5/v5-beta, 65/dse-v1)">
    DEBUG:cassandra.io.libevreactor:Closing connection (4392158672) to 127.0.0.1:9042
    DEBUG:cassandra.io.libevreactor:Closed socket to 127.0.0.1:9042
    WARNING:cassandra.cluster:Downgrading core protocol version from 66 to 65 for 127.0.0.1:9042. To avoid this, it is best practice to explicitly set Cluster(protocol_version) to the version supported by your cluster. http://datastax.github.io/python-driver/api/cassandra/cluster.html#cassandra.cluster.Cluster.protocol_version
    DEBUG:cassandra.io.libevreactor:All Connections currently closed, event loop ended
    DEBUG:cassandra.connection:Sending initial options message for new connection (4392158672) to 127.0.0.1:9042
    DEBUG:cassandra.io.libevreactor:Starting libev event loop
    DEBUG:cassandra.connection:Received options response on new connection (4392158672) from 127.0.0.1:9042
    DEBUG:cassandra.connection:No available compression types supported on both ends. locally supported: odict_keys([]). remotely supported: ['snappy', 'lz4']
    DEBUG:cassandra.connection:Sending StartupMessage on <LibevConnection(4392158672) 127.0.0.1:9042>
    DEBUG:cassandra.connection:Sent StartupMessage on <LibevConnection(4392158672) 127.0.0.1:9042>
    DEBUG:cassandra.connection:Got ReadyMessage on new connection (4392158672) from 127.0.0.1:9042
    DEBUG:cassandra.cluster:[control connection] Established new connection <LibevConnection(4392158672) 127.0.0.1:9042>, registering watchers and refreshing schema and topology
    DEBUG:cassandra.cluster:[control connection] Refreshing node list and token map using preloaded results
    INFO:cassandra.policies:Using datacenter 'dse_dc' for DCAwareRoundRobinPolicy (via host '127.0.0.1:9042'); if incorrect, please specify a local_dc to the constructor, or limit contact points to local cluster nodes
    DEBUG:cassandra.cluster:[control connection] Finished fetching ring info
    DEBUG:cassandra.cluster:[control connection] Rebuilding token map due to topology changes
    DEBUG:cassandra.cluster:Control connection created
    DEBUG:cassandra.pool:Initializing connection for host 127.0.0.1:9042
    DEBUG:cassandra.pool:Initializing connection for host 127.0.0.2:9042
    DEBUG:cassandra.connection:Sending initial options message for new connection (4415256656) to 127.0.0.1:9042
    DEBUG:cassandra.connection:Sending initial options message for new connection (4415255760) to 127.0.0.2:9042
    DEBUG:cassandra.connection:Received options response on new connection (4415256656) from 127.0.0.1:9042
    DEBUG:cassandra.connection:No available compression types supported on both ends. locally supported: odict_keys([]). remotely supported: ['snappy', 'lz4']
    DEBUG:cassandra.connection:Sending StartupMessage on <LibevConnection(4415256656) 127.0.0.1:9042>
    DEBUG:cassandra.connection:Sent StartupMessage on <LibevConnection(4415256656) 127.0.0.1:9042>
    DEBUG:cassandra.connection:Got ReadyMessage on new connection (4415256656) from 127.0.0.1:9042
    DEBUG:cassandra.pool:Finished initializing connection for host 127.0.0.1:9042
    DEBUG:cassandra.cluster:Added pool for host 127.0.0.1:9042 to session
    DEBUG:cassandra.pool:Initializing connection for host 127.0.0.3:9042
    DEBUG:cassandra.cluster:Not starting MonitorReporter thread for Insights; not supported by server version 3.11.1.2130 on ControlConnection host 127.0.0.1:9042
    DEBUG:cassandra.cluster:Started Session with client_id c00bb933-09aa-4b14-8c89-734a6e8d0644 and session_id f85dd57b-f298-49d0-86c6-3c19fa597cb9
    DEBUG:ccm_extensions._ExtendedCluster.<locals>.ExtendedClusterImpl:Executing CQL statement "CREATE KEYSPACE example WITH replication = {'class': 'EverywhereStrategy'};".
    DEBUG:cassandra.connection:Sending initial options message for new connection (4415257488) to 127.0.0.3:9042
    DEBUG:cassandra.connection:Message pushed from server: <EventMessage(event_type='SCHEMA_CHANGE', event_args={'target_type': 'KEYSPACE', 'change_type': 'CREATED', 'keyspace': 'example'}, stream_id=-1, trace_id=None)>
    DEBUG:cassandra.connection:Received options response on new connection (4415255760) from 127.0.0.2:9042
    DEBUG:cassandra.connection:No available compression types supported on both ends. locally supported: odict_keys([]). remotely supported: ['snappy', 'lz4']
    DEBUG:cassandra.connection:Sending StartupMessage on <LibevConnection(4415255760) 127.0.0.2:9042>
    DEBUG:cassandra.connection:Sent StartupMessage on <LibevConnection(4415255760) 127.0.0.2:9042>
    DEBUG:cassandra.connection:Got ReadyMessage on new connection (4415255760) from 127.0.0.2:9042
    DEBUG:cassandra.pool:Finished initializing connection for host 127.0.0.2:9042
    DEBUG:cassandra.cluster:Added pool for host 127.0.0.2:9042 to session
    DEBUG:cassandra.cluster:Refreshing schema in response to schema change. {'target_type': 'KEYSPACE', 'change_type': 'CREATED', 'keyspace': 'example'}
    DEBUG:cassandra.cluster:[control connection] Waiting for schema agreement
    DEBUG:cassandra.cluster:[control connection] Schemas mismatched, trying again
    DEBUG:cassandra.connection:Received options response on new connection (4415257488) from 127.0.0.3:9042
    DEBUG:cassandra.connection:No available compression types supported on both ends. locally supported: odict_keys([]). remotely supported: ['snappy', 'lz4']
    DEBUG:cassandra.connection:Sending StartupMessage on <LibevConnection(4415257488) 127.0.0.3:9042>
    DEBUG:cassandra.connection:Sent StartupMessage on <LibevConnection(4415257488) 127.0.0.3:9042>
    DEBUG:cassandra.connection:Got ReadyMessage on new connection (4415257488) from 127.0.0.3:9042
    DEBUG:cassandra.pool:Finished initializing connection for host 127.0.0.3:9042
    DEBUG:cassandra.cluster:Added pool for host 127.0.0.3:9042 to session
    DEBUG:cassandra.cluster:[control connection] Schemas mismatched, trying again
    DEBUG:cassandra.cluster:[control connection] Schemas mismatched, trying again
    DEBUG:cassandra.cluster:[control connection] Schemas mismatched, trying again
    DEBUG:cassandra.cluster:[control connection] Schemas mismatched, trying again
    DEBUG:cassandra.cluster:[control connection] Schemas mismatched, trying again
    DEBUG:cassandra.cluster:[control connection] Schemas mismatched, trying again
    DEBUG:cassandra.cluster:[control connection] Schemas mismatched, trying again
    DEBUG:cassandra.cluster:[control connection] Schemas match
    DEBUG:ccm_extensions._ExtendedCluster.<locals>.ExtendedClusterImpl:Executing CQL statement "CREATE TABLE example.demo_table (".
    DEBUG:cassandra.connection:Message pushed from server: <EventMessage(event_type='SCHEMA_CHANGE', event_args={'target_type': 'TABLE', 'change_type': 'CREATED', 'keyspace': 'example', 'table': 'demo_table'}, stream_id=-1, trace_id=None)>
    DEBUG:cassandra.cluster:Refreshing schema in response to schema change. {'target_type': 'TABLE', 'change_type': 'CREATED', 'keyspace': 'example', 'table': 'demo_table'}
    DEBUG:cassandra.cluster:[control connection] Waiting for schema agreement
    DEBUG:cassandra.cluster:[control connection] Schemas mismatched, trying again
    DEBUG:cassandra.cluster:[control connection] Schemas mismatched, trying again
    DEBUG:cassandra.cluster:[control connection] Schemas mismatched, trying again
    DEBUG:cassandra.cluster:[control connection] Schemas mismatched, trying again
    DEBUG:cassandra.cluster:[control connection] Schemas mismatched, trying again
    DEBUG:cassandra.cluster:[control connection] Schemas mismatched, trying again
    DEBUG:cassandra.cluster:[control connection] Schemas match
    DEBUG:cassandra.cluster:[control connection] Waiting for schema agreement
    DEBUG:cassandra.cluster:[control connection] Schemas match
    DEBUG:ccm_extensions._ExtendedCluster.<locals>.ExtendedClusterImpl:Executing CQL statement "INSERT INTO example.demo_table (a, b) VALUES ('a', '1')".
    DEBUG:cassandra.cluster:[control connection] Waiting for schema agreement
    DEBUG:cassandra.cluster:[control connection] Schemas match
    DEBUG:ccm_extensions._ExtendedCluster.<locals>.ExtendedClusterImpl:Executing CQL statement "INSERT INTO example.demo_table (a, b) VALUES ('b', '2')".
    DEBUG:ccm_extensions._ExtendedCluster.<locals>.ExtendedClusterImpl:Executing CQL statement "INSERT INTO example.demo_table (a, b) VALUES ('c', '3')".
    DEBUG:ccm_extensions._ExtendedCluster.<locals>.ExtendedClusterImpl:Executing CQL statement "INSERT INTO example.demo_table (a, b) VALUES ('d', '4')".
    DEBUG:cassandra.io.libevreactor:Closing connection (4415256656) to 127.0.0.1:9042
    DEBUG:cassandra.io.libevreactor:Closed socket to 127.0.0.1:9042
    DEBUG:cassandra.io.libevreactor:Closing connection (4415255760) to 127.0.0.2:9042
    DEBUG:cassandra.io.libevreactor:Closed socket to 127.0.0.2:9042
    DEBUG:cassandra.io.libevreactor:Closing connection (4415257488) to 127.0.0.3:9042
    DEBUG:cassandra.io.libevreactor:Closed socket to 127.0.0.3:9042
    DEBUG:cassandra.cluster:Shutting down Cluster Scheduler
    DEBUG:cassandra.cluster:Shutting down control connection
    DEBUG:cassandra.io.libevreactor:Closing connection (4392158672) to 127.0.0.1:9042
    DEBUG:cassandra.io.libevreactor:Closed socket to 127.0.0.1:9042
    INFO:__main__:DSE nodetool status:
    Datacenter: dse_dc
    ==================
    Status=Up/Down
    |/ State=Normal/Leaving/Joining/Moving
    --  Address    Load       Tokens       Owns (effective)  Host ID                               Rack
    UN  127.0.0.1  95.52 KiB  1            100.0%            143e71a4-0445-4748-8588-6aa5de93ec3a  dse_dc-rack-a
    UN  127.0.0.2  123.52 KiB  1            100.0%            7287f599-ea37-4021-b561-9875093b2478  dse_dc-rack-b
    UN  127.0.0.3  123.51 KiB  1            100.0%            051d3202-b353-464d-a299-6ff40ed6721f  dse_dc-rack-c
    
    
    INFO:__main__:Setting up Cassandra cluster.
    INFO:__main__:Starting Cassandra cluster.
    INFO:__main__:Cassandra nodetool status:
    Datacenter: cassandra_dc
    ========================
    Status=Up/Down
    |/ State=Normal/Leaving/Joining/Moving
    --  Address    Load       Tokens       Owns (effective)  Host ID                               Rack
    UN  127.0.1.1  76.83 KiB  256          100.0%            f10efc50-fd97-40dd-a931-98000b006a4d  cassandra_dc-rack-a
    UN  127.0.1.2  119.88 KiB  256          100.0%            49cb4f94-bb58-49e6-85b8-936a7be81ebc  cassandra_dc-rack-b
    UN  127.0.1.3  84.33 KiB  256          100.0%            1f74a004-ea96-400a-aad1-7f49862a4913  cassandra_dc-rack-c
    Datacenter: dse_dc
    ==================
    Status=Up/Down
    |/ State=Normal/Leaving/Joining/Moving
    --  Address    Load       Tokens       Owns (effective)  Host ID                               Rack
    UN  127.0.0.1  105.27 KiB  1            100.0%            143e71a4-0445-4748-8588-6aa5de93ec3a  dse_dc-rack-a
    UN  127.0.0.2  123.52 KiB  1            100.0%            7287f599-ea37-4021-b561-9875093b2478  dse_dc-rack-b
    UN  127.0.0.3  96.92 KiB  1            100.0%            051d3202-b353-464d-a299-6ff40ed6721f  dse_dc-rack-c
    
    
    INFO:compare_dumps:Flushing SSTables
    INFO:compare_dumps:Compacting SSTables
    INFO:compare_dumps:Dumping SSTables
    INFO:compare_dumps:Writing 127.0.0.1 dump to /var/folders/3w/vwfv50057mq0z3jx1d7h56240000gn/T/tmpz719h5y2/dumps/127.0.0.1-0.json
    INFO:compare_dumps:Writing 127.0.0.2 dump to /var/folders/3w/vwfv50057mq0z3jx1d7h56240000gn/T/tmpz719h5y2/dumps/127.0.0.2-0.json
    INFO:compare_dumps:Writing 127.0.0.3 dump to /var/folders/3w/vwfv50057mq0z3jx1d7h56240000gn/T/tmpz719h5y2/dumps/127.0.0.3-0.json
    INFO:compare_dumps:Writing 127.0.1.1 dump to /var/folders/3w/vwfv50057mq0z3jx1d7h56240000gn/T/tmpz719h5y2/dumps/127.0.1.1-0.json
    INFO:compare_dumps:Writing 127.0.1.2 dump to /var/folders/3w/vwfv50057mq0z3jx1d7h56240000gn/T/tmpz719h5y2/dumps/127.0.1.2-0.json
    INFO:compare_dumps:Writing 127.0.1.3 dump to /var/folders/3w/vwfv50057mq0z3jx1d7h56240000gn/T/tmpz719h5y2/dumps/127.0.1.3-0.json
    INFO:compare_dumps:Comparing dumps
    INFO:compare_dumps:Dumps are identical.
    INFO:compare_dumps:Partitions:
    INFO:compare_dumps:	Partition(key=('a',), rows=(Row(cells=(Cell(name='b', value='1'),)),))
    INFO:compare_dumps:	Partition(key=('c',), rows=(Row(cells=(Cell(name='b', value='3'),)),))
    INFO:compare_dumps:	Partition(key=('d',), rows=(Row(cells=(Cell(name='b', value='4'),)),))
    INFO:compare_dumps:	Partition(key=('b',), rows=(Row(cells=(Cell(name='b', value='2'),)),))
    INFO:compare_dumps:... are shared by the following dumps:
    INFO:compare_dumps:	127.0.1.2-0.json
    INFO:compare_dumps:	127.0.0.2-0.json
    INFO:compare_dumps:	127.0.0.3-0.json
    INFO:compare_dumps:	127.0.1.3-0.json
    INFO:compare_dumps:	127.0.0.1-0.json
    INFO:compare_dumps:	127.0.1.1-0.json