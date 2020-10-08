package org.apache.cassandra.locator;

import java.lang.reflect.Field;
import java.net.InetAddress;
import java.util.HashMap;
import java.util.List;
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

    protected final Map<String, Integer> datacenters;
    protected final IEndpointSnitch snitch;

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
        final Field datacentersField = NetworkTopologyStrategy.class.getDeclaredField("datacenters");
        datacentersField.setAccessible(true);
        this.datacenters = new HashMap<>();
        datacentersField.set(this, this.datacenters);

        // snitch is private in NTS 3.0

        final Field snitchField = NetworkTopologyStrategy.class.getDeclaredField("snitch");
        snitchField.setAccessible(true);
        this.snitch = snitch;
        snitchField.set(this, this.snitch);
    }

    // this gets called whenever the ring topology changes.
    // redetermine the RF for each DC.
    public List<InetAddress> calculateNaturalEndpoints(final Token token, final TokenMetadata tokenMetadata) {
        final Set<InetAddress> endpoints = tokenMetadata.getAllEndpoints();

        final Map<String, Integer> previousDataCenters = ImmutableMap.copyOf(this.datacenters);

        this.datacenters.clear();

        for (final InetAddress endpoint : endpoints) {
            final String datacenter = this.snitch.getDatacenter(endpoint);
            this.datacenters.merge(datacenter, 1, Integer::sum);
        }

        if (!previousDataCenters.equals(this.datacenters)) {
            logger.info("Data center replication factors for keyspace '{}' = {}", this.keyspaceName, this.datacenters);
        }

        return super.calculateNaturalEndpoints(token, tokenMetadata);
    }
}
