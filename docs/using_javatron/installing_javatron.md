# Deploy a java-tron Node

java-tron nodes support to be deployed on `Linux` or `MacOS` operating systems, and rely on `Oracle JDK 1.8`, other versions of JDK are not supported.

The minimum hardware configuration required to run a java-tron node is `8-core CPU`, `16G memory`, `3T SDD`, the recommended configuration is: `16-core CPU`, `32G memory`, `3.5T+ SDD`. The fullnode running by super representative to produce block recommends `32-core CPU` and `64G memory`.


## Compile the Source Code
First, clone the java-tron repository to the local with the following git command, and switch to the `master` branch. Before executing the command, make sure you have installed the `git` tool.

```
$ git clone https://github.com/tronprotocol/java-tron.git
$ git checkout -t origin/master
```

Then, compile the java-tron source code by executing the following command. The parameter `-x test` means to skip the execution of the test case. You can also remove this parameter to execute the test code during the compilation process, which will make the compilation time longer. After the compilation is complete, FullNode.jar will be generated in the `java-tron/build/libs/` directory.

```
$ cd java-tron
$ ./gradlew clean build -x test
```

## Startup a java-tron Node
You can choose different configuration files to connect java-tron nodes to different networks. The mainnet configuration file is: [main_net_config.conf](https://github.com/tronprotocol/tron-deployment/blob/master/main_net_config.conf), other network configuration files can be found [here](https://github.com/tronprotocol/tron-deployment).


### Startup a fullnode

Fullnode has full historical data, it is the entry point into the TRON network , it provides HTTP API and gRPC API for external query. You can interact with the TRON network through fullnode：transfer assets, deploy contracts, interact with contracts and so on. The mainnet fullnode startup command is as follows, and the configuration file of the fullnode is specified by the `-c` parameter: 

```
$  java -Xmx24g -XX:+UseConcMarkSweepGC -jar FullNode.jar -c main_net_config.conf
```

* -XX:+UseConcMarkSweepGC  ：Specifies parallel garbage collection. To be placed before the -jar parameter, not at the end. 
* -Xmx  ：The maximum value of the JVM heap, which can be set to 80% of the physical memory.

### Startup a fullnode that produces blocks 

Adding the `--witness` parameter to the startup command, fullnode will run as a node which produces blocks. In addition to supporting all the functions of fullnode, the block-producing fullnode also supports block production and transaction packaging. Please make sure you have a super representative account and get the votes of others. If the votes ranks in the top 27, you need to start a full node that produces blocks to participate in block production.
  
Fill in the private key of the super representative address into the `localwitness` list in the main_net_config.conf, below is an example. But if you don't want to use this way of specifying the private key in plain text, you can use the keystore + password method, please refer to [Others](#others) chapter.

```
localwitness = [
    650950B193DDDDB35B6E48912DD28F7AB0E7140C1BFDEFD493348F02295BD812
]
```
  
then run the following command to start the node:
  
```
$ java -Xmx24g -XX:+UseConcMarkSweepGC -jar FullNode.jar --witness -c main_net_config.conf
```

**Note**: For the mainnet and nile testnet, since the amount of data to be synchronized is large after the new node is started, it will take a long time to synchronize the data. You can use [Data Snapshots](backup_restore.md/#public-backup-data) to speed up node synchronization. First download the latest data snapshot and extract it to the `output-directory` directory of the TRON project, and then start the node, so that the node will synchronize on the basis of the data snapshot.

### Block-producing fullnodes in Master-Slave Mode
To enhance the reliability of block-producing fullnode, you can deploy multiple block-producing fullnodes under the same account to form a master-slave mode. When deploying two or more nodes for an account with block-producing permission, the `node.backup` configuration in the configuration file of each node must be properly set. The configuration items for `node.backup` are as follows:  

```
node.backup {
  # udp listen port, each member should have the same configuration
  port = 10001

  # my priority, each member should use different priority
  priority = 8

  # time interval to send keepAlive message, each member should have the same configuration unit: ms
  keepAliveInterval = 3000

  # peer's ip list, can't contain myself
  members = [
    # "ip",
    # "ip"
  ]
}
```
For example, if an account with block production permission deploys three nodes with IP addresses 192.168.0.100, 192.168.0.101, and 192.168.0.102 respectively, their `node.backup` configurations should be set as follows:

- ip = 192.168.0.100
```
node.backup {
  port = 10001
  priority = 8
  keepAliveInterval = 3000
  members = [
    "192.168.0.101",
    "192.168.0.102"
  ]
}
```

- ip = 192.168.0.101
```
node.backup {
  port = 10001
  priority = 7
  keepAliveInterval = 3000
  members = [
    "192.168.0.100",
    "192.168.0.102"
  ]
}
```

- ip = 192.168.0.102
```
node.backup {
  port = 10001
  priority = 6
  keepAliveInterval = 3000
  members = [
    "192.168.0.100",
    "192.168.0.101"
  ]
}
```
**Notes:**

- The backup service of a node will only be activated when it has synchronized to the latest state. The latest state is defined as:  `(node's system time - timestamp of the latest successfully synchronized block) < block production interval`, block production interval: slot time(currently 3 seconds).
  
- When a high-priority node fails and loses its master status, other slave nodes will compete to become the new master. If the original high-priority node recovers and meets the block production conditions again, it will not automatically regain master status. It must wait until the current master node fails before it can compete again.

- Time required for master-slave switchover: when the master node fails, the minimum time required for a slave node to switch to master status is `2 × keepAliveTimeout`, where `keepAliveTimeout = keepAliveInterval × 6`. The reason for requiring `2 × keepAliveTimeout` is that the slave node must go through an intermediate `INIT` state during the transition:  `SLAVER`  → `INIT` → `MASTER`(Each backup node has three status: INIT, SLAVER, MASTER)

### Others
#### How to use `keystore + password` to specify the privatekey of witness account

1. You should not use the nohup command because the interaction is required when running the node. It is recommended to use session keeping tools such as screen, tmux, etc.
2. Comment the `localwitness` item in main_net_config.conf and uncomment the `localwitnesskeystore` item. Fill in the path of the Keystore file. Note that the Keystore file needs to be placed in the current directory where the startup command is executed or its subdirectory. If the current directory is "A", the directory of the Keystore file is "A/B/localwitnesskeystore.json", it needs to be configured as:
    ```
    localwitnesskeystore = [
          "B/localwitnesskeystore.json"
    ]
    ```
    **Note**: For `keystore + password` generation, you can use the register wallet command of the [wallet-cli](https://github.com/tronprotocol/wallet-cli.git).
3. Startup the fullnode which produces blocks
    ```
        $ java -Xmx24g -XX:+UseConcMarkSweepGC -jar FullNode.jar --witness -c main_net_config.conf
    ```
4. Enter the password correctly to finish the node startup.



#### Optimize Memory Allocation with tcmalloc

Memory allocation of java-tron can be optimized with tcmalloc. The method is as follows:

First install tcmalloc, then add the following two lines to the startup script, the path of tcmalloc is slightly different for different Linux distributions.

```
#!/bin/bash
  
export LD_PRELOAD="/usr/lib/libtcmalloc.so.4"
export TCMALLOC_RELEASE_RATE=10
  
# original start command
java -jar .....
```

Instructions for each Linux distributions are as below:

* Ubuntu 20.04 LTS / Ubuntu 18.04 LTS / Debian stable
    Install

    ```
    $ sudo apt install libgoogle-perftools4
    ```

    In the startup script add the following:

    ```
    export LD_PRELOAD="/usr/lib/x86_64-linux-gnu/libtcmalloc.so.4"
    export TCMALLOC_RELEASE_RATE=10
    ```

* Ubuntu 16.04 LTS
    Same install command as above. In the startup script add the following:

    ```
    export LD_PRELOAD="/usr/lib/libtcmalloc.so.4"
    export TCMALLOC_RELEASE_RATE=10
    ```

* CentOS 7
  Install
    ```
    $ sudo yum install gperftools-libs
    ```
    In the startup script add the following:
    ```
    export LD_PRELOAD="/usr/lib64/libtcmalloc.so.4"
    export TCMALLOC_RELEASE_RATE=10
    ```
