
## TRON Network Instructure

TRON network uses Peer-to-Peer(P2P) network instructure, all nodes status equal. There are three types of node: SuperNode, FullNode, SolidityNode. SuperNode produces blocks, FullNode synchronizes blocks and broadcasts transactions, SolidityNode synchronizes solidified blocks. Any device that deploy the java-tron code can join TRON network as a node.
![image](https://raw.githubusercontent.com/tronprotocol/documentation-EN/master/imags/network.png)


<h3>SuperNode</h3>

Super Representative(abbr: SR) is the block producer in TRON network, there are 27 SR. They verify the transactions and write the transactions into the blocks, they take turns to produce blocks. The super Representatives' information is public to everyone in TRON network. The best way to browse is using [tronscan](https://tronscan.org/#/sr/representatives).

Recommended Hardware Configuration:  
minimum requirement:  
CPU: 16 cores, RAM: 32G, Bandwidth: 100M, Disk: 1T  
Recommended requirement:  
CPU: > 64 cores RAM: > 64G, Bandwidth: > 500M, Disk: > 20T

<h3>FullNode</h3> 

FullNode has the complete block chain data, can update data in real time. It can broadcast the transactions and provide api service.

Recommended Hardware Configuration:  
minimum requirement:     
CPU: 16 cores, RAM: 32G, Bandwidth: 100M, Disk: 1T   
Recommended requirement:  
CPU: > 64 cores RAM: > 64G, Bandwidth: > 500M, Disk: > 20T

<h3>SolidityNode</h3>

SolidityNode only synchronize solidified blocks data from the fullNode it specifies, It also provie api service.  

Recommended Hardware Configuration:  
minimum requirement:    
CPU: 16 cores, RAM: 32G, Bandwidth: 100M, Disk: 1T   
Recommended requirement:  
CPU: > 64 cores RAM: > 64G, Bandwidth: > 500M, Disk: > 20T


## MainNet, TestNet, PrivateNet

MainNet, TestNet, PrivateNet all use the same code, only the node start configuration varies.  

<h3>1. MainNet </h3>

[MainNet configuration](https://github.com/tronprotocol/tron-deployment/blob/master/main_net_config.conf)  

<h3>2. TestNet </h3>

[TestNet configuration](https://github.com/tronprotocol/tron-deployment/blob/master/test_net_config.conf)  

<h3>3. PrivateNet </h3>

<h4>3.1 Preconditions </h4>

- at least two accounts [generate an account](https://tronscan.org/#/wallet/new)  
- at least deploy one SuperNode to produce blocks  
- deploy serval FullNodes to synchronize blocks and broadcast transactions  
- SuperNode and FullNode comprise the private network  

<h5>3.2 Deployment </h5>

<h6>3.2.1 Step 1: SuperNode Deployment </h6>

 1.&nbsp;download private_net_config.conf  

```text
wget https://github.com/tronprotocol/tron-deployment/blob/master/private_net_config.conf
```
 2.&nbsp;add your private key in localwitness  
 3.&nbsp;set genesis.block.witnesses as the private key's corresponding address  
 4.&nbsp;set p2p.version, any positive integer but 11111  
 5.&nbsp;set the first SR needSyncCheck = false, others can be set true  
 6.&nbsp;set node.discovery.enable = true  
 7.&nbsp;run the script  

```text
nohup java -Xmx6g -XX:+HeapDumpOnOutOfMemoryError -jar FullNode.jar  --witness  -c private_net_config.conf

command line parameters introduction:  
--witness: start witness function, i.e.: --witness  
--log-config: specify the log configuration file path, i.e.: --log-config logback.xml  
-c: specify the configuration file path, i.e.: -c config.conf 
```
 
 The usage of the log file:  
 You can change the level of the module to control the log output. The default level of each module is INFO, for example: only print the message with the level higher than warn:  
 <logger name="net" level="WARN"/>
 The parameters in configuration file that need to modify:  
 localwitness:  
 ![image](https://raw.githubusercontent.com/tronprotocol/documentation-EN/master/imags/localwitness.jpg)  
 witnesses:  
 ![image](https://raw.githubusercontent.com/tronprotocol/documentation-EN/master/imags/witness.png)  
 version:  
 ![image](https://raw.githubusercontent.com/tronprotocol/documentation-EN/master/imags/p2p_version.png)  
 enable:  
 ![image](https://raw.githubusercontent.com/tronprotocol/documentation-EN/master/imags/discovery_enable.png)  


<h6>3.2.2 Step 2: FullNode Deployment </h6>
 1.&nbsp;Download private_net_config.conf  

```text
wget https://github.com/tronprotocol/tron-deployment/blob/master/private_net_config.conf 
```
 2.&nbsp;set seed.node ip.list with SR's ip and port  
 3.&nbsp;set p2p.version the same as SuperNode's p2p.version   
 4.&nbsp;set genesis.block the same as genesis.block  
 5.&nbsp;set needSyncCheck true   
 6.&nbsp;set node.discovery.enable true   
 7.&nbsp;run the script  

```text
 nohup java -Xmx6g -XX:+HeapDumpOnOutOfMemoryError -jar FullNode.jar  --witness  -c private_net_config.conf

 command lines parameters  
 --witness: start witness function，i.e.: --witness  
 --log-config: specify the log configuration file path, i.e.: --log-config logback.xml  
 -c: specify the configuration file path, i.e.: -c config.conf
```

 The usage of the log file:  
 You can change the level of the module to control the log output. The default level of each module is INFO, for example: only print the message with the level higher than warn:  
 <logger name="net" level="WARN"/>
 The parameters in configuration file that need to modify:    
 ip.list:  
 ![image](https://raw.githubusercontent.com/tronprotocol/documentation-EN/master/imags/ip_list.png)  
 p2p.version:  
 ![image](https://raw.githubusercontent.com/tronprotocol/documentation-EN/master/imags/p2p_version.png)  
 genesis.block:  
 ![image](https://raw.githubusercontent.com/tronprotocol/documentation-EN/master/imags/genesis_block.png)  
 needSyncCheck:  
 ![image](https://raw.githubusercontent.com/tronprotocol/documentation-EN/master/imags/need_sync_check.png)  
 node.discovery.enable:  
 ![image](https://raw.githubusercontent.com/tronprotocol/documentation-EN/master/imags/discovery_enable.png)  
 


