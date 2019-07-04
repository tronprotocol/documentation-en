## Premise
Create separate directories for fullnode and soliditynode
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
# Stop Node Gracefully
Create file stop.sh，use kill -15 to close java-tron.jar（or FullNode.jar、SolidityNode.jar）.
You need to modify pid=`ps -ef |grep java-tron.jar |grep -v grep |awk '{print $2}'` to find the correct pid.
```text
#!/bin/bash
while true; do
  pid=`ps -ef |grep java-tron.jar |grep -v grep |awk '{print $2}'`
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

## Advanced Configurations

Read the [Advanced Configuration](../advanced-configuration.md)
