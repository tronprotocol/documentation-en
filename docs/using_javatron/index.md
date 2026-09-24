# Operate a java-tron node

Guides for java-tron deployment, configuration, connectivity, logging, monitoring, storage, backup, and maintenance.

## First deployment

For a new node, start with these pages:

1. [Deploy a java-tron node](installing_javatron.md) — Hardware and JDK requirements, client acquisition, and startup options for FullNode, SolidityNode, and block-producing nodes.
2. [Configure the node](configuration.md) — Configuration precedence, networks and peers, storage, API services, TVM execution settings, rate limits, block-production credentials, event and monitoring settings, reload behavior, and validation.
3. [Check node logs](logging.md) — Locate and follow node and garbage-collection logs, customize Logback or stdout output when needed, and adjust log levels for troubleshooting.

## Optional deployment scenarios

| Topic | Guide | Covered content |
|---|---|---|
| Lite FullNode | [Lite FullNode](litefullnode.md) | Lite FullNode concepts, state-snapshot startup, reduced storage, API limitations, deployment, and pruning |
| Private network | [Private network](private_network.md) | Prerequisites and deployment steps for a basic private network with one block-producing Super Representative node and one regular FullNode |

## Additional configuration

- [Connect to the TRON network](connecting_to_tron.md) — Network and genesis settings, discovery, active and passive peers, connection limits, status verification, troubleshooting, and private-network connectivity.
- [Database configuration](../architecture/database.md) — Storage-engine support by CPU architecture, RocksDB configuration and optimization, and LevelDB-to-RocksDB migration on x86_64.
- [Event subscription](../architecture/event.md) — Local event subscription through Kafka or MongoDB plugins, supported event types and filters, the event query service, and built-in ZeroMQ subscription.
- [Set up node metrics monitoring](metrics.md) — Enabling java-tron metrics and deploying Prometheus and Grafana.

## Maintenance and recovery

- [Backup and restore](backup_restore.md) — Stopping and archiving a node data directory, restoring a backup, and using public Mainnet or Nile data snapshots.
- [Node maintenance toolkit](toolkit.md) — Keystore management, database partitioning, Lite FullNode pruning, fast copying, LevelDB-to-RocksDB conversion, LevelDB startup optimization, and Merkle-root computation.
