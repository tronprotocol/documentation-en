# Network
## Overview
P2P is a distributed network in which participants in the network share a part of the hardware resources they own, such as processing power, storage capacity, network connection capacity, printers, etc. These shared resources need to be provided services and content by the network, which can be accessed by other peers directly without going through an intermediate entity. Participants in this network are both providers and acquirers of service and content.

Different from the traditional Client/Server central server structure, the status of each node in the P2P network is equal. While serving as a client, each node can also serve as a server to provide services to other nodes, which greatly improves the utilization of resources.


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

* [Node Discovery](#node-discovery)
* [Node Connection](#node-connection)
* [Block Synchronization](#block-synchronization)
* [Block and Transaction Broadcast](#block-and-transaction-broadcast)

Below will separately introduce these four functional parts.


## Node Discovery
Node discovery is the first step for nodes to access the blockchain network. The blockchain network is a structured P2P network which organizes all nodes in an orderly manner, such as forming a ring network or a tree-like network. Structured networks are generally implemented based on the DHT (Distributed Hash Table) algorithm. Specific implementation algorithms include Chord, Pastry, CAN, Kademlia and so on. The TRON network uses the Kademlia algorithm.

### Kademlia Algorithm
Kademlia is an implementation of Distributed Hash Table (DHT), it is the core routing technology in the decentralized P2P network and can quickly find target nodes in the network without a central server.

For a detailed introduction to the algorithm, please refer to [Kademlia](https://en.wikipedia.org/wiki/Kademlia).

### Kademlia Implementation by TRON
The main points of the Kademlia algorithm implemented by TRON are as follows:

* Node ID: Randomly generated 512bit ID
* Node Distance: The node distance is obtained through the XOR operation of two nodes' ID. The formula is: `Node distance = 256 - the number of leading 0s in the node ID XOR result`, if the calculation result is negative, the distance is equal to 0.
* K-Bucket: The node routing table. According to the distance between the nodes, the remote nodes are divided into different buckets. The remote nodes with the same distance as the current node are recorded in the same bucket, and each bucket can accommodate up to 16 nodes. According to the calculation formula of node distance, it can be seen that the Kademlia algorithm implemented by TRON maintains a total of 256 buckets.


The node discovery protocol of TRON includes the following four UDP messages:

* `DISCOVER_PING` - used to detect if a node is online
* `DISCOVER_PONG` - used in response to `DISCOVER_PING` message
* `DISCOVER_FIND_NODE` - used to find other nodes closest to the target node
* `DISCOVER_NEIGHBORS` - used in response to `DISCOVER_FIND_NODE` message, will return one or more nodes, up to 16

#### Initialize K-Buckets
After the node is started, it will read the seed nodes configured in the node configuration file and the peer nodes recorded in the database, and then send `DISCOVER_PING` message to them respectively. If the reply message `DISCOVER_PONG` from a peer is received, and at the condition that the K bucket is not full, it will then write the peer node into the K bucket; But if the corresponding bucket has already been full (that is the bucket has reached 16 nodes), it will challenge to the earliest node in the bucket. If the challenge is successful, the old node will be deleted, and the new node will be added to the K bucket. That is the K bucket initialization process, then the node discovery process is performed.


![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/network_discoverinit.png)

#### Send DISCOVER_FIND_NODE to Find More Nodes

The node discovery service will start two scheduled tasks (`DiscoverTask` and `RefreshTask`) to periodically perform the node discovery process to update k buckets.

* `DiscoverTask` is to discover more nodes that are closer to myself. It is executed every 30s. The execution flow is as follows:
    ![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/network_discovertask.png)
* `RefreshTask` is to expand the local k-bucket by random node ID, that is, to find nodes that are closer to the random node ID. It is executed every 7.2s. The execution process is as follows:
    ![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/network_refreshtask.png)


The node discovery algorithm used in `DiscoverTask` and `RefreshTask` will be executed 8 rounds in one call, and each round sends `DISCOVER_FIND_NODE` message to the 3 nodes closest to the target node ID in the K bucket, and waits for a reply.


#### Receive Neighbors' Messages and Update K Bucket
When the local node receives the `DISCOVER_NEIGHBORS` message replied by the remote node, it will send the `DISCOVER_PING` message to the received neighbor node in turn, and then if it receives the reply message `DISCOVER_PONG`, it will judge whether the corresponding K-bucket is full, if the K-bucket is not full, it will add the new node to the K bucket, if the K bucket is full, it will challenge one of the nodes, if the challenge is successful (send a `DISCOVER_PING` message to the old node, if it fails to receive the reply message `DISCOVER_PONG`, the challenge is successful, otherwise the challenge fails), the old node will be deleted from the K bucket, and the new node will be added to the K bucket.

![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/network_updatek.png)


Nodes periodically perform node discovery tasks, continuously update K-buckets, and build their own node routing tables. The next step is to establish a connection with nodes.

## Node Connection

Before understanding how to establish a TCP connection between nodes, we need to first understand the peer node type.

### Peer Node Management
The local node needs to manage and classify peer nodes for efficient and stable node connection. Remote nodes can be divided into the following categories:

* Active nodes: specified in the configuration file. After the system starts, it will actively establish connections with the nodes. If the connection fails to be established, it will retry in each scheduled TCP connection task.
* Passive nodes: specified in the configuration file. The local node will passively accept connections from them.
* Trust nodes: specified in the configuration file, both Active nodes and Passive nodes are trusted nodes. When receiving a connection request from a trusted node, some other condition checks are skipped and the request is accepted directly.
* BadNodes: When an abnormal protocol packet is received, the sending node will be added to the badNodes list, valid for 1 hour. When a connection request from badNodes is received, the request will be rejected directly
* RecentlyDisconnectedNodes: When a connection is disconnected, the peer node will be added to the recentlyDisconnectedNodes list, valid for 30s, when a connection request from recentlyDisconnectedNodes is received, the request will be rejected directly

### Establish TCP Connection with Peers
After the node is started, a scheduled task `poolLoopExecutor` will be created to establish a TCP connection with nodes. It will select nodes and establish connections with them. The working process is as follows:

![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/network_connect.png)

The TCP connection can be mainly divided into two steps: first, determine the node list which the node will establish a connection with. The list needs to contain the active nodes that have not successfully established a connection, and then calculate the number of connections that also need to be established, and filter out the nodes from discovered neighbors according to the [node filtering strategy](#node-filtering-strategy), then score and sort them according to the [node scoring strategy](#node-scoring-strategy), and the corresponding number of nodes with the highest score is added to the request list. Finally, TCP connections are established with the nodes in the request list.

#### Node Filtering Strategy
When establishing a node connection, it is necessary to filter out the following types of nodes and determine whether the node's own connection number has reached the maximum value.

* Myself
* Nodes in the recentlyDisconnectedNodes list
* Nodes in badNodes list
* Nodes that have already established a connection
* The number of connections established with the node IP has already reached the upper limit (maxConnectionsWithSameIp)

But for trusted nodes, some filtering policies are ignored and connections are always established.

![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/network_filterrule.png)



#### Node Scoring Strategy
The node score is used to determine the priority of nodes to establish a connection. The higher the score, the higher the priority. Scoring dimensions include:

* Packet loss rate: The lower the packet loss rate, the better the communication quality. The score is inversely proportional to the packet loss rate. The highest score is 100 and the lowest is 0.
* Network delay: The smaller the network delay, the better the network quality. The score is inversely proportional to the average network latency. The highest score is 20 and the lowest is 0.
* TCP traffic: The larger the TCP traffic, the more active the communication. The score is proportional to the TCP traffic, with a maximum score of 20 and a minimum of 0
* Disconnection times: The fewer disconnection times, the more stable the node is. The score is inversely proportional to the number of disconnections. The score is 10 times the number of disconnections.
* Handshake: Nodes that have been handshake successfully before indicate that they have the same blockchain information, so it is preferred to establish a connection with them. When the number of successful Handshakes is greater than 0, the Handshake score is 20, otherwise, the score is 0.
* Penalty state: A node in the Penalty state has a score of 0 and does not participate in scoring in other dimensions. The following situations will be regarded as in the Penalty state:
    * Node disconnection time is less than 60s
    * The node is in the badNodes list
    * Inconsistent blockchain information

When calculating the node score, first determine whether the node is in the Penalty state, if so, the score is counted as 0, otherwise, the node score is the sum of the scores of each dimension.

### Handshake

After the TCP connection is successfully established, the node that actively initiates the TCP connection request will send a handshake message `P2P_HELLO` to the neighbor node, in order to confirm whether the blockchain information between the nodes is consistent and whether it is necessary to initiate the block synchronization process.

When the neighbor node receives `P2P_HELLO`, it will compare with the local information, such as checking whether the p2p version and the genesis block information are consistent. If all the check conditions are passed, it will reply to the `P2P_HELLO` message, and then perform the block synchronization or broadcast; otherwise, it will disconnect the connection.

### Channel Keep-Alive
Channel keep-alive is accomplished through `P2P_PING`, `P2P_PONG` TCP messages. When a node establishes a TCP connection with a neighbor node and handshakes successfully, the node will open a thread `pingTask` for the connection and periodically send `P2P_PING` messages to maintain the TCP connection, which is scheduled every 10s. If the `P2P_PONG` message replied is not received within the timeout period, the connection will be terminated.

## Block Synchronization

After completing the handshake with the peer node, if the peer node's blockchain is longer than the local blockchain, the block synchronization process `syncService.startSync` will be triggered according to the longest chain principle. The message interaction during the synchronization process is as follows:

![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/network_syncflow.png)

Node A sends an `SYNC_BLOCK_CHAIN` message to peer node B to announce the blockchain summary information of the local chain. After the peer node B receives it, it calculates the list of missing blocks of node A, and sends the lost block ID list to node A through the `BLOCK_CHAIN_INVENTORY` message, carrying a maximum of 2000 block ids at a time.

After node A receives the `BLOCK_CHAIN_INVENTORY` message, it gets the missing block id, and sends a `FETCH_INV_DATA` message to node B asynchronously to request the missing block, up to 100 blocks at a time. If there are still blocks that need to be synchronized (that is, the remain_num in the `BLOCK_CHAIN_INVENTORY` message is greater than 0), a new round of block synchronization process will be triggered.

After node B receives the `FETCH_INV_DATA` message from node A, it sends the block to node A through the `BLOCK` message. After node A receives the `BLOCK` message, it asynchronously processes the block.

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

## Summary
This article introduces the implementation details related to the P2P network, the lowest level module of TRON, including node discovery, node connection, block synchronization, and the process of block and transaction broadcasting. I hope that reading this article can help developers to further understand and develop java-tron network-related modules.
