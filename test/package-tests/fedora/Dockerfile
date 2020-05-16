FROM fedora:31

RUN dnf -y install wget

COPY cassandra.repo /etc/yum.repos.d/

RUN wget -O - https://bintray.com/instaclustr/rpm/rpm | tee /etc/yum.repos.d/instaclustr.repo && \
    dnf -y install cassandra instaclustr-everywhere-strategy

