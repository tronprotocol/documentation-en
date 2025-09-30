# TRON Kafka Plugin: Deployment and Usage

This guide is designed to help developers efficiently use the Kafka event subscription plugin to listen for on-chain events on the TRON network. We will walk you through the entire process step-by-step, from environment setup to deployment, configuration, and final verification.

The main steps include:

- [Checking System Configuration](#1)
- [Compiling the Event Plugin](#2)
- [Deploying and Running Kafka](#3)
- [Configuring Event Subscription Rules](#4)
- [Creating the Kafka Subscription Topic](#5)
- [Starting the Event Subscription Node](#6)

<a id="1"></a>
## Recommended System Configuration

To ensure the stable operation of your TRON node and event subscription service, the following system configuration is recommended:

  * **CPU**: 16 cores or higher
  * **RAM**: 32 GB or higher
  * **SSD**: 2.5 TB or more of storage space
  * **Operating System**: Linux or macOS

<a id="2"></a>
## Compiling the Kafka Event Plugin

First, you need to clone the `event-plugin` project from its GitHub repository and compile it to generate the plugin's `.zip` file. Please follow these steps:

```
git clone https://github.com/tronprotocol/event-plugin.git
cd event-plugin
./gradlew build
```

After a successful compilation, you will find the generated `.zip` plugin file in the `event-plugin/build/plugins/` directory, for example, `plugin-kafka-1.0.0.zip`.


<a id="3"></a>
## Deploying and Running Kafka

### Step 1. Installing Kafka

In a Linux environment, please follow these steps to install Kafka:

```
cd /usr/local
wget https://downloads.apache.org/kafka/2.8.0/kafka_2.13-2.8.0.tgz
tar -xzf kafka_2.13-2.8.0.tgz
```

### Step 2: Running Kafka

In a Linux environment, please follow these steps to start the ZooKeeper and Kafka Broker services:

```shell
cd /usr/local/kafka_2.13-2.8.0
# Start the ZooKeeper service
bin/zookeeper-server-start.sh config/zookeeper.properties &
# Start the Kafka Broker service
bin/kafka-server-start.sh config/server.properties &
```

<a id="4"></a>
## Configuring Event Subscription

To support Kafka event subscriptions, you need to modify the Fullnode's configuration file (`config.conf`) by adding the `event.subscribe` section.

### Plugin Configuration Options

The following is an example of the `event.subscribe` configuration section:

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
  # ... other configuration options ...
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

### Configuring Event Subscription Type 

TRON event subscription supports 7 types of events: `block`, `transaction`, `contractevent`, `contractlog`, `solidity`, `solidityevent`, and `soliditylog`. Developers should configure these based on their application's specific needs. **We recommend subscribing to only 1-2 event types. Enabling too many triggers can lead to performance degradation.**

The following is an example configuration for subscribing to `block` events:

```
topics = [
  {
    triggerName = "block" 
    enable = true
    topic = "block" 
  }
]
```

  * `triggerName`: An internal field that cannot be changed.
  * `enable`: If set to `true`, enables the subscription to `block` events.
  * `topic`: The name of the corresponding topic in Kafka that will receive the events. You must create this topic in Kafka beforehand.

For more information on event subscription types, please refer to the [Event Types](../event#event-types) chapter.

### Configuring Event Filtering 

The `filter` field is used to filter subscribed events. You can specify a block range (`fromblock` - `toblock`), specific contract addresses (`contractAddress`), or specific contract topics (`contractTopic`) to provide developers with a more efficient and precise event subscription service.

```
filter = {
  fromblock = "" // The starting block number of the query range. Can be an empty string, "earliest", or a specific block number.
  toblock = "" // The ending block number of the query range. Can be an empty string, "latest", or a specific block number.
  contractAddress = [
    "" // The contract addresses you wish to subscribe to. If set to an empty string, logs/events from all contract addresses will be received.
  ]

  contractTopic = [
    "" // The contract topics you wish to subscribe to. If set to an empty string, logs/events for all contract topics will be received.
  ]
}
```

<a id="5"></a>
## Creating a Kafka Subscription Topic

The name of the Kafka subscription topic must match the `topic` setting in the `topics` field of your `event.subscribe` configuration. For example, if you need to subscribe to `block` events and set the `topic` field in the `block` trigger to `"block"`, you must create a topic named `"block"` in Kafka to receive block events.

In a Linux environment, the command to create a Kafka topic is as follows:

```
bin/kafka-topics.sh --create --topic block --bootstrap-server localhost:9092
```

<a id="6"></a>
## Starting the Event Subscription Node

After completing the above configuration, you must add the `--es` parameter when starting the FullNode to enable the event subscription feature.

```
java -jar FullNode.jar -c config.conf --es
```

### Verifying Plugin Load

You can verify that the Kafka event plugin has loaded successfully by checking the Fullnode logs:

```
grep -i eventplugin logs/tron.log
```

If you see a message similar to the following in the logs, the event subscription plugin has loaded successfully:

```
[o.t.c.l.EventPluginLoader] 'your plugin path/plugin-kafka-1.0.0.zip' loaded
```

### Verifying Event Subscription

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