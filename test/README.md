# Tests

* `ccm-test`: simple test that spins up a multi-node Apache Cassandra cluster withthe `instaclustr-everywhere-strategy`
    JAR installed.
    
* `dse-migrate-test`: e2e test that validates a DSE → Apache Cassandra migration.

## Requirements

These tests rely on [ccm-extensions](https://github.com/zegelin/ccm-extensions) being installed.
This is currently a manual process.