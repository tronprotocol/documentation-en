# Deploy Java-tron Node

Supported Operating Systems: `Linux` ,`MacOS`

Tools and Dependencies：`Oracle JDK 1.8` , `git`

**Note**: Please install `Oracle JDK 1.8`, not `Open JDK 1.8`

# Recommended Configuration
If you want to deploy a Java-tron node on the mainnet or Nile testnet, the recommended machine configuration is as follows:

* CPU：16 cores 
* RAM：32G 
* SSD：1.5T+
* Bandwidth：100M 

If you are a super representative to build a fullnode for block production, the recommended configuration is: CPU：32 cores, RAM：64G

If you only need to develop or test some features of Java-tron or your DAPP application, and only need to build a private chain network, the recommended configuration is: 2+ core CPU.

# Deployment Guide
Regardless of the type of node, the deployment process is the same, please refer to the following steps:
## 1. Obtain Fullnode.jar
You can obtain FullNode.jar through compiling source code or downloading [the released jar](https://github.com/tronprotocol/java-tron/releases) directly.

### Compile the source code
To obtain an executable file by compiling the source code, you need to clone the source code locally, and then execute the compile command:

1. Obtain java-tron source code
    Get the Java-tron source code with the following command. Before executing the command, make sure you have installed the `git` tool.

    ```
    $ git clone https://github.com/tronprotocol/java-tron.git
    $ git checkout -t origin/master
    ```
2. Compile
    The Java-tron project can be compiled directly by executing the following command. The parameter `-x test` means to skip the execution of the test case, you can also remove this parameter, it just requires more compilation time.

    ```
    $ cd java-tron
    $ ./gradlew clean build -x test
    ```
    You will find the FullNode.jar under ./java-tron/build/libs/ folder if build is successful.


## 2. Obtain the configuration file
Get the mainnet configure file: [main_net_config.conf](https://github.com/tronprotocol/tron-deployment/blob/master/main_net_config.conf), other network configuration files can be found [here](https://github.com/tronprotocol/tron-deployment).

## 2. Start The Node
The command to start a fullnode or a block-producing fullnode is as follows:

* Startup a fullnode for mainnet

    Full node has full historical data, it is the entry point into the TRON network , it provides HTTP API and gRPC API for external query. You can interact with the TRON network through fullnode：transfer assets, deploy contracts, interact with contracts and so on. The mainnet fullnode startup command is as follows, and the configuration file of the fullnode is specified by the `-c` parameter: 

    ```
    $  java -Xmx24g -XX:+UseConcMarkSweepGC -jar FullNode.jar -c main_net_config.conf
    ```

    * -XX:+UseConcMarkSweepGC  ：Specifies parallel garbage collection. To be placed before the -jar parameter, not at the end. 
    * -Xmx  ：The maximum value of the JVM heap, which can be set to 80% of the physical memory.

* Startup a fullnode that produces blocks for mainnet

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

**Note**: For the mainnet and nile testnet, since the amount of data to be synchronized is large after the new node is started, it will take a long time to synchronize the data. You can use [Data Snapshots](../backup_restore/#public-backup-data) to speed up node synchronization. First download the latest data snapshot and extract it to the `output-directory` directory of the tron project, and then start the node, so that the node will synchronize on the basis of the data snapshot.

For a running fullnode, you can use the command `kill -15 process id` to shut down it.


# Others
**How to use `keystore + password` to specify the privatekey of witness account**

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



**Optimize Memory Allocation with tcmalloc**

Memory allocation of java-tron can be optimized with tcmalloc. The method is as follows:

First install tcmalloc, then add the following two lines to the startup script, the path of tcmalloc is slightly different for different Linux distributions.

```
#!/bin/bash
  
export LD_PRELOAD="/usr/lib/libtcmalloc.so.4"
export TCMALLOC_RELEASE_RATE=10
  
# original start command
java -jar .....
```

Instructions for each Linux distributions are as belows:

* Ubuntu 20.04 LTS / Ubuntu 18.04 LTS / Debian stable
    Install

    ```
    $ sudo apt install libgoogle-perftools4
    ```

    In the startup script add the followings:

    ```
    export LD_PRELOAD="/usr/lib/x86_64-linux-gnu/libtcmalloc.so.4"
    export TCMALLOC_RELEASE_RATE=10
    ```

* Ubuntu 16.04 LTS
    Same install command as above. In the startup script add the followings:

    ```
    export LD_PRELOAD="/usr/lib/libtcmalloc.so.4"
    export TCMALLOC_RELEASE_RATE=10
    ```

* CentOS 7
  Install
    ```
    $ sudo yum install gperftools-libs
    ```
    In the startup script add the followings:
    ```
    export LD_PRELOAD="/usr/lib64/libtcmalloc.so.4"
    export TCMALLOC_RELEASE_RATE=10
    ```