# Lite FullNode

For any user who wants to achieve the highest level of security and autonomy on the TRON network, running a FullNode is undoubtedly the best choice. This means the user holds a complete, continuously synchronized copy of the TRON ledger to independently validate every transaction and block. It also grants direct network access and the ability to query all historical data without relying on third-party services.

However, running a FullNode requires high memory, terabytes of storage, and significant CPU resources, making it impractical for everyone. To allow more people to participate in the TRON ecosystem, TRON offers a more flexible solution. This solution offers a strategic trade-off: it forgoes the local storage of complete historical data in exchange for a significant optimization in hardware resources, enabling the node to run smoothly on lower-spec devices. In TRON's technical ecosystem, this type of node, designed for efficiency and accessibility, is what we call a Lite FullNode.

## What is a Lite FullNode

Lite FullNodes run the exact same code as FullNodes, but they are designed with the primary goal of rapid deployment and low resource consumption.

## Core Features

- **Starts from a State Data Snapshot**: A Lite FullNode does not sync from the genesis block. Instead, it directly loads a state data snapshot that contains only the latest state of the entire network and the historical data of the most recent 65,536 blocks. This block count is a fixed constant in the source code and cannot be changed via configuration. The value 65,536 (= 2^16) matches TRON's transaction reference-block window: every transaction's `ref_block_hash` must point to a block within the most recent 65,536 blocks, otherwise the transaction will fail the Tapos verification. A Lite FullNode therefore must retain at least this many recent blocks to validate incoming transactions.
- **Significant Resource Advantages**: Because the initial data size is far smaller than that of a FullNode, Lite FullNodes have the distinct advantages of occupying less disk space and faster startup times.
- **Provides a Subset of FullNode APIs**: By default, to save resources, a Lite FullNode disables historical data queries (for data outside the snapshot's range). For the list of unsupported APIs, please refer to [HTTP](https://github.com/tronprotocol/java-tron/blob/master/framework/src/main/java/org/tron/core/services/filter/LiteFnQueryHttpFilter.java) and [gRPC](https://github.com/tronprotocol/java-tron/blob/master/framework/src/main/java/org/tron/core/services/filter/LiteFnQueryGrpcInterceptor.java).
- **Extendable Functionality**: These unsupported APIs can be enabled by setting `openHistoryQueryWhenLiteFN = true` in the configuration file. Because a Lite FullNode stores data identically to a standard FullNode after startup, enabling this option re-opens all filtered APIs. However, historical data prior to the snapshot's start height remains unavailable.

Therefore, if developers only need to use a node for block synchronization, processing, and broadcasting transactions, a Lite FullNode is a better choice.

## Lite FullNode Deployment

The deployment steps, configuration files, and startup commands for a Lite FullNode are identical to those of a standard FullNode. Please refer to the [Deployment Guide](installing_javatron.md) to deploy a Lite FullNode. The only difference is the database. You have two ways to obtain the required Lite FullNode database:

- Download the Lite FullNode data snapshot from the [Public Backup Data](backup_restore.md/#lite-fullnode-data-snapshots) and use it directly.
- Use the [Lite FullNode Pruning Tool](toolkit.md/#lite-fullnode-data-pruning) to convert a FullNode's database into a Lite FullNode's database.

When creating your own snapshot, the pruning tool keeps the `balance-trace` and `account-trace` databases by default. If historical balance queries are not required, you can use `--exclude-historical-balance` with `split -t snapshot` to reduce the snapshot size. This exclusion cannot be reversed by merging a history dataset; do not enable it if the resulting Lite FullNode must support historical balance queries. See [Lite FullNode Data Pruning](toolkit.md/#lite-fullnode-data-pruning) for the command and complete warning.

## Lite FullNode Maintenance

Although a Lite FullNode starts with a minimal data footprint, it continuously syncs and saves new block data during operation. Consequently, its data expansion rate matches that of a standard FullNode, and its disk usage will grow over time.

To manage disk space, you can perform periodic maintenance (pruning) on the Lite FullNode's data. This maintenance is also done using the [Lite FullNode Pruning Tool](toolkit.md/#lite-fullnode-data-pruning), which re-prunes the current node data into a new snapshot dataset containing only the latest state.
