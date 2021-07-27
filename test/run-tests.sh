#!/bin/bash

ip link add name loop1 type dummy
ip link set loop1 up
ip addr add 127.0.0.2/8 dev loop1

# ssltabledump not available on 2.2.x
#python3 ccm-test.py -j ../cassandra-2.2/target/everywhere-strategy-cassandra-2.2-1.0.0.jar 2.2.18
# circleci machine is running with Java 11 and 3.0 nor 3.11 is not compatible with that
#python3 ccm-test.py -j ../cassandra-3.0/target/everywhere-strategy-cassandra-3.0-1.0.0.jar 3.0.24
#python3 ccm-test.py -j ../cassandra-3.11/target/everywhere-strategy-cassandra-3.11-1.0.0.jar 3.11.10
python3 ccm-test.py -j ../cassandra-4/target/everywhere-strategy-cassandra-4.0-1.0.0.jar 4.0.0