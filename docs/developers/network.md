# P2P Network Deep Dive

> This article focuses on how the P2P network works internally (architecture, block synchronization, and broadcast). For how to **configure** a node to discover peers and connect to a network (config.conf parameters, boot/seed nodes, active/passive peers), see [Connect to the TRON Network](../using_javatron/connecting_to_tron.md).

## Overview
A Peer-to-Peer (P2P) network is a distributed architecture where participants share a portion of their hardware resources, such as processing power, storage capacity, network connection capacity, printers, etc. These shared resources need to be provided services and content by the network, which can be accessed by other peers directly without going through an intermediate entity. Participants in this network are both providers and acquirers of service and content.

Unlike traditional Client/Server architectures, all nodes in a P2P network have equal status. While serving as a client, each node can also serve as a server to provide services to other nodes, which greatly improves the utilization of resources.


### Blockchain Network
P2P is the network layer in the blockchain structure. The main purpose of the network layer is to realize information broadcast, verification and communication between nodes. The blockchain network is essentially a P2P network, and each node can both receive and generate information. Nodes keep communication by maintaining common blockchain data.

As the foundation of the blockchain, the P2P network brings the following advantages to the blockchain:

* Prevent single-point attack
* High fault tolerance
* Better compatibility and scalability


### TRON Network
The architecture diagram of TRON is as follows:

![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/network_architecture.png)

As the most fundamental module of TRON, the P2P network directly determines the stability of the entire blockchain network. The network module can be divided into the following four parts according to the function:

* Node Discovery
* [Node Connection](#peer-connection-management)
* [Block Synchronization](#block-synchronization)
* [Block and Transaction Broadcast](#block-and-transaction-broadcast)

The underlying implementations of **Node Discovery** and **Node Connection** have been extracted from the java-tron repository into a standalone external dependency, [`io.github.tronprotocol:libp2p`](https://github.com/tronprotocol/libp2p). This library is responsible for low-level node discovery (based on the Kademlia algorithm) and connection transport, and it adds capabilities such as DNS-based node discovery. The TRON protocol layer above it — including the P2P_HELLO handshake, P2P_PING/P2P_PONG keep-alive, peer business-state management, message dispatch, synchronization, and broadcast — is still implemented in java-tron's `core/net`, which integrates with libp2p through `TronNetService`. For the low-level discovery and connection implementation details, please refer to the libp2p repository; they are no longer covered in this document.

**Block Synchronization** and **Block and Transaction Broadcast** are still implemented in java-tron's `core/net`, and are introduced separately below.

## Peer Connection Management

When random peer disconnection is enabled and the node has reached its maximum number of connections, java-tron periodically frees a connection slot so that it can discover potentially better peers. Trusted peers are never selected. In the primary selection path, peers that are synchronizing in either direction are also excluded. If at least three eligible broadcast peers remain, java-tron sorts them by `blockRcvTime`—the time at which each peer last supplied a successfully processed block—and keeps the older half as candidates. It then makes a weighted random selection based on `lastInteractiveTime`, so peers that have been inactive for longer are more likely to be disconnected. This prevents a full connection table from being occupied indefinitely by peers that contribute little recent block data.

For received block inventory, `lastInteractiveTime` is updated only when a peer announces a block above the local head. Stale block inventory therefore cannot make a peer appear recently active.

## Block Synchronization

After completing the handshake with the peer node, if the peer node's blockchain is longer than the local blockchain, the block synchronization process `syncService.startSync` will be triggered according to the longest chain principle. The message interaction during the synchronization process is as follows:

![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/network_syncflow.png)

Node A sends an `SYNC_BLOCK_CHAIN` message to peer node B to announce the blockchain summary information of the local chain. After the peer node B receives it, it calculates the list of missing blocks of node A, and sends the lost block ID list to node A through the `BLOCK_CHAIN_INVENTORY` message, carrying a maximum of 2000 block ids at a time.

After node A receives the `BLOCK_CHAIN_INVENTORY` message, it gets the missing block id, and sends a `FETCH_INV_DATA` message to node B asynchronously to request the missing block, up to 100 blocks at a time. If there are still blocks that need to be synchronized (that is, the remain_num in the `BLOCK_CHAIN_INVENTORY` message is greater than 0), a new round of block synchronization process will be triggered.

After node B receives the `FETCH_INV_DATA` message from node A, it sends the block to node A through the `BLOCK` message. After node A receives the `BLOCK` message, it asynchronously processes the block.

### Synchronization Limits and Resource Control

An inbound `SYNC_BLOCK_CHAIN` message must contain at least one block ID and may contain no more than 30 block IDs. A message outside these bounds is treated as an invalid protocol message. The separate `BLOCK_CHAIN_INVENTORY` response can still carry up to 2000 missing block IDs, as described above.

To reduce retained heap usage during catch-up, java-tron stores pending synchronization blocks in its queues as a block ID plus serialized bytes instead of retaining a parsed `BlockCapsule`. The bytes are parsed again when the queued block is ready to be processed.

`node.maxPendingBlockSize` provides a global budget for new forward-progress synchronization requests. The available budget accounts for blocks requested across active peers, blocks just received, and blocks waiting to be processed. Retry requests for heights at or below the highest previously requested height may bypass this budget to avoid a synchronization deadlock, so the setting is not a strict upper bound on all in-flight blocks. Its default value is `500`; values outside the supported range of `50` to `2000` are clamped to the nearest bound.

### Blockchain Summary and List of Missing Blocks
Below will take several different block synchronization scenarios as examples to illustrate the generation of the blockchain summary and the lost block ID list. 

* Blockchain summary: an ordered list of block IDs, including the highest solidified block, the highest non-solidified block, and the blocks corresponding to the dichotomy.
* List of missing blocks: The neighbor node compares its own chain with the received blockchain summary, determines the missing blocks list of peers, and returns a set of consecutive block IDs and the number of remaining blocks.

#### Normal Synchronization Scene

The height of the local header block is 1018, and the height of the solidified block is 1000. The two nodes have just established a connection, so the height of the common block is 0. The local blockchain summary of node A obtained by the dichotomy is 1000, 1010, 1015, 1017, and 1018.

After node B receives the blockchain summary of node A, combined with the local chain, it can produce the list of blocks that node A lacks: 1018, 1019, 1020, and 1021. Then, node A requests to synchronize blocks 1019, 1020, and 1021 according to the list of missing blocks.

![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/network_sync1.png)


#### Chain-Switching Scene

The head block height of the local main chain is 1018, and the height of the solidified block is 1000. The two nodes have just established a connection, so the height of the common block is 0. The local blockchain summary of node A obtained by the dichotomy is 1000, 1010, 1015, 1017, and 1018.

After node B receives the chain summary of node A, it finds that the local main chain is not the same as the main chain of node A, compares the chain summary of node A and finds that the common block height is 1015, then it computes the list of blocks that node A lacks are 1015, 1016', 1017', 1018', and 1019'. Then, node A requests to synchronize blocks 1018' and 1019' according to the list of missing blocks.

![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/network_sync2.png)

In another switching chain scenario, the height of the local main chain header block is 1018, the height of the solidified block is 1000, and the common block is 1017', which is located on the fork chain. The local blockchain summary of node A obtained by the dichotomy is 1000, 1009, 1014, 1016', and 1017'.

After node B receives the chain summary of node A, combined with the local chain, it can produce the list of blocks that node A lacks 1017', 1018', and 1019'. Then, node A requests to synchronize blocks 1018', and 1019' according to the list of missing blocks.

![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/network_sync3.png)

## Block and Transaction Broadcast

When the super representative node produces a new block, or the fullnode receives a new transaction initiated by the user, the transaction & block broadcasting process will be initiated. When a node receives a new block or new transaction, it will forward the corresponding block or transaction, and the forwarding process is the same as that of broadcasting. The message interaction is shown in the following figure:

![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/network_broadcastflow.png)

The types of messages involved include:

* `INVENTORY` - broadcast list: list of block or transaction ids
* `FETCH_INV_DATA` - the list data that the node needs to get: block or transaction id list
* `BLOCK` - block data
* `TRXS` - transaction data

Node A sends the transaction or block to be broadcast to Node B via the `INVENTORY` list message. After node B receives the `INVENTORY` list message, it needs to check the status of the peer node, and if it can receive the message, it puts the blocks/transactions in the list into the "to be fetched queue" `invToFetch`. If it is a block list, it will also trigger the "get block & transaction task" immediately to send a `FETCH_INV_DATA` message to node A to get the block & transaction.

After node A receives the `FETCH_INV_DATA` message, it will check whether an "INVENTORY" message has been sent to the peer. If it has been sent, it will send a transaction or block message to node B according to the list data. After node B receives the transaction or block message, it processes the message and triggers the forwarding process.

### Inbound Validation and Backpressure

Before accepting or forwarding broadcast data, java-tron applies validation and resource controls at the P2P boundary:

| Check | Behavior |
|---|---|
| Inventory type and duplicates | The inventory type in an `INVENTORY` or `FETCH_INV_DATA` message must be either `TRX` or `BLOCK`. Duplicate hashes within either message and duplicate transactions within a `TRXS` message cause the message to be rejected and the sending peer to be disconnected with `BAD_PROTOCOL`. |
| Transaction inventory rate | The number of transaction IDs announced by each peer is limited by `node.maxTps`, which defaults to `1000` IDs per second. The limit is evaluated over a 10-second window and includes the IDs in the current message. A transaction `INVENTORY` message that would exceed the projected window limit is dropped. |
| Block inventory rate | Block inventory from each peer is limited by `node.maxBlockInvPerSecond`. The limit is enforced over a rolling 10-second window. With the default value of `10`, up to `100` block IDs are allowed in the window, including IDs in the current message. Values below `1` are raised to `1`. A block `INVENTORY` message that would exceed the window limit is dropped. |
| Transaction backpressure | If the transaction handling queues and transaction cache exceed `node.maxTrxCacheSize`, new transaction inventory announcements are dropped until capacity becomes available. The default is `50000`; values below `2000` are raised to `2000`. |
| Signature length | Every signature in a transaction received over P2P, as well as the signature in a fast-forward `HelloMessage`, must be between `65` and `68` bytes, inclusive. A transaction containing a signature outside this range is treated as a bad transaction; an incorrectly sized `HelloMessage` signature is rejected before signature verification. |
| Block validation | An announced block is validated before it is re-broadcast. An invalid Merkle root or block signature causes the sending peer to be disconnected with the `BAD_BLOCK` reason. |
| Protobuf normalization | For a received `Block`, java-tron removes unknown protobuf fields from both the block itself and its `BlockHeader` before processing or forwarding it. |

## Summary
This article introduces the P2P network, the lowest level module of TRON. Node discovery and node connection have been extracted into the external libp2p dependency and are only briefly located here; block synchronization and the process of block and transaction broadcasting, which remain in java-tron's `core/net`, are introduced in detail. I hope that reading this article can help developers to further understand and develop java-tron network-related modules.
