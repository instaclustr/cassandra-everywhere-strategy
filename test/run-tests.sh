#!/bin/bash

# ssltabledump not available on 2.2.x
#python3 ccm-test.py -j ../cassandra-2.2/target/everywhere-strategy-cassandra-2.2-1.0.0.jar 2.2.18
python3 ccm-test.py -j ../cassandra-3.0/target/everywhere-strategy-cassandra-3.0-1.0.0.jar 3.0.26
python3 ccm-test.py -j ../cassandra-3.11/target/everywhere-strategy-cassandra-3.11-1.0.0.jar 3.11.14
python3 ccm-test.py -j ../cassandra-4/target/everywhere-strategy-cassandra-4.0-1.0.0.jar 4.0.7
python3 ccm-test.py -j ../cassandra-4.1/target/everywhere-strategy-cassandra-4.1-1.0.0.jar 4.1.0