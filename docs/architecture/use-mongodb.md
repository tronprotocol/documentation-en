# TRON MongoDB Plugin: Deployment and Usage

This guide is designed to help developers quickly deploy and use the TRON MongoDB event subscription plugin to achieve real-time data capture, persistent storage, and querying of on-chain events. The document covers the entire process, including system environment configuration, plugin deployment, database installation, query service setup, and API usage.

The main steps include:

- [Checking System Configuration](#1)
- [Understanding the System Architecture](#2)
- [Deploying the Event Plugin](#3)
- [Deploying the MongoDB](#4)
- [Deploying the Event Query Service](#5)
- [Starting and Verifing](#6)
- [Using the TRON Event Query Service API](#7)

<a id="1"></a>
## Recommended System Configuration

To ensure the efficient and stable operation of your TRON node and event service, the following configuration is recommended:

  * **CPU**: 16 cores or more
  * **RAM**: 32 GB or higher
  * **SSD**: 2.5 TB or more
  * **Operating System**: Linux or macOS


<a id="2"></a>
## System Architecture and Workflow

The TRON MongoDB event subscription system consists of three core modules:

1.  **Event Subscription Plugin**: Connects to a TRON node to capture event data and writes it to MongoDB.
2.  **MongoDB Database**: The persistence layer for storing event data.
3.  **Event Query Service**: Provides an HTTP API for external applications to query event data.


<a id="3"></a>
## Deploying the Event Subscription Plugin

### 3.1 Building the Plugin

```
git clone https://github.com/tronprotocol/event-plugin.git
cd event-plugin
./gradlew build
```

After the build is complete, the generated plugin file will be located at:

```
event-plugin/build/plugins/plugin-mongodb-*.zip
```

### 3.2 Configuring the FullNode 

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
  * `topics`: Seven event types are currently supported: `block`, `transaction`, `contractevent`, `contractlog`, `solidity`, `solidityevent`, and `soliditylog`. For more details, please refer to the [Event Types](../event/#event-types) chapter.
      * `triggerName`: The name of the trigger, which cannot be modified.
      * `enable`: Toggles the event subscription. `true` enables it, `false` disables it.
      * `topic`: The name of the collection in MongoDB that will receive the events. This can be modified.
  * `filter`: The criteria for filtering events.
      * `fromblock`: The starting block number of the query range. Can be `""`, `"earliest"` (to query from the genesis block), or a specific block number.
      * `toblock`: The ending block number of the query range. Can be `""`, `"latest"` (the most recent block), or a specific block number.
      * `contractAddress`: A list of contract addresses you wish to subscribe to. If set to an empty string, logs/events from all contract addresses will be received.
      * `contractTopic`: A list of contract topics you wish to subscribe to. If set to an empty string, logs/events for all contract topics will be received.

<a id="4"></a>
## Installing and Configuring MongoDB

MongoDB will be used to store TRON event data. Please follow these steps to install and configure it:

### 4.1 Installing MongoDB

First, create an installation directory for MongoDB, then download and extract the installation package:

```
mkdir /home/java-tron
cd /home/java-tron
curl -O https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-4.0.4.tgz
tar zxvf mongodb-linux-x86_64-4.0.4.tgz
mv mongodb-linux-x86_64-4.0.4 mongodb
```

### 4.2 Setting Environment Variables

To simplify subsequent operations, please set the environment variables for MongoDB:

```
export MONGOPATH=/home/java-tron/mongodb/
export PATH=$PATH:$MONGOPATH/bin
```

### 4.3 Configuring MongoDB

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

**Important Configuration Notes**:

  * `bind_ip=0.0.0.0`: Must be configured to `0.0.0.0`; otherwise, remote connections will be rejected.
  * `wiredTigerCacheSizeGB`: This parameter must be configured to prevent Out Of Memory (OOM) issues.

### 4.4 Starting MongoDB

Start the MongoDB service using the configuration file:

```
mongod --config /home/java-tron/mongodb/mgdb.conf &
```

### 4.5 Creating Admin and Database Users

Connect to MongoDB to create an administrative user, then create the database and user for the event subscription service:

```
mongo
use admin
db.createUser({user:"<admin-username>",pwd:"<admin-password>",roles:[{role:"root",db:"admin"}]})

db.auth("<admin-username>", "<admin-password>")
use eventlog
db.createUser({user:"<eventlog-username>",pwd:"<eventlog-password>",roles:[{role:"dbOwner",db:"eventlog"}]})
```

<a id="5"></a>
## Deploying the Event Query Service

The Event Query Service provides an HTTP interface for querying event data stored in MongoDB. This service requires a Java environment.

**Note**: Please ensure you are using **Oracle JDK 8**, not Open JDK 8.

### 5.1 Downloading the Source Code

Clone the `tron-eventquery` project source code:

```
git clone https://github.com/tronprotocol/tron-eventquery.git
cd tron-eventquery
```

### 5.2 Building the Service

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

### 5.3 Starting the TRON Event Query Service

Start the `tron-eventquery` service and insert the indexes:

```
sh deploy.sh
sh insertIndex.sh
```

**Note**: The default port is `8080`. To change it, edit the `deploy.sh` script. For example:

```
nohup java -jar -Dserver.port=8081 target/troneventquery-1.0.0-SNAPSHOT.jar 2>&1 &
```

<a id="6"></a>
## Launch and Verification

After completing the deployment steps, you can start the TRON FullNode and verify that the event subscription service is working correctly.

### 6.1 Starting the FullNode

**Important**: Before starting the FullNode, ensure that the MongoDB service has been started successfully.

The command to start the FullNode is as follows:

```
java -jar FullNode.jar -c config.conf --es
```

For information on installing a FullNode, please refer to the [Deploying a FullNode](https://tronprotocol.github.io/documentation-en/using_javatron/installing_javatron/) documentation.

### 6.2 Verifying Plugin Load

You can verify that the event plugin has loaded successfully by checking the FullNode logs:

```
tail -f logs/tron.log | grep -i eventplugin
```

If you see a message similar to the following, the plugin has loaded successfully:

```text
o.t.c.l.EventPluginLoader 'your plugin path/plugin-kafka-1.0.0.zip' loaded
```

### 6.3 Verifying Data Persistence in MongoDB

Connect to MongoDB and query the data to verify that event data has been captured from the node and stored in the database via the event subscription:

```
mongo 47.90.245.68:27017
use eventlog
db.auth("tron", "123456")
show collections
db.block.find()
```

If data is returned, it means the data has been stored successfully. Otherwise, please review the FullNode logs to troubleshoot the issue.


<a id="7"></a>
## Using the TRON Event Query Service API

The TRON Event Query Service provides a series of HTTP API endpoints for querying event data stored in MongoDB. For details on the specific APIs and their usage, please refer to the [Event Query Service HTTP API documentation](https://github.com/tronprotocol/tron-eventquery?tab=readme-ov-file#main-http-service).