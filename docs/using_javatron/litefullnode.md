# Lite Fullnode

For any user who wants to achieve the highest level of security and autonomy on the TRON network, running a Fullnode is undoubtedly the best choice. This means the user holds a complete, continuously synchronized copy of the TRON ledger to independently validate every transaction and block. It also grants direct network access and the ability to query all historical data without relying on third-party services.

However, running a Fullnode requires high memory, terabytes of storage, and significant CPU resources, making it impractical for everyone. To allow more people to participate in the TRON ecosystem, TRON offers a more flexible solution. This solution offers a strategic trade-off: it forgoes the local storage of complete historical data in exchange for a significant optimization in hardware resources, enabling the node to run smoothly on lower-spec devices. In TRON's technical ecosystem, this type of node, designed for efficiency and accessibility, is what we call a Lite Fullnode.

## What is a Lite Fullnode
Lite Fullnodes run the exact same code as Fullnodes, but they are designed with the primary goal of rapid deployment and low resource consumption.

## Core Features
  - **Starts from a State Data Snapshot**: A Lite Fullnode does not sync from the genesis block. Instead, it directly loads a "state data snapshot" that contains only the state of all network accounts and the historical data of the most recent ~65,536 blocks.
 - **Significant Resource Advantages**: Due to the minimal initial data size (about 3% of a Fullnode's data), Lite Fullnodes have the distinct advantages of occupying less disk space and faster startup times.
 - **Provides a Subset of Fullnode APIs**: By default, to save resources, a Lite Fullnode support historical data queries (for data outside the snapshot's range). For a list of unsupported APIs, please refer to HTTP and GRPC.
 - **Extendable Functionality**: These unsupported APIs can be enabled by setting openHistoryQueryWhenLiteFN = true in the configuration file. Because a Lite FullNode saves data exactly like a standard FullNode after startup, enabling this option restores full API functionality for newly synced blocks. However, it will still be unable to query historical data prior to the node's initial startup snapshot.

Therefore, if developers only need to use a node for block synchronization, processing, and broadcasting transactions, a Lite Fullnode is a better choice.

## Lite Fullnode Deployment
The deployment steps, configuration files, and startup commands for a Lite Fullnode are identical to those of a standard FullNode. Please refer to the [Deployment Guide](installing_javatron.md) to deploy a Lite Fullnode. The only difference is the database. You have two ways to obtain the required Lite Fullnode database:

 - Download the Lite Fullnode data snapshot from the [Public Backup Data](backup_restore.md/#lite-fullnode-data-snapshots) and use it directly.
 - Use the [Lite Fullnode Pruning Tool](toolkit.md/#lite-fullnode-data-pruning) to convert a Fullnode's database into a Lite Fullnode's database.


## Lite Fullnode Maintenance
Although a Lite FullNode starts with a minimal data footprint, it continuously syncs and saves new block data during operation. Consequently, its data expansion rate matches that of a standard FullNode, and its disk usage will grow over time.

To manage disk space, you can perform periodic maintenance (pruning) on the Lite Fullnode's data. This maintenance is also done using the Lite Fullnode Pruning Tool, which re-prunes the current node data into a new snapshot dataset containing only the latest state.
