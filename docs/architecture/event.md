# Event Subscription

TRON provides a robust event subscription mechanism that allows developers to capture critical on-chain events in real-time. This includes transaction statuses, contract invocations, and block production, facilitating the development of feature-rich decentralized applications (dApps).

TRON offers two primary event subscription methods, allowing developers to choose based on their specific use cases:

* [Local Event Plugin Subscription](#local-event-plugin-subscription-recommended)
* [Built-in Message Queue (ZeroMQ) Subscription](#built-in-message-queue-subscription-zeromq)

## Local Event Plugin Subscription (Recommended)

This method utilizes an extensible plugin architecture to persistntly store on-chain events in external systems, such as **MongoDB** or **Kafka**, either in real-time or in batches. Designed specifically for production environments, this solution caters to applications requiring high reliability, durable storage, and robust data analysis capabilities.

This method has the following advantages:

  - **Diverse Plugin Support:** Currently supports Kafka and MongoDB.
  - **Rich Data Types**: Enables subscriptions to blocks, transactions, smart contract events, and logs.
  - **Advanced Filtering**: Supports filtering of events based on user-defined criteria.
  - **Historical Event Replay**: The V2.0 framework allows syncing historical events from any specified block height.
  - **Production-Grade Reliability**: Ideal for applications requiring high data integrity and dependability.


### Event Service Framework

java-tron currently supports two versions of the event service framework: `V1.0` and `V2.0`.

- **V1.0**: Only supports real-time event streaming for newly produced blocks.
- **V2.0 (Recommended)**:  Introduces a historical event replay feature, enabling synchronization from a specified block height.

For a detailed comparison and guidance, refer to: [Introduction to Event Service Framework V2.0](https://medium.com/tronnetwork/event-service-framework-v2-0-0622f2f07249).

**Workflow of Event Service**:

1. **Event Capture**: The TRON node extracts event data from on-chain blocks.
2. **Event Queuing**: Events are encapsulated and added to a buffer queue.
3. **Plugin Consumption**: The event plugin asynchronously consumes events from the queue.
4. **Event Delivery**: The plugin pushes the processed data to the target system (e.g., Kafka or MongoDB).
5. **Application Logic**: Downstream applications continuously process the event data.

#### How to Migrate to Event Service Framework V2.0 

The `V2.0` event service framework introduces a historical event replay feature and includes comprehensive optimizations to the event push mechanism. This guide outlines the procedure for migrating to `V2.0`.

**Pre-Migration Considerations**

Before migrating, please consider the following factors:

- Internal Transaction Log Support: `V2.0` currently does not support internal transaction logs (the `internalTransactionList` field will be empty). If your application has a dependency on this field, you must remain on `V1.0`.
- Plugin Version: We strongly recommend upgrading the event plugin to the latest version to prevent potential performance degradation when processing large volumes of historical data.
 
**Migration Procedure**

##### Step 1: Obtain the New Event Plugin

You can get the source code from GitHub and build it yourself, or download the officially released version directly.

* Build from Source:

```
git clone git@github.com:tronprotocol/event-plugin.git
cd event-plugin
git checkout master
./gradlew build
```
After the build is complete, the generated `.zip` file is the plugin package.


* Download the Official Release:

Visit the [event-plugin Releases page](https://github.com/tronprotocol/event-plugin/releases) to download the latest plugin package.

##### Step 2: Modify the FullNode Configuration

In your `config.conf` file, set the event service version to `V2.0`, the value is `1`.

```
event.subscribe.version = 1 # 1 for V2.0，0 for V1.0
```

##### Step 3: Configure the Event Plugin

The configuration process for the new plugin is mostly identical to the old version. You can refer to the official documentation for deployment:

  - [Deploying the Event Plugin (MongoDB)](#mongodb-plugin-deployment-and-usage)
  - [Deploying the Event Plugin (Kafka)](#kafka-plugin-deployment-and-usage)

##### Step 4 (Optional): Configure the Starting Point for Historical Sync

If you need to sync historical events starting from a specific block height, add the following setting to your configuration file.

```
event.subscribe.startSyncBlockNum = <block_height>
```

##### Step 5: Start the Fullnode and Plugin

After completing the configuration, use the following command to start the `FullNode` and load the event plugin.

```
java -jar FullNode.jar -c config.conf --es
```

### Kafka Plugin: Deployment and Usage

This guide is designed to help developers efficiently use the Kafka event subscription plugin to listen for on-chain events on the TRON network. We will walk you through the entire process step-by-step, from environment setup to deployment, configuration, and final verification.

The main steps include:

- [Checking System Configuration](#recommended-system-configuration)
- [Compiling the Event Plugin](#compiling-the-kafka-event-plugin)
- [Deploying and Running Kafka](#deploying-and-running-kafka)
- [Configuring Event Subscription Rules](#configuring-event-subscription)
- [Creating the Kafka Subscription Topic](#creating-a-kafka-subscription-topic)
- [Starting the Event Subscription Node](#starting-the-event-subscription-node)


#### Recommended System Configuration

To ensure the stable operation of your TRON node and event subscription service, the following system configuration is recommended:

  * **CPU**: 16 cores or higher
  * **RAM**: 32 GB or higher
  * **SSD**: 2.5 TB or more of storage space
  * **Operating System**: Linux or macOS


#### Compiling the Kafka Event Plugin

First, you need to clone the `event-plugin` project from its GitHub repository and compile it to generate the plugin's `.zip` file. Please follow these steps:

```
git clone https://github.com/tronprotocol/event-plugin.git
cd event-plugin
./gradlew build
```

After a successful compilation, you will find the generated `.zip` plugin file in the `event-plugin/build/plugins/` directory, for example, `plugin-kafka-1.0.0.zip`.



#### Deploying and Running Kafka

##### Step 1. Installing Kafka

In a Linux environment, please follow these steps to install Kafka:

```
cd /usr/local
wget https://downloads.apache.org/kafka/2.8.0/kafka_2.13-2.8.0.tgz
tar -xzf kafka_2.13-2.8.0.tgz
```

##### Step 2: Running Kafka

In a Linux environment, please follow these steps to start the ZooKeeper and Kafka Broker services:

```shell
cd /usr/local/kafka_2.13-2.8.0
# Start the ZooKeeper service
bin/zookeeper-server-start.sh config/zookeeper.properties &
# Start the Kafka Broker service
bin/kafka-server-start.sh config/server.properties &
```


#### Configuring Event Subscription

To support Kafka event subscriptions, you need to modify the Fullnode's configuration file (`config.conf`) by adding the `event.subscribe` section.


```
event.subscribe = {
  version = 1 
  startSyncBlockNum = 0 

  native = {
    useNativeQueue = false 
  }

  path = "" 
  server = "" 
  dbconfig = "" 
  contractParse = true
  topics = []
  filter = {}
}
```

**Field Descriptions**:

  * `version`: The version of the event service framework. `1` indicates V2.0, while `0` indicates V1.0. If not configured, it defaults to V1.0.
  * `startSyncBlockNum`: A new feature in v2.0 designed for historical data subscriptions. It allows the service to start processing and pushing events from a specific historical block height stored on the local node.
      * If `startSyncBlockNum <= 0`, this feature is disabled.
      * If `startSyncBlockNum > 0`, this feature is enabled, and historical event synchronization will begin from the specified block height. **Note**: We recommend using the latest version of the event plugin when enabling this feature.
  * `native.useNativeQueue`: Specifies whether to use the built-in message queue (ZeroMQ) for event subscriptions. If you need to support Kafka event subscriptions, ensure this field is set to `false`; otherwise, Kafka subscriptions will not work.
  * `path`: The absolute local path to the `plugin-kafka-1.0.0.zip` file. Please ensure the path is correct, or the plugin will fail to load.
  * `server`: The Kafka server address in `ip:port` format. The default Kafka port is `9092`. Please ensure the port number is correct and that the Kafka service is accessible.
  * `dbconfig`: This option is only for the MongoDB plugin and should be ignored for the Kafka plugin.
  * `topics`: Configure the events to subscribe to. For more details, please refer to the [Event Types](#event-types) section below.
  * `filter`: Filtering parameters. For more details, please refer to the [Event Types](#event-types) section below.

###### Event Types

TRON event subscription supports 7 types of events: `block`, `transaction`, `contractevent`, `contractlog`, `solidity`, `solidityevent`, and `soliditylog`. Developers should configure these based on their application's specific needs. **We recommend subscribing to only 1-2 event types. Enabling too many triggers can lead to performance degradation.**

**1. Transaction Event**

Subscribes to events related to on-chain transactions.

Configuration Example：

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
Parameters:

- `triggerName`: (String) The event type identifier. For transaction events, this value is fixed to `transaction`.
- `enable`: (Boolean) Enables or disables the subscription for this event type.
- `topic`: (String) The name of the topic for receiving this event type in MongoDB or Kafka. This value must be consistent with the configuration in MongoDB or Kafka.
- `solidified`: (Boolean) If set to `true`, the subscription will only deliver events for transactions included in solidified blocks.
- `ethCompatible`: (Boolean) If set to `true`, the event payload will include Ethereum-compatible fields (e.g., `transactionIndex`, `logList`).

Key Fields in Transaction Events:

- `transactionId`: The transaction hash.
- `blockNumber`: The block height containing the transaction.
- `energyUsage`: The total amount of Energy consumed by the transaction.
- `energyFee`: The total amount of TRX (in sun) consumed by the transaction.


For a complete list of fields, see the [TransactionLogTrigger](https://github.com/tronprotocol/java-tron/blob/develop/common/src/main/java/org/tron/common/logsfilter/trigger/TransactionLogTrigger.java) source code.

**2. Block Events**

Subscribes to events triggered upon the creation of new blocks.

Configuration Example：

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

Key Fields in Block Events:

- `blockHash`: The hash of the block.
- `blockNumber`: The block height.
- `transactionSize`: The total number of transactions included in the block.
- `latestSolidifiedBlockNumber`: The block number of the most recently solidified block at the time of this event.
- `transactionList`: An array of transaction hashes contained within the block.


For a complete list of fields, see the [BlockLogTrigger](https://github.com/tronprotocol/java-tron/blob/develop/common/src/main/java/org/tron/common/logsfilter/trigger/BlockLogTrigger.java) source code.

**3. Contract Events and Logs**

Subscribes to smart contract events and logs generated during contract execution.

Configuration Example：

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

Parameters:

  - `contractevent`: Subscribes to all contract events from all blocks.
  - `contractlog`: Subscribes to all contract logs from all blocks.
  - `solidityevent`: Subscribes only to contract events from solidified blocks.
  - `soliditylog`: Subscribes only to contract logs from solidified blocks.

Key Fields in Contract Events

  - `transactionId`: The hash of the transaction that generated the event.
  - `contractAddress`: The address of the smart contract.
  - `blockNumber`: The block height at which the event was included.

For a complete list of fields, see the [ContractEventTrigger](https://github.com/tronprotocol/java-tron/blob/develop/common/src/main/java/org/tron/common/logsfilter/trigger/ContractEventTrigger.java) and [ContractLogTrigger](https://github.com/tronprotocol/java-tron/blob/develop/common/src/main/java/org/tron/common/logsfilter/trigger/ContractLogTrigger.java) source code.


> **Note**: `Contract event` and `Contract log` support event filtering through the `filter` field. You can specify a block range (`fromblock` - `toblock`), specific contract addresses (`contractAddress`), or specific contract topics (`contractTopic`) to provide developers with a more efficient and precise event subscription service.
> ```
> filter = {
>   fromblock = "" // The starting block number of the query range. Can be an empty string, "earliest", or a specific block number.
>   toblock = "" // The ending block number of the query range. Can be an empty string, "latest", or a specific block number.
>   contractAddress = [
>     "" // The contract addresses you wish to subscribe to. If set to an empty string, logs/events from all contract addresses will be received.
>   ]
>
>   contractTopic = [
>     "" // The contract topics you wish to subscribe to. If set to an empty string, logs/events for all contract topics will be received.
>   ]
> }
> ```

**4. Solidified Block Notification Events**

Subscribes to real-time notifications for the latest solidified block height. This is ideal for applications that need to track the chain's finalized state.


Configuration Example：

```
event.subscribe.topics = [
  {
    triggerName = "solidity"
    enable = true
    topic = "solidity"
  }
]
```

Key Fields in Solidity Notification Events:

  - `latestSolidifiedBlockNumber`: The block number of the newly solidified block.
  - `timestamp`: The timestamp of the solidified block.

For a complete list of fields, see the [SolidityTrigger](https://github.com/tronprotocol/java-tron/blob/develop/common/src/main/java/org/tron/common/logsfilter/trigger/SolidityTrigger.java) source code.


#### Creating a Kafka Subscription Topic

The name of the Kafka subscription topic must match the `topic` setting in the `topics` field of your `event.subscribe` configuration. For example, if you need to subscribe to `block` events and set the `topic` field in the `block` trigger to `"block"`, you must create a topic named `"block"` in Kafka to receive block events.

In a Linux environment, the command to create a Kafka topic is as follows:

```
bin/kafka-topics.sh --create --topic block --bootstrap-server localhost:9092
```

#### Starting the Event Subscription Node

After completing the above configuration, you must add the `--es` parameter when starting the FullNode to enable the event subscription feature.

```
java -jar FullNode.jar -c config.conf --es
```

##### Verifying Plugin Load

You can verify that the Kafka event plugin has loaded successfully by checking the Fullnode logs:

```
grep -i eventplugin logs/tron.log
```

If you see a message similar to the following in the logs, the event subscription plugin has loaded successfully:

```
[o.t.c.l.EventPluginLoader] 'your plugin path/plugin-kafka-1.0.0.zip' loaded
```

##### Verifying Event Subscription

Execute the `kafka-console-consumer.sh` script to retrieve messages from the `"block"` topic in Kafka to verify that the event subscription is successful.

In a Linux environment, the command is as follows:

```
bin/kafka-console-consumer.sh --topic block --from-beginning --bootstrap-server localhost:9092
```

If you see JSON-formatted output similar to the following in your console, the event subscription is successful:

```
{
	"timeStamp": 1539973125000,
	"triggerName": "blockTrigger",
	"blockNumber": 3341315,
	"blockHash": "000000000032fc03440362c3d42eb05e79e8a1aef77fe31c7879d23a750f2a31",
	"transactionSize": 16,
	"latestSolidifiedBlockNumber": 3341297,
	"transactionList": ["8757f846e541b51b5692a2370327f4b8031125f4557f8ad4b1037d4452616d39", "f6adab7814b34e5e756170f93a31a0c3393c5d99eff11e30271916375adc7467", ..., "89bcbcd063a48ef4a5678a033acf5edbb6b17419a3c91eb0479a3c8598774b43"]
}
```


### MongoDB Plugin: Deployment and Usage

This guide is designed to help developers quickly deploy and use the TRON MongoDB event subscription plugin to achieve real-time data capture, persistent storage, and querying of on-chain events. The document covers the entire process, including system environment configuration, plugin deployment, database installation, query service setup, and API usage.

The main steps include:

- [Checking System Configuration](#recommended-system-configuration_1)
- [Understanding the System Architecture](#system-architecture-and-workflow)
- [Deploying the Event Plugin](#deploying-the-event-subscription-plugin)
- [Deploying the MongoDB](#installing-and-configuring-mongodb)
- [Deploying the Event Query Service](#deploying-the-event-query-service)
- [Starting and Verifing](#launch-and-verification)
- [Using the TRON Event Query Service API](#using-the-tron-event-query-service-api)


#### Recommended System Configuration

To ensure the efficient and stable operation of your TRON node and event service, the following configuration is recommended:

  * **CPU**: 16 cores or more
  * **RAM**: 32 GB or higher
  * **SSD**: 2.5 TB or more
  * **Operating System**: Linux or macOS


#### System Architecture and Workflow

The TRON MongoDB event subscription system consists of three core modules:

1.  **Event Subscription Plugin**: Connects to a TRON node to capture event data and writes it to MongoDB.
2.  **MongoDB Database**: The persistence layer for storing event data.
3.  **Event Query Service**: Provides an HTTP API for external applications to query event data.

#### Deploying the Event Subscription Plugin

##### 1. Building the Plugin

```
git clone https://github.com/tronprotocol/event-plugin.git
cd event-plugin
./gradlew build
```

After the build is complete, the generated plugin file will be located at:

```
event-plugin/build/plugins/plugin-mongodb-*.zip
```

##### 2. Configuring the FullNode 

Add the following content to your FullNode's configuration file, `config.conf`:

```javascript
event.subscribe = {
  version = 1  
  startSyncBlockNum = 0  

  native = {
    useNativeQueue = false  
  }
  path = "/deploy/fullnode/event-plugin/build/plugins/plugin-mongodb-1.0.0.zip"  
  server = "127.0.0.1:27017"  
  dbconfig = "eventlog|tron|123456"  
  topics = [
    {
      triggerName = "block"  
      enable = false
      topic = "block"  
      solidified = false  
    },
    {
      triggerName = "transaction"
      enable = false
      topic = "transaction"
      solidified = false
      ethCompatible = false  
    },
    {
      triggerName = "contractevent"
      enable = false
      topic = "contractevent"
    },
    {
      triggerName = "contractlog"
      enable = false
      topic = "contractlog"
      redundancy = false  
    },
    {
      triggerName = "solidity"
      enable = true  
      topic = "solidity"
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
      redundancy = false  
    }
  ]

  filter = {
    fromblock = ""  
    toblock = ""  
    contractAddress = ["" ]
    contractTopic = [""]
  }
}
```

**Field Descriptions**:

  * `version`: The version of the event service framework. `1` indicates V2.0, while `0` indicates V1.0. If not configured, it defaults to V1.0.
  * `startSyncBlockNum`: A feature introduced in V2.0 that allows processing and pushing events from historical blocks, satisfying the need for historical data subscriptions. If `startSyncBlockNum <= 0`, this feature is disabled. If `startSyncBlockNum > 0`, the feature is enabled, and historical event synchronization will begin from the specified block height. **Note**: It is recommended to use the latest version of the event plugin when enabling this feature.
  * `native.useNativeQueue`: Specifies whether to use the built-in message queue (ZeroMQ) for event subscriptions. `true` uses the built-in queue, while `false` uses the plugin. This must be set to `false`.
  * `path`: The absolute path to the plugin file, e.g., `"/deploy/fullnode/event-plugin/build/plugins/plugin-mongodb-1.0.0.zip"`.
  * `server`: The target server address, i.e., the address and port for MongoDB, e.g., `"127.0.0.1:27017"`.
  * `dbconfig`: The MongoDB database configuration in the format: `database_name|username|password`, e.g., `"eventlog|tron|123456"`.
  * `topics`: Seven event types are currently supported: `block`, `transaction`, `contractevent`, `contractlog`, `solidity`, `solidityevent`, and `soliditylog`. For more details, please refer to the [Event Types](#event-types) chapter.
      * `triggerName`: The name of the trigger, which cannot be modified.
      * `enable`: Toggles the event subscription. `true` enables it, `false` disables it.
      * `topic`: The name of the collection in MongoDB that will receive the events. This can be modified.
  * `filter`: The criteria for filtering events.
      * `fromblock`: The starting block number of the query range. Can be `""`, `"earliest"` (to query from the genesis block), or a specific block number.
      * `toblock`: The ending block number of the query range. Can be `""`, `"latest"` (the most recent block), or a specific block number.
      * `contractAddress`: A list of contract addresses you wish to subscribe to. If set to an empty string, logs/events from all contract addresses will be received.
      * `contractTopic`: A list of contract topics you wish to subscribe to. If set to an empty string, logs/events for all contract topics will be received.


#### Installing and Configuring MongoDB

MongoDB will be used to store TRON event data. Please follow these steps to install and configure it:

##### 1. Installing MongoDB

First, create an installation directory for MongoDB, then download and extract the installation package:

```
mkdir /home/java-tron
cd /home/java-tron
curl -O https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-4.0.4.tgz
tar zxvf mongodb-linux-x86_64-4.0.4.tgz
mv mongodb-linux-x86_64-4.0.4 mongodb
```

##### 2. Setting Environment Variables

To simplify subsequent operations, please set the environment variables for MongoDB:

```
export MONGOPATH=/home/java-tron/mongodb/
export PATH=$PATH:$MONGOPATH/bin
```

##### 3. Configuring MongoDB

Create the log and data directories for MongoDB and create the configuration file `mgdb.conf`:

```
mkdir -p /home/java-tron/mongodb/{log,data}
cd /home/java-tron/mongodb/log/ && touch mongodb.log && cd -
vim /home/java-tron/mongodb/mgdb.conf
```

Write the following content into the `mgdb.conf` file. Ensure that `dbpath` and `logpath` use absolute paths:

```text
dbpath=/home/java-tron/mongodb/data
logpath=/home/java-tron/mongodb/log/mongodb.log
port=27017
logappend=true
fork=true
bind_ip=0.0.0.0
auth=true
wiredTigerCacheSizeGB=2
```

Important Configuration Notes:

  * `bind_ip=0.0.0.0`: Must be configured to `0.0.0.0`; otherwise, remote connections will be rejected.
  * `wiredTigerCacheSizeGB`: This parameter must be configured to prevent Out Of Memory (OOM) issues.

##### 4. Starting MongoDB

Start the MongoDB service using the configuration file:

```
mongod --config /home/java-tron/mongodb/mgdb.conf &
```

##### 5. Creating Admin and Database Users

Connect to MongoDB to create an administrative user, then create the database and user for the event subscription service:

```
mongo
use admin
db.createUser({user:"<admin-username>",pwd:"<admin-password>",roles:[{role:"root",db:"admin"}]})

db.auth("<admin-username>", "<admin-password>")
use eventlog
db.createUser({user:"<eventlog-username>",pwd:"<eventlog-password>",roles:[{role:"dbOwner",db:"eventlog"}]})
```


#### Deploying the Event Query Service

The Event Query Service provides an HTTP interface for querying event data stored in MongoDB. This service requires a Java environment.

**Note**: Please ensure you are using **Oracle JDK 8**, not Open JDK 8.

##### 1. Downloading the Source Code

Clone the `tron-eventquery` project source code:

```
git clone https://github.com/tronprotocol/tron-eventquery.git
cd tron-eventquery
```

##### 2. Building the Service

Download and use Maven to build the `tron-eventquery` service:

```
wget https://mirrors.cnnic.cn/apache/maven/maven-3/3.5.4/binaries/apache-maven-3.5.4-bin.tar.gz --no-check-certificate
tar zxvf apache-maven-3.5.4-bin.tar.gz
export M2_HOME=$HOME/maven/apache-maven-3.5.4
export PATH=$PATH:$M2_HOME/bin
mvn --version
mvn package
```

Upon successful execution, a JAR package will be generated in the `tron-eventquery/target` directory, and a `config.conf` file will be created in the `tron-eventquery/` directory. An example of the configuration file content is shown below:

```text
mongo.host=IP
mongo.port=27017
mongo.dbname=eventlog
mongo.username=tron
mongo.password=123456
mongo.connectionsPerHost=8
mongo.threadsAllowedToBlockForConnectionMultiplier=4
```

Please modify `mongo.host`, `mongo.port`, `mongo.dbname`, `mongo.username`, and `mongo.password` according to your MongoDB configuration.

##### 3. Starting the TRON Event Query Service

Start the `tron-eventquery` service and insert the indexes:

```
sh deploy.sh
sh insertIndex.sh
```

**Note**: The default port is `8080`. To change it, edit the `deploy.sh` script. For example:

```
nohup java -jar -Dserver.port=8081 target/troneventquery-1.0.0-SNAPSHOT.jar 2>&1 &
```


#### Launch and Verification

After completing the deployment steps, you can start the TRON FullNode and verify that the event subscription service is working correctly.

##### 1. Starting the FullNode

**Important**: Before starting the FullNode, ensure that the MongoDB service has been started successfully.

The command to start the FullNode is as follows:

```
java -jar FullNode.jar -c config.conf --es
```

For information on installing a FullNode, please refer to the [Deploying a FullNode](https://tronprotocol.github.io/documentation-en/using_javatron/installing_javatron/) documentation.

##### 2. Verifying Plugin Load

You can verify that the event plugin has loaded successfully by checking the FullNode logs:

```
tail -f logs/tron.log | grep -i eventplugin
```

If you see a message similar to the following, the plugin has loaded successfully:

```text
o.t.c.l.EventPluginLoader 'your plugin path/plugin-kafka-1.0.0.zip' loaded
```

##### 3. Verifying Data Persistence in MongoDB

Connect to MongoDB and query the data to verify that event data has been captured from the node and stored in the database via the event subscription:

```
mongo 47.90.245.68:27017
use eventlog
db.auth("tron", "123456")
show collections
db.block.find()
```

If data is returned, it means the data has been stored successfully. Otherwise, please review the FullNode logs to troubleshoot the issue.


#### Using the TRON Event Query Service API

The TRON Event Query Service provides a series of HTTP API endpoints for querying event data stored in MongoDB. For details on the specific APIs and their usage, please refer to the [Event Query Service HTTP API documentation](https://github.com/tronprotocol/tron-eventquery?tab=readme-ov-file#main-http-service).



## Built-in Message Queue Subscription (ZeroMQ)

The java-tron node includes a built-in **ZeroMQ** message queue that provides a lightweight event streaming service. This method requires no external plugins and is ideal for use cases that demand high real-time event delivery but do not require event persistence or historical replay, such as rapid prototyping and testing.

This method has the following advantages:

  - **No Plugin Deployment**: Subscriptions are established by connecting directly to a TRON node.
  - **Low Latency**: Optimized for real-time event streaming.
  - **Lightweight**: Well-suited for rapid development and testing environments.

Therefore, when you want to connect to an event stream quickly and at a minimal cost without relying on persistence capabilities, using the **built-in ZeroMQ message queue** is a more lightweight and direct choice. This guide explains how to subscribe to events using this method.

### Configuring the Node

To enable event subscriptions via java-tron's built-in ZeroMQ, you must enable the feature in the node's configuration file.

```
event.subscribe = {
  native = {
    useNativeQueue = true  
    bindport = 5555  
    sendqueuelength = 1000  
  }

  ......
 
  topics = [
    {
      triggerName = "block"  
      enable = true
      topic = "block"  
    },
    ......
  ]
}
```

  * `native.useNativeQueue`: `true` to use the built-in message queue, `false` to use event plugins.
  * `native.bindport`: The port that the ZeroMQ publisher binds to. In this example, it is `5555`, so the subscriber should connect to the publisher address `"tcp://127.0.0.1:5555"`.
  * `native.sendqueuelength`: The length of the send queue. This is the maximum number of messages the TCP buffer can hold if the subscriber is slow to receive them. Messages published beyond this limit will be discarded.
  * `topics`: The subscribed [Event Types](#event-types), such as block types, transaction types, etc.

### Starting the Node

The event subscription service is disabled by default and must be enabled using the `--es` command-line argument. The startup command for a node with event subscription enabled is as follows:

```
$ java -jar FullNode.jar --es
```

### Preparing the Event Subscription Script

This guide uses Node.js as an example to demonstrate how to subscribe to events.

First, install the `ZeroMQ` library:

```
$ npm install zeromq@5
```

Next, write the subscriber code:

```
// subscriber.js
var zmq = require("zeromq"),
var sock = zmq.socket("sub");

sock.connect("tcp://127.0.0.1:5555");
sock.subscribe("block");
console.log("Subscriber connected to port 5555");

sock.on("message", function(topic, message) {
  console.log(
    "received a message related to:",
    Buffer.from(topic).toString(),
    ", containing message:",
    Buffer.from(message).toString()
  );
});
```

This example connects the subscriber to the node's event publisher and subscribes to `block` events.

### Starting the Subscriber

The Node.js startup command is as follows:

```
$ node subscriber.js

> Subscriber connected to port 5555
```

When the node produces a new block, the subscriber will receive the block event, and the output will look like this:

```
received a message related to: block, containing message: {"timeStamp":1678343709000,"triggerName":"blockTrigger","blockNumber":1361,"blockHash":"00000000000005519b3995cd638753a862c812d1bda11de14bbfaa5ad3383280","transactionSize":0,"latestSolidifiedBlockNumber":1361,"transactionList":[]}
received a message related to: block, containing message: {"timeStamp":1678343712000,"triggerName":"blockTrigger","blockNumber":1362,"blockHash":"0000000000000552d53d1bdd9929e4533a983f14df8931ee9b3bf6d6c74a47b0","transactionSize":0,"latestSolidifiedBlockNumber":1362,"transactionList":[]}
```
