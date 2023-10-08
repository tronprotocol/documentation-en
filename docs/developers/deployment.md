# Deployment

## Premise
Create separate directories for fullnode and soliditynode

> NOTE: SolidityNode is deprecated. Now a FullNode supports all RPCs of a SolidityNode.
> New developers should deploy FullNode only.

```text
/deploy/fullnode
/deploy/soliditynode
```

Create two folders for fullnode and soliditynode.

Clone the latest master branch of [https://github.com/tronprotocol/java-tron](https://github.com/tronprotocol/java-tron) and extract it to
```text
/deploy/java-tron
```

Make sure you have the proper dependencies.

* JDK 1.8 (JDK 1.9+ is not supported yet)
* On Linux Ubuntu system (e.g. Ubuntu 16.04.4 LTS), ensure that the machine has [__Oracle JDK 8__](https://www.digitalocean.com/community/tutorials/how-to-install-java-with-apt-get-on-ubuntu-16-04), instead of having __Open JDK 8__ in the system. If you are building the source code by using __Open JDK 8__, you will get [__Build Failed__](https://github.com/tronprotocol/java-tron/issues/337) result.
* Open **UDP** ports for connection to the network
* **MINIMUM** 2 CPU Cores


## Deployment Guide

1.&nbsp;Build the java-tron project
```text
cd /deploy/java-tron
./gradlew build
```

2.&nbsp;Copy the FullNode.jar and SolidityNode.jar along with configuration files into the respective directories
```text
download your needed configuration file from https://github.com/tronprotocol/TronDeployment.

main_net_config.conf is the configuration for MainNet, and test_net_config.conf is the configuration for TestNet.

please rename the configuration file to `config.conf` and use this config.conf to start FullNode and SoliditNode.

cp build/libs/FullNode.jar ../fullnode

cp build/libs/SolidityNode.jar ../soliditynode
```

3.&nbsp;You can now run your FullNode using the following command
```text
java -jar FullNode.jar -c config.conf // make sure that your config.conf is downloaded from https://github.com/tronprotocol/TronDeployment
```

4.&nbsp;Configure the SolidityNode configuration file

You need to edit `config.conf` to connect to your local FullNode. Change  `trustNode` in `node` to local `127.0.0.1:50051`, which is the default rpc port. Set `listen.port` to any number within the range of 1024-65535. Please don't use any ports between 0-1024 since you'll most likely hit conflicts with other system services. Also change `rpc port` to `50052` or something to avoid conflicts. **Please forward the UDP port 18888 for FullNode.**
```text
rpc {
      port = 50052
    }
```

5.&nbsp;You can now run your SolidityNode using the following command：
```text
java -jar SolidityNode.jar -c config.conf //make sure that your config.conf is downloaded from https://github.com/tronprotocol/TronDeployment
```

6.&nbsp;Running a Super Representative Node for mainnet
```text
java -jar FullNode.jar -p your private key --witness -c your config.conf(Example：/data/java-tron/config.conf)
Example:
java -jar FullNode.jar -p 650950B193DDDDB35B6E48912DD28F7AB0E7140C1BFDEFD493348F02295BD812 --witness -c /data/java-tron/config.conf
```

This is similar to running a private testnet, except that the IPs in the `config.conf` are officially declared by TRON.

7.&nbsp;Running a Super Representative Node for private testnet

You should modify the config.conf:

- Replace existing entry in genesis.block.witnesses with your address
- Replace existing entry in seed.node ip.list with your ip list
- The first Super Node start, needSyncCheck should be set false
- Set p2pversion to 61

```text
cd build/libs
java -jar FullNode.jar -p your private key --witness -c your config.conf (Example：/data/java-tron/config.conf)
Example:
java -jar FullNode.jar -p 650950B193DDDDB35B6E48912DD28F7AB0E7140C1BFDEFD493348F02295BD812 --witness -c /data/java-tron/config.conf
```


## Logging and Network Connection Verification

Logs for both nodes are located in `/deploy/\*/logs/tron.log`. Use `tail -f /logs/tron.log/` to follow along with the block syncing.

You should see something similar to this in your logs for block synchronization:

**FullNode**
```text
12:00:57.658 INFO  [pool-7-thread-1] [o.t.c.n.n.NodeImpl](NodeImpl.java:830) Success handle block Num:236610,ID:0000000000039c427569efa27cc2493c1fff243cc1515aa6665c617c45d2e1bf
```
**SolidityNode**
```text
12:00:40.691 INFO  [pool-17-thread-1] [o.t.p.SolidityNode](SolidityNode.java:88) sync solidity block, lastSolidityBlockNum:209671, remoteLastSolidityBlockNum:211823
```
## Stop Node Gracefully
Create file stop.sh，use kill -15 to close FullNode.jar(or SolidityNode.jar).
You need to modify pid=`ps -ef |grep FullNode.jar |grep -v grep |awk '{print $2}'` to find the correct pid.
```text
#!/bin/bash
while true; do
  pid=`ps -ef |grep FullNode.jar |grep -v grep |awk '{print $2}'`
  if [ -n "$pid" ]; then
    kill -15 $pid
    echo "The java-tron process is exiting, it may take some time, forcing the exit may cause damage to the database, please wait patiently..."
    sleep 1
  else
    echo "java-tron killed successfully!"
    break
  fi
done
```

## FullNode and SolidityNode Fast Deployment

Download fast deployment script, run the script according to different types of node.

<h3>Scope of use</h3>

This script could be used on Linux/MacOS, but not on Windows.
Just Support FullNode and SolidityNode.

<h3>Download and run script</h3>

```shell
wget https://raw.githubusercontent.com/tronprotocol/TronDeployment/master/deploy_tron.sh -O deploy_tron.sh
```

<h3>Parameter Illustration</h3>

```shell
bash deploy_tron.sh --app [FullNode|SolidityNode] --net [mainnet|testnet|privatenet] --db [keep|remove|backup] --heap-size <heapsize>

--app Optional, Running application. The default node is Fullnode and it could be FullNode or SolidityNode.
--net Optional, Connecting network. The default network is mainnet and it could be mainnet, testnet.
--db  Optional, The way of data processing could be keep, remove and backup. Default is keep. If you launch two different networks, like from mainnet to testnet or from testnet to mainnet, you need to delete database.
--trust-node  Optional, It only works when deploying SolidityNode. Default is 127.0.0.1:50051. The specified gRPC service of Fullnode, like 127.0.0.1:50051 or 13.125.249.129:50051.
--rpc-port  Optional, Port of grpc. Default is 50051. If you deploy SolidityNode and FullNode on the same host，you need to configure different ports.
--commit  Optional, commitid of project.
--branch  Optional, branch of project.  Mainnet default is latest release and Testnet default is master.
--heap-size  Optional, jvm option: Xmx. The default heap-size is 0.8 * memory size.
--work_space  Optional, default is current directory.
```

<h3> Deployment of FullNode on the one host </h3>

```shell
wget https://raw.githubusercontent.com/tronprotocol/TronDeployment/master/deploy_tron.sh -O deploy_tron.sh
bash deploy_tron.sh
```

<h3> Deployment of SolidityNode on the one host </h3>

```shell
wget https://raw.githubusercontent.com/tronprotocol/TronDeployment/master/deploy_tron.sh -O deploy_tron.sh
# User can self-configure the IP and Port of GRPC service in the turst-node field of SolidityNode. trust-node is the fullnode you just deploy.
bash deploy_tron.sh --app SolidityNode --trust-node <grpc-ip:grpc-port>
```

<h3> Deployment of FullNode and SolidityNode on the same host </h3>

```shell
# You need to configure different gRPC ports on the same host because gRPC port is available on SolidityNode and FullNodeConfigure and it cannot be set as default value 50051. In this case the default value of rpc port is set as 50041.
wget https://raw.githubusercontent.com/tronprotocol/TronDeployment/master/deploy_tron.sh -O deploy_tron.sh
bash deploy_tron.sh --app FullNode
bash deploy_tron.sh --app SolidityNode --rpc-port 50041
```

## Grpc Gateway Deployment

<h3> Summary </h3>

This script helps you download the code from https://github.com/tronprotocol/grpc-gateway and deploy the code on your environment.

<h3> Pre-requests </h3>

Please follow the guide on https://github.com/tronprotocol/grpc-gateway
Install Golang, Protoc, and set $GOPATH environment variable according to your requirement.

<h3> Download and run script </h3>

```shell
wget https://raw.githubusercontent.com/tronprotocol/TronDeployment/master/deploy_grpc_gateway.sh -O deploy_grpc_gateway.sh
```

<h3> Parameter Illustration </h3>

```shell
bash deploy_grpc_gateway.sh --rpchost [rpc host ip] --rpcport [rpc port number] --httpport [http port number]

--rpchost The fullnode or soliditynode IP where the grpc service is provided. Default value is "localhost".
--rpcport The fullnode or soliditynode port number grpc service is consuming. Default value is 50051.
--httpport The port intends to provide http service provided by grpc gateway. Default value is 18890.
```

<h3> Example </h3>

Use default configuration：
```shell
bash deploy_grpc_gateway.sh
```
Use customized configuration：
```shell
bash deploy_grpc_gateway.sh --rpchost 127.0.0.1 --rpcport 50052 --httpport 18891
```

## Event Subscribe plugin Deployment

This is an implementation of Tron eventsubscribe model.

* **api** module defines IPluginEventListener, a protocol between Java-tron and event plugin.
* **app** module is an example for loading plugin, developers could use it for debugging.
* **kafkaplugin** module is the implementation for kafka, it implements IPluginEventListener, it receives events subscribed from Java-tron and relay events to kafka server.
* **mongodbplugin** mongodbplugin module is the implementation for mongodb.

<h3> Setup/Build </h3>

1. Clone the repo `git clone https://github.com/tronprotocol/event-plugin.git`
2. Go to eventplugin `cd event-plugin`
3. run `./gradlew build`

* This will produce one plugin zip, named `plugin-kafka-1.0.0.zip`, located in the `event-plugin/build/plugins/` directory.


<h3> Edit **config.conf** of Java-tron， add the following fileds:</h3>

```
event.subscribe = {
    path = "" // absolute path of plugin
    server = "" // target server address to receive event triggers
    dbconfig="" // dbname|username|password
    topics = [
        {
          triggerName = "block" // block trigger, the value can't be modified
          enable = false
          topic = "block" // plugin topic, the value could be modified
        },
        {
          triggerName = "transaction"
          enable = false
          topic = "transaction"
        },
        {
          triggerName = "contractevent"
          enable = true
          topic = "contractevent"
        },
        {
          triggerName = "contractlog"
          enable = true
          topic = "contractlog"
        }
    ]

    filter = {
       fromblock = "" // the value could be "", "earliest" or a specified block number as the beginning of the queried range
       toblock = "" // the value could be "", "latest" or a specified block number as end of the queried range
       contractAddress = [
           "" // contract address you want to subscribe, if it's set to "", you will receive contract logs/events with any contract address.
       ]

       contractTopic = [
           "" // contract topic you want to subscribe, if it's set to "", you will receive contract logs/events with any contract topic.
       ]
    }
}


```
 * **path**: is the absolute path of "plugin-kafka-1.0.0.zip"
 * **server**: Kafka server address
 * **topics**: each event type maps to one Kafka topic, we support four event types subscribing, block, transaction, contractlog and contractevent.
 * **dbconfig**: db configuration information for mongodb, if using kafka, delete this one; if using Mongodb, add like that dbname|username|password
 * **triggerName**: the trigger type, the value can't be modified.
 * **enable**: plugin can receive nothing if the value is false.
 * **topic**: the value is the kafka topic to receive events. Make sure it has been created and Kafka process is running
 * **filter**: filter condition for process trigger.
 **note**: if the server is not 127.0.0.1, pls set some properties in config/server.properties file
           remove comment and set listeners=PLAINTEXT://:9092
           remove comment and set advertised.listeners to PLAINTEXT://host_ip:9092

<h3 id="kafka"> Install Kafka </h3>

**On Mac**:
```
brew install kafka
```

**On Linux**:
```
cd /usr/local
wget http://archive.apache.org/dist/kafka/0.10.2.2/kafka_2.10-0.10.2.2.tgz
tar -xzvf kafka_2.10-0.10.2.2.tgz
mv kafka_2.10-0.10.2.2 kafka

add "export PATH=$PATH:/usr/local/kafka/bin" to end of /etc/profile
source /etc/profile


kafka-server-start.sh /usr/local/kafka/config/server.properties &

```
**Note**: make sure the version of Kafka is the same as the version set in build.gradle of eventplugin project.(kafka_2.10-0.10.2.2 kafka)

<h3> Run Kafka </h3>

**On Mac**:
```
zookeeper-server-start /usr/local/etc/kafka/zookeeper.properties & kafka-server-start /usr/local/etc/kafka/server.properties
```

**On Linux**:
```
zookeeper-server-start.sh /usr/local/kafka/config/zookeeper.properties &
Sleep about 3 seconds
kafka-server-start.sh /usr/local/kafka/config/server.properties &
```

<h3> Create topics to receive events, the topic is defined in config.conf </h3>

**On Mac**:
```
kafka-topics --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic block
kafka-topics --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic transaction
kafka-topics --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic contractlog
kafka-topics --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic contractevent
```

**On Linux**:
```
kafka-topics.sh  --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic block
kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic transaction
kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic contractlog
kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic contractevent
```

<h3> Kafka consumer </h3>

**On Mac**:
```
kafka-console-consumer --bootstrap-server localhost:9092  --topic block
kafka-console-consumer --bootstrap-server localhost:9092  --topic transaction
kafka-console-consumer --bootstrap-server localhost:9092  --topic contractlog
kafka-console-consumer --bootstrap-server localhost:9092  --topic contractevent
```

**On Linux**:
```
kafka-console-consumer.sh --zookeeper localhost:2181 --topic block
kafka-console-consumer.sh --zookeeper localhost:2181 --topic transaction
kafka-console-consumer.sh --zookeeper localhost:2181 --topic contractlog
kafka-console-consumer.sh --zookeeper localhost:2181 --topic contractevent
```

<h3> Load plugin in Java-tron </h3>

* add --es to command line, for example:
```
 java -jar FullNode.jar -p privatekey -c config.conf --es
```


<h3> Event filter </h3>

which is defined in config.conf, path: event.subscribe
```
filter = {
       fromblock = "" // the value could be "", "earliest" or a specified block number as the beginning of the queried range
       toblock = "" // the value could be "", "latest" or a specified block number as end of the queried range
       contractAddress = [
           "TVkNuE1BYxECWq85d8UR9zsv6WppBns9iH" // contract address you want to subscribe, if it's set to "", you will receive contract logs/events with any contract address.
       ]

       contractTopic = [
           "f0f1e23ddce8a520eaa7502e02fa767cb24152e9a86a4bf02529637c4e57504b" // contract topic you want to subscribe, if it's set to "", you will receive contract logs/events with any contract topic.
       ]
    }
```


<h3 id="mongo"> Download and install MongoDB </h3>

** Suggested Configuration **

- CPU/ RAM: 16Core / 32G
- DISK: 500G
- System: CentOS 64

The version of MongoDB is **4.0.4**, below is the command:

- cd /home/java-tron
- curl -O https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-4.0.4.tgz
- tar zxvf mongodb-linux-x86_64-4.0.4.tgz
- mv mongodb-linux-x86_64-4.0.4 mongodb

** Set environment **
- export MONGOPATH=/home/java-tron/mongodb/
- export PATH=$PATH:$MONGOPATH/bin

** Create mongodb config **
The path is : /etc/mongodb/mgdb.conf

- cd /etc/mongodb
- touch mgdb.conf

Create data&log folder for mongodb
Create data, log subfolder in mongodb directory,  and add their absolute path to mgdb.conf

** Example: **

- dbpath=/home/java-tron/mongodb/data
- logpath=/home/java-tron/mongodb/log/mongodb.log
- port=27017
- logappend=true
- fork=true
- bind_ip=0.0.0.0
- auth=true
- wiredTigerCacheSizeGB=2

** Note: **
- bind_ip must be configured to 0.0.0.0，otherwise remote connection will be refused.
- wiredTigerCacheSizeGB, must be configured to prevent OOM

** Launch MongoDB **
  - mongod  --config /etc/mongodb/mgdb.conf

** Create admin account: **
- mongo
- use admin
- db.createUser({user:"root",pwd:"admin",roles:[{role:"root",db:"admin"}]})

** Create eventlog and its owner account **

- db.auth("root", "admin")
- use eventlog
- db.createUser({user:"tron",pwd:"123456",roles:[{role:"dbOwner",db:"eventlog"}]})

> database: eventlog, username:tron, password: 123456

** Firewall rule: **
- iptables -A INPUT -p tcp -m state --state NEW -m tcp --dport 27017 -j ACCEPT

** Remote connection via mongo: **

- mongo 47.90.245.68:27017
- use eventlog
- db.auth("tron", "123456")
- show collections
- db.block.find()

** Query block trigger data: **

-  db.block.find({blockNumber: {$lt: 1000}});  // return records whose blockNumber less than1000

** Set database index to speedup query: **

cd /{projectPath}
sh insertIndex.sh

## Event query service deployment

<h3>Download sourcecode</h3>

Download sourcecode

git clone https://github.com/tronprotocol/tron-eventquery.git
cd troneventquery

<h3> Build </h3>

- mvn package

After the build command is executed successfully, troneventquery jar to release will be generated under troneventquery/target directory.

Configuration of mongodb "config.conf" should be created for storing mongodb configuration, such as database name, username, password, and so on. We provided an example in sourcecode, which is " troneventquery/config.conf ". Replace with your specified configuration if needed.

**Note**:

Make sure the relative path of config.conf and troneventquery jar. The config.conf 's path is the parent of troneventquery jar.

 - mongo.host=IP
 - mongo.port=27017
 - mongo.dbname=eventlog
 - mongo.username=tron
 - mongo.password=123456
 - mongo.connectionsPerHost=8
 - mongo.threadsAllowedToBlockForConnectionMultiplier=4

Any configuration could be modified except **mongo.dbname**, "**eventlog**" is the specified database name for event subscribe.

<h3> Run </h3>

- troneventquery/deploy.sh is used to deploy troneventquery
- troneventquery/insertIndex.sh is used to setup mongodb index to speedup query.


## Advanced Configurations

Read the [Advanced Configuration](./advanced-configuration.md)
