# Event Subscription

TRON provides a robust event subscription mechanism that allows developers to capture critical on-chain events in real-time. This includes transaction statuses, contract invocations, and block production, facilitating the development of feature-rich decentralized applications (dApps).

## Overview of Subscription Methods

TRON offers two primary event subscription methods, each designed to cater to different use cases and technical requirements.

### 1. Local Event Plugin Subscription (Recommended)

This method utilizes an extensible plugin architecture to persistntly store on-chain events in external systems, such as **MongoDB** or **Kafka**, either in real-time or in batches. Designed specifically for production environments, this solution caters to applications requiring high reliability, durable storage, and robust data analysis capabilities.

This method has the following advantages:

  - **Diverse Plugin Support:** Currently supports Kafka and MongoDB.
  - **Rich Data Types**: Enables subscriptions to blocks, transactions, smart contract events, and logs.
  - **Advanced Filtering**: Supports filtering of events based on user-defined criteria.
  - **Historical Event Replay**: The V2.0 framework allows syncing historical events from any specified block height.
  - **Production-Grade Reliability**: Ideal for applications requiring high data integrity and dependability.

> **Important Note**: In extreme situations such as network forks, non-solidified events might be rolled back. Therefore, in scenarios with high demand for data reliability, subscribing to solidified events is strongly recommended.


### 2. Built-in Message Queue Subscription (ZeroMQ)

The java-tron node includes a built-in **ZeroMQ** message queue that provides a lightweight event streaming service. This method requires no external plugins and is ideal for use cases that demand high real-time event delivery but do not require event persistence or historical replay, such as rapid prototyping and testing.

This method has the following advantages:

  - **No Plugin Deployment**: Subscriptions are established by connecting directly to a TRON node.
  - **Low Latency**: Optimized for real-time event streaming.
  - **Lightweight**: Well-suited for rapid development and testing environments.


## Event Service Framework (Based on Local Plugin)

java-tron currently supports two versions of the event service framework: `V1.0` and `V2.0`.

- **V1.0**: Only supports real-time event streaming for newly produced blocks.
- **V2.0 (Recommended)**:  Introduces a historical event replay feature, enabling synchronization from a specified block height.

For a detailed comparison and guidance, refer to: [Introduction to Event Service Framework V2.0](https://medium.com/tronnetwork/event-service-framework-v2-0-0622f2f07249).

**Workflow**:

1. **Event Capture**: The TRON node extracts event data from on-chain blocks.
2. **Event Queuing**: Events are encapsulated and added to a buffer queue.
3. **Plugin Consumption**: The event plugin asynchronously consumes events from the queue.
4. **Event Delivery**: The plugin pushes the processed data to the target system (e.g., Kafka or MongoDB).
5. **Application Logic**: Downstream applications continuously process the event data.


## Event Types

Developers can flexibly specify the event types they want to subscribe to by modifying the node's configuration file, `config.conf`.


### 1. Transaction Event

Subscribes to events related to on-chain transactions.

**Configuration Example：**

```
event.subscribe.topics = [
  {
    triggerName = "transaction"
    enable = false
    topic = "transaction"
    solidified = false
    ethCompatible = false
  }
]
```
**Parameters**:

- `triggerName`: (String) The event type identifier. For transaction events, this value is fixed to `transaction`.
- `enable`: (Boolean) Enables or disables the subscription for this event type.
- `topic`: (String) The name of the topic for receiving this event type in MongoDB or Kafka. This value must be consistent with the configuration in MongoDB or Kafka.
- `solidified`: (Boolean) If set to `true`, the subscription will only deliver events for transactions included in solidified blocks.
- `ethCompatible`: (Boolean) If set to `true`, the event payload will include Ethereum-compatible fields (e.g., `transactionIndex`, `logList`).

**Key Fields in Transaction Events:**

- `transactionId`: The transaction hash.
- `blockNumber`: The block height containing the transaction.
- `energyUsage`: The total amount of Energy consumed by the transaction.
- `energyFee`: The total amount of TRX (in sun) consumed by the transaction.


For a complete list of fields, see the [TransactionLogTrigger](https://github.com/tronprotocol/java-tron/blob/develop/common/src/main/java/org/tron/common/logsfilter/trigger/TransactionLogTrigger.java) source code.

### 2. Block Events

Subscribes to events triggered upon the creation of new blocks.

**Configuration Example：**

```
event.subscribe.topics = [
  {
    triggerName = "block"
    enable = false
    topic = "block"
    solidified = false
  }
]
```

**Key Fields in Block Events:**

- `blockHash`: The hash of the block.
- `blockNumber`: The block height.
- `transactionSize`: The total number of transactions included in the block.
- `latestSolidifiedBlockNumber`: The block number of the most recently solidified block at the time of this event.
- `transactionList`: An array of transaction hashes contained within the block.


For a complete list of fields, see the [BlockLogTrigger](https://github.com/tronprotocol/java-tron/blob/develop/common/src/main/java/org/tron/common/logsfilter/trigger/BlockLogTrigger.java) source code.

### 3. Contract Events and Logs

Subscribes to smart contract events and logs generated during contract execution.

**Configuration Example：**

```
event.subscribe.topics = [
  {
    triggerName = "contractevent"
    enable = false
    topic = "contractevent"
  },
  {
    triggerName = "contractlog"
    enable = false
    topic = "contractlog"
  },
  {
    triggerName = "solidityevent"
    enable = false
    topic = "solidityevent"
  },
  {
    triggerName = "soliditylog"
    enable = false
    topic = "soliditylog"
  }
]
```

  - `contractevent`: Subscribes to all contract events from all blocks.
  - `contractlog`: Subscribes to all contract logs from all blocks.
  - `solidityevent`: Subscribes only to contract events from solidified blocks.
  - `soliditylog`: Subscribes only to contract logs from solidified blocks.

**Key Fields in Contract Events**

  - `transactionId`: The hash of the transaction that generated the event.
  - `contractAddress`: The address of the smart contract.
  - `blockNumber`: The block height at which the event was included.

For a complete list of fields, see the [ContractEventTrigger](https://github.com/tronprotocol/java-tron/blob/develop/common/src/main/java/org/tron/common/logsfilter/trigger/ContractEventTrigger.java) and [ContractLogTrigger](https://github.com/tronprotocol/java-tron/blob/develop/common/src/main/java/org/tron/common/logsfilter/trigger/ContractLogTrigger.java) source code.

> **Note**: Subscriptions for `contractevent` and `contractlog` support the following filter parameters:
> ```
> fromBlock: The starting block number.
> toBlock: The ending block number.
> contractAddress: The specific contract address to monitor.
> contractTopics: An array of indexed event topics for filtering.
> ```


### 4. Solidified Block Notification Events

Subscribes to real-time notifications for the latest solidified block height. This is ideal for applications that need to track the chain's finalized state.


**Configuration Example：**

```
event.subscribe.topics = [
  {
    triggerName = "solidity"
    enable = true
    topic = "solidity"
  }
]
```

**Key Fields in Solidity Notification Events:**

  - `latestSolidifiedBlockNumber`: The block number of the newly solidified block.
  - `timestamp`: The timestamp of the solidified block.

For a complete list of fields, see the [SolidityTrigger](https://github.com/tronprotocol/java-tron/blob/develop/common/src/main/java/org/tron/common/logsfilter/trigger/SolidityTrigger.java) source code.


## Migrating to V2.0 Event Service Framework

The `V2.0` event service framework introduces a historical event replay feature and includes comprehensive optimizations to the event push mechanism. This guide outlines the procedure for migrating to `V2.0`.

### Pre-Migration Considerations

Before migrating, please consider the following factors:

- **Internal Transaction Log Support**: `V2.0` currently does not support internal transaction logs (the `internalTransactionList` field will be empty). If your application has a dependency on this field, you must remain on `V1.0`.
- **Plugin Version**: We strongly recommend upgrading the event plugin to the latest version to prevent potential performance degradation when processing large volumes of historical data.
 
### Migration Procedure

#### Step 1: Obtain the New Event Plugin

You can get the source code from GitHub and build it yourself, or download the officially released version directly.

**Build from Source:**

```
git clone git@github.com:tronprotocol/event-plugin.git
cd event-plugin
git checkout master
./gradlew build
```
After the build is complete, the generated `.zip` file is the plugin package.


**Download the Official Release:**

Visit the [event-plugin Releases page](https://github.com/tronprotocol/event-plugin/releases) to download the latest plugin package.

#### Step 2: Modify the FullNode Configuration

In your `config.conf` file, set the event service version to `V2.0`, the value is `1`.

```
event.subscribe.version = 1 # 1 for V2.0，0 for V1.0
```

#### Step 3: Configure the Event Plugin

The configuration process for the new plugin is mostly identical to the old version. You can refer to the official documentation for deployment:

  - [Deploying the Event Plugin (MongoDB)](/documentation-en/architecture/use-mongodb/)
  - [Deploying the Event Plugin (Kafka)](/documentation-en/architecture/use-kafka/)

#### Step 4 (Optional): Configure the Starting Point for Historical Sync

If you need to sync historical events starting from a specific block height, add the following setting to your configuration file.

```
event.subscribe.startSyncBlockNum = <block_height>
```

#### Step 5: Start the Fullnode and Plugin

After completing the configuration, use the following command to start the `FullNode` and load the event plugin.

```
java -jar FullNode.jar -c config.conf --es
```