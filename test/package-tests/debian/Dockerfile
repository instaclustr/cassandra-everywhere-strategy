FROM debian:buster

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -qy --no-install-recommends install curl gnupg ca-certificates

RUN echo "deb https://downloads.apache.org/cassandra/debian 311x main" | tee /etc/apt/sources.list.d/cassandra.sources.list && \
    curl https://downloads.apache.org/cassandra/KEYS | apt-key add - && \
    echo "deb https://dl.bintray.com/instaclustr/debian buster extra" | tee /etc/apt/sources.list.d/instaclustr.sources.list && \
    apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 379CE192D401AB61 && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get -qy --no-install-recommends install cassandra instaclustr-everywhere-strategy

