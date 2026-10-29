# Lite FullNode

For any user who wants to achieve the highest level of security and autonomy on the TRON network, running a FullNode is undoubtedly the best choice. This means the user holds a complete, continuously synchronized copy of the TRON ledger to independently validate every transaction and block. It also grants direct network access and the ability to query all historical data without relying on third-party services.

However, synchronizing a FullNode from the genesis block takes time, and storing the complete blockchain history requires substantial disk space. A Lite FullNode offers an alternative: it starts from a snapshot, saving initial synchronization time and reducing initial disk space requirements.

## What is a Lite FullNode

Lite FullNodes run the same code as FullNodes, but start from a snapshot with limited historical data for faster initial synchronization and lower initial disk usage.

## Core Features

- **Starts from a State Data Snapshot**: A Lite FullNode does not sync from the genesis block. Instead, it loads a snapshot containing the latest network state, the genesis block, and the most recent 65,536 blocks. This block count is a fixed constant in the source code and cannot be changed via configuration. The value 65,536 (= 2^16) matches TRON's transaction reference-block window: every transaction's `ref_block_hash` must point to a block within the most recent 65,536 blocks, otherwise the transaction will fail the Tapos verification. A Lite FullNode therefore must retain at least this many recent blocks to validate incoming transactions.
- **Faster Initial Synchronization and Lower Initial Disk Usage**: Starting from a snapshot saves time compared with synchronizing from the genesis block. The snapshot also requires less disk space than a FullNode database containing the complete blockchain history.
- **Provides a Subset of FullNode APIs**: By default, a Lite FullNode disables a predefined set of APIs, even when the requested data is available locally. For the list of APIs disabled by default, please refer to [HTTP](https://github.com/tronprotocol/java-tron/blob/master/framework/src/main/java/org/tron/core/services/filter/LiteFnQueryHttpFilter.java) and [gRPC](https://github.com/tronprotocol/java-tron/blob/master/framework/src/main/java/org/tron/core/services/filter/LiteFnQueryGrpcInterceptor.java).
- **Extendable Functionality**: These APIs can be enabled by setting `node.openHistoryQueryWhenLiteFN = true` in the configuration file. Because a Lite FullNode stores data identically to a standard FullNode after startup, enabling this option re-opens all filtered APIs. However, historical data prior to the snapshot's start height remains unavailable, except for the genesis block.

Therefore, if developers only need to use a node for block synchronization, transaction processing and broadcasting, a Lite FullNode is a better choice.

## Lite FullNode Deployment

The deployment steps, configuration files, and startup commands for a Lite FullNode are identical to those of a standard FullNode. Please refer to the [Deployment Guide](installing_javatron.md) to deploy a Lite FullNode. The only difference is the database. You have two ways to obtain the required Lite FullNode database:

- Download the Lite FullNode data snapshot from the [Public Backup Data](backup_restore.md/#lite-fullnode-data-snapshots) and use it directly.
- Use the [Lite FullNode Pruning Tool](toolkit.md/#lite-fullnode-data-pruning) to convert a FullNode's database into a Lite FullNode's database.

When creating your own snapshot, the pruning tool keeps the `balance-trace` and `account-trace` databases by default. If historical balance queries are not required, you can use `--exclude-historical-balance` with `split -t snapshot` to reduce the snapshot size. This exclusion cannot be reversed by merging a history dataset; do not enable it if the resulting Lite FullNode must support historical balance queries. See [Lite FullNode Data Pruning](toolkit.md/#lite-fullnode-data-pruning) for the command and complete warning.

## Lite FullNode Maintenance

Although a Lite FullNode starts with a minimal data footprint, it continuously syncs and saves new block data during operation. Consequently, its data expansion rate matches that of a standard FullNode, and its disk usage will grow over time.

To manage disk space, you can periodically use the [Lite FullNode Pruning Tool](toolkit.md/#lite-fullnode-data-pruning) to generate a new snapshot from the node's current database, retaining the latest network state, the genesis block, and the most recent 65,536 blocks. The historical balance databases are retained as described above.
