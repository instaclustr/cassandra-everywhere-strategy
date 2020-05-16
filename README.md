# Instaclustr Everywhere Strategy

[![Bintray Badge](https://img.shields.io/bintray/v/instaclustr/debian/instaclustr-everywhere-strategy.svg)](https://bintray.com/instaclustr/debian/instaclustr-everywhere-strategy)

An `EverywhereStrategy` implementation for Apache Cassandra.

This is useful for performing DSE Cassandra → Apache Cassandra migrations.

The remainder of this README refers to _DSE Cassandra_ as simply _DSE_, and _Apache Cassandra_ as _Cassandra_.

Simply install the JAR into the classpath on all Cassandra nodes. The JAR contains an implementation of `EverywhereStrategy` that
is compatible with Cassandra.

## Installation

### Cassandra Package Installs

We offer a packaged version of `instaclustr-everywhere-strategy` for systems where Cassandra has been installed via the official Apache.org Debian or RPM package.

This package will automatically install `instaclustr-everywhere-strategy` into an appropriate location for the Cassandra package install
(i.e., `$CASSANDRA_HOME/lib`, which at present is `/usr/share/cassandra/lib`).

_Note_: These packages have a hard dependency for a `cassandra` package.
If Cassandra hasn't been installed via your distributions package manager, installing `instaclustr-everywhere-strategy`
may force the Cassandra package to be installed. This may conflict with a tarball install.
See [Cassandra Tarball Installs](#cassandra-tarball-installs) below on how to install `instaclustr-everywhere-strategy`
for tarball installs of Cassandra.

#### Debian-based Distributions

(Debian, Ubuntu, et al.)

1. Add the `instaclustr/debian` repository.

       echo "deb https://dl.bintray.com/instaclustr/debian stable main" > \
           /etc/apt/sources.list.d/instaclustr.sources.list
    
2. Run `apt-get update` to fetch the contents of the new package repository.

3. Run `apt-get install instaclustr-everywhere-stratgey` to install the package.

#### RPM-based Distributions

(RHEL, Fedora, CentOS, et al.)

1. Add the `instaclustr/rpm` repository.

       wget -O - https://bintray.com/instaclustr/rpm/rpm | \
           sudo tee /etc/yum.repos.d/instaclustr.repo

2. Run `dnf install instaclustr-everywhere-strategy` to install the package.

    Hint: For YUM-based distributions the command is `yum install instaclustr-everywhere-strategy`.

### Cassandra Tarball Installs

1. Download the latest `instaclustr-everywhere-strategy` JAR from the [releases](https://github.com/instaclustr/everywhere-strategy/releases) page.

2. Install the `instaclustr-everywhere-strategy` JAR into the Cassandra classpath.

    Typically the best location is `$CASSANDRA_HOME/lib`.

3. Restart Cassandra.

## Testing

Some automated tests leveraging [Cassandra Cluster Manager](https://github.com/riptano/ccm) (CCM) exist in the
[`tests/`](tests/) directory.

The basic gist of testing is as follows:

1. Create a new keyspace using `EverywhereStrategy`:

       CREATE KEYSPACE example USING replication = {'class': 'EverywhereStrategy'};

    The strategy is installed correctly if the keyspace is created successfully.

1. Create a table under the new keyspace, and insert some data:

       CREATE TABLE example.demo (a text PRIMARY KEY);
       INSERT INTO example.demo (a) VALUES ('a');
       INSERT INTO example.demo (a) VALUES ('b');
       INSERT INTO example.demo (a) VALUES ('c');
       INSERT INTO example.demo (a) VALUES ('d');

    The strategy is functioning correctly if the data is replicated to all nodes.
    
1. Run `nodetool flush` on every node.

1. Run `nodetool compact` on every node.

1. Run `sstabledump` on the table SSTables from each node.

1. Compare the JSON output from each node and confirm that the data in each dump is identical.

See [DSE → Cassandra Migration Test Results](test/dse-migrate-test-results.md) for the results of running the
DSE → Cassandra end-to-end tests.


## Motivation

DSE uses an internal `EverywhereStrategy` implementation for various `dse_*` keyspaces.
When joining a Cassandra node to a DSE cluster these keyspaces will cause `ClassNotFound` exceptions to be thrown on the Cassandra node.
These exceptions result in a schema disagreement. <!-- and what else? -->

In the `system.log` for a Cassandra node:

    ERROR [InternalResponseStage:1] MigrationTask.java:95 - Configuration exception merging remote schema
    org.apache.cassandra.exceptions.ConfigurationException: Unable to find replication strategy class 'org.apache.cassandra.locator.EverywhereStrategy'
        <stacktrace snipped>

and `nodetool describecluster`:

    Cluster Information:
    	Name: test-cluster
    	Snitch: org.apache.cassandra.locator.GossipingPropertyFileSnitch
    	DynamicEndPointSnitch: enabled
    	Partitioner: org.apache.cassandra.dht.Murmur3Partitioner
    	Schema versions:
    		850859e7-fcca-3516-9d8c-e9a9a205c974: [127.0.0.1, 127.0.0.2, 127.0.0.3]
    
    		e84b6a60-24cf-30ca-9b58-452d92911703: [127.0.1.1, 127.0.1.2, 127.0.1.3]
    		
In the output above, IPs `127.0.0.*` are DSE nodes, `127.0.1.*` are Cassandra nodes.

One common solution is to `ALTER` the `dse_*` keyspaces to use `NetworkTopologyStrategy` before joining Cassandra nodes to the cluster.
While this works, it's also dangerous.
DSE nodes reset the replication strategy back to `EverywhereStrategy` on startup.
As a result, if any DSE nodes restart while Cassandra nodes are present the cluster, then schema disagreement will again occur. 


## Implementation

Our `EverywhereStartegy` implementation extends `NetworkTopologyStrategy`.
This is required because various core components inside Cassandra
(e.g., [`ConsistencyLevel`](https://github.com/apache/cassandra/blob/trunk/src/java/org/apache/cassandra/db/ConsistencyLevel.java))
perform `instanceof NetworkTopologyStrategy` checks when they need to be datacenter aware.

Yet, `NetworkTopologyStrategy` hasn't been designed to be extendable.
A number of its fields are private final immutable, including `datacenters`, which is the DC→RF mapping.
So we resort to reflection to fix this. Yuck. But, it works…


## Version Compatibility

| Cassandra Version | Status |
| --- | --- |
| 3.11.x | Compatible |
| 4.x | _Untested_ |
| 3.0.x | _Untested_ |
| 2.2.x | _Untested_ |
| 2.1.x | _Untested_ |
| 2.0.x | Unsupported |



## License

This project is licensed under the Apache License, version 2.0. See [LICENSE](LICENSE) for details.

## Instaclustr Support

Please see our [Open Source Project Status](https://www.instaclustr.com/support/documentation/announcements/instaclustr-open-source-project-status/) page for details on Instaclustr's support status of this project.
