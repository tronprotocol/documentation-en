# Lite Fullnode

For any user who wants to achieve the highest level of security and autonomy on the TRON network, running a Fullnode is undoubtedly the best choice. This not only means the user will hold a complete and continuously synchronized copy of the TRON ledger, able to independently validate every transaction and block, but it also grants them direct access to the entire network and the ability to query all historical data, free from reliance on any third-party services.

However, running a Fullnode requires high memory, terabytes of storage, and significant CPU resources, making it impractical for everyone. To allow more people to participate in the TRON ecosystem, TRON offers a more flexible solution. This solution makes a clever trade-off: it forgoes the local storage of complete historical data in exchange for a significant optimization in hardware resources, enabling the node to run smoothly on lower-spec devices. In TRON's technical ecosystem, this type of node, designed for efficiency and accessibility, is what we call a Lite Fullnode.

## What is a Lite Fullnode
Lite Fullnodes run the exact same code as Fullnodes, but they are designed with the primary goal of rapid deployment and low resource consumption.

## Core Features
  - **Starts from a State Data Snapshot**: A Lite Fullnode does not sync from the genesis block. Instead, it directly loads a "state data snapshot" that contains only the state of all network accounts and the historical data of the most recent ~65,536 blocks.
 - **Significant Resource Advantages**: Due to the minimal initial data size (about 3% of a Fullnode's data), Lite Fullnodes have the distinct advantages of occupying less disk space and starting up fast.
 - **Provides a Subset of Fullnode APIs**: By default, to save resources, a Lite Fullnode does not provide historical data query (for data outside the snapshot's range). For a list of unsupported APIs, please refer to HTTP and GRPC.
 - **Extendable Functionality**: These unsupported APIs can be enabled by setting openHistoryQueryWhenLiteFN = true in the configuration file. Since a Lite Fullnode saves data in the same way as a Fullnode after startup, once this option is enabled, the Lite Fullnode will offer the same functionalities as a Fullnode. It will support querying block data synchronized after the node started up, but it will still not support querying block data from before the node's startup snapshot.

Therefore, if developers only need to use a node for block synchronization, processing, and broadcasting transactions, a Lite Fullnode is a better choice.

## Lite Fullnode Deployment
The deployment steps, configuration file, and startup command for a Lite Fullnode are the same as a Fullnode's. Please refer to the [Deployment Guide](installing_javatron.md) to deploy a Lite Fullnode. The only difference is the database. You have two ways to obtain the required Lite Fullnode database:
 - Download the Lite Fullnode data snapshot from the [Public Backup Data](backup_restore.md/#lite-fullnode) and use it directly.
 - Use the [Lite Fullnode Pruning Tool](toolkit.md/#_6) to convert a Fullnode's database into a Lite Fullnode's database.


## Lite Fullnode Maintenance
Although a Lite Fullnode starts with a very small amount of data, it will continuously sync and save new block data just like a Fullnode after it's running. As a result, its data expansion rate is the same as a Fullnode's, and its disk usage will grow over time.

To manage disk space, you can perform periodic maintenance (pruning) on the Lite Fullnode's data. This maintenance is also done using the Lite Fullnode Pruning Tool, which re-prunes the current node data into a new snapshot dataset containing only the latest state.