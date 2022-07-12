package org.apache.cassandra.locator;

import java.lang.reflect.Field;
import java.util.Collection;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;

import com.google.common.collect.ImmutableMap;
import org.apache.cassandra.dht.Token;
import org.apache.cassandra.exceptions.ConfigurationException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/*
    The strategy should be DC-aware, but DC-awareness is hardcoded to NTS throughout Cassandra.
    (see for example org.apache.cassandra.db.ConsistencyLevel)
    Hence why this implementation subclasses NTS.
 */
public class EverywhereStrategy extends NetworkTopologyStrategy {

    private static final Logger logger = LoggerFactory.getLogger(EverywhereStrategy.class);

    protected final Map<String, ReplicationFactor> datacenters;

    public EverywhereStrategy(final String keyspaceName,
                              final TokenMetadata tokenMetadata,
                              final IEndpointSnitch snitch,
                              final Map<String, String> configOptions) throws NoSuchFieldException, IllegalAccessException {
        super(keyspaceName, tokenMetadata, snitch, null);

        if (configOptions != null && configOptions.size() != 0) {
            throw new ConfigurationException("EverywhereStrategy doesn't accept any options.");
        }

        // yuck. but then again, why is this field private?
        // also, sucks that its final *and* and an unmodifiable collection.
        // lets fix that...
        final Field field = NetworkTopologyStrategy.class.getDeclaredField("datacenters");
        field.setAccessible(true);

        this.datacenters = new HashMap<>();

        field.set(this, this.datacenters);
    }

    // this gets called whenever the ring topology changes.
    // redetermine the RF for each DC.
    @Override
    public EndpointsForRange calculateNaturalReplicas(Token searchToken, TokenMetadata tokenMetadata) {
        final Set<InetAddressAndPort> endpoints = tokenMetadata.getAllEndpoints();

        final Map<String, ReplicationFactor> previousDataCenters = ImmutableMap.copyOf(this.datacenters);

        this.datacenters.clear();

        for (final InetAddressAndPort endpoint : endpoints) {
            if (!tokenMetadata.isMember(endpoint))
                continue;

            final String datacenter = this.snitch.getDatacenter(endpoint);
            this.datacenters.merge(datacenter, ReplicationFactor.fromString("1"), (rf1, rf2) -> ReplicationFactor.fullOnly(rf1.fullReplicas + rf2.fullReplicas));
        }

        if (!previousDataCenters.equals(this.datacenters)) {
            logger.info("Data center replication factors for keyspace '{}' = {}", this.keyspaceName, this.datacenters);
        }

        return super.calculateNaturalReplicas(searchToken, tokenMetadata);
    }

    @Override
    public Collection<String> recognizedOptions() {
        return Collections.emptyList();
    }

    @Override
    public void validateOptions() throws ConfigurationException {
        super.validateOptions();
    }

    @Override
    protected void validateExpectedOptions() throws ConfigurationException {
        // do nothing, we are not excepting any options and method in super would throw as we have not provided any
    }
}
