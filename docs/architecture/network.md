# Tron Network Instructure

Tron network uses Peer-to-Peer(P2P) network instructure, all nodes status equal. There are three types of node: SuperNode, FullNode, SolidityNode. SuperNode produces blocks, FullNode synchronizes blocks and broadcasts transactions, SolidityNode synchronizes solidified blocks. Any device that deploy the java-tron code can join Tron network as a node.

![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/network.png)

## SuperNode

Super Representative(abbr: SR) is the block producer in TRON network, there are 27 SRs. They verify the transactions and write the transactions into the blocks in turn. The super Representatives' information is public to everyone in Tron network. The best way to browse is using [Tronscan](https://tronscan.org/#/sr/representatives).

Recommended Hardware Configuration:

```text
minimum requirement:
CPU: 16 cores, RAM: 32G, Bandwidth: 100M, Disk: 1T
Recommended requirement:
CPU: > 64 cores RAM: > 64G, Bandwidth: > 500M, Disk: > 2T
```

## FullNode

FullNode has the complete block chain data, can update data in real time. It can broadcast the transactions and provide api service.

Recommended Hardware Configuration:

```text
minimum requirement:
CPU: 16 cores, RAM: 32G, Bandwidth: 100M, Disk: 1T
Recommended requirement:
CPU: > 32 cores RAM: > 48G, Bandwidth: > 500M, Disk: > 2T
```

## SolidityNode

SolidityNode only synchronize solidified blocks data from the fullNode it specifies, It also provie api service.

> NOTE: SolidityNode is deprecated. Now a FullNode supports all RPCs of a SolidityNode.
> New developers should deploy FullNode only.

Recommended Hardware Configuration:

```text
minimum requirement:
CPU: 16 cores, RAM: 32G, Bandwidth: 100M, Disk: 1T
Recommended requirement:
CPU: > 32 cores RAM: > 48G, Bandwidth: > 500M, Disk: > 2T
```

## MainNet, TestNet and PrivateNet

MainNet, TestNet, PrivateNet all use the same code, only the node start configuration varies.

### MainNet

[MainNet configuration: main_net_config.conf](https://github.com/tronprotocol/tron-deployment/blob/master/main_net_config.conf)

### TestNet

[TestNet configuration: test_net_config.conf](https://github.com/tronprotocol/tron-deployment/blob/master/test_net_config.conf)

### PrivateNet

#### Preconditions

- at least two accounts [generate an account](https://tronscan.org/#/wallet/new)
- at least one SuperNode to produce blocks
- deploy serval FullNodes to synchronize blocks and broadcast transactions
- SuperNode and FullNode comprise the private network

#### Deploy the SuperNode

1. download private_net_config.conf

    ```console
    > wget https://raw.githubusercontent.com/tronprotocol/tron-deployment/master/private_net_config.conf
    ```

2. add your private key in `localwitness`
3. set `genesis.block.witnesses` as the private key's corresponding address
4. set `p2p.version`, any positive integer except `11111`
5. set for first SR `needSyncCheck = false`, others can be set true
6. set `node.discovery.enable = true`
7. run the following command

    ```text
    > nohup java -Xmx6g -XX:+HeapDumpOnOutOfMemoryError -jar FullNode.jar -c private_net_config.conf </dev/null &>/dev/null &

    command line parameters introduction:
    --witness: start witness function, i.e.: --witness YOUR_PRIVATE_KEY_IN_HEX
    --log-config: specify the log configuration file path, i.e.: --log-config logback.xml
    -c: specify the configuration file path, i.e.: -c config.conf
    ```

The usage of the log file:

You can change the level of the module to control the log output. The default level of each module is INFO, for example: only print the message with the level higher than warn:

```xml
<logger name="net" level="WARN"/>
```

The parameters in configuration file that need to modify:

localwitness:
> ![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/localwitness.jpg)

witnesses:
> ![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/witness.png)

version:
> ![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/p2p_version.png)

enable:
> ![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/discovery_enable.png)

#### Deploy the FullNode

Same as above except for:

1. set `seed.node.ip.list` to SR's ip and port
2. set `needSyncCheck` true
3. modify `listen.port`, `http.port` and `rpc.port` if SuperNode and FullNode are deployed on the same server.
4. do not need a private key in `localwitness`

The parameters in configuration file that need to modify:

ip.list:
> ![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/ip_list.png)

p2p.version:
> ![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/p2p_version.png)

genesis.block:
> ![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/genesis_block.png)

needSyncCheck:
> ![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/need_sync_check.png)

node.discovery.enable:
> ![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/discovery_enable.png)
