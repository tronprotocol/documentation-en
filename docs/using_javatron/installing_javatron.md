# Deploying a java-tron Node

This document guides developers on how to deploy a TRON java-tron node on `Linux` or `macOS` operating systems.

**Important Note:** The java-tron node currently requires **Oracle JDK 1.8**. Other JDK versions are not supported.


## Hardware Configuration Requirements

The minimum hardware configuration required to run a java-tron node is as follows:

* **CPU**: 8 Cores
* **Memory**: 16 GB
* **SSD**: 3 TB
* **Network Bandwidth**: 100 Mbps

The recommended configuration is:

* **CPU**: 16 Cores
* **Memory**: 32 GB
* **SSD**: 3.5 TB+
* **Network Bandwidth**: 100 Mbps

For a Super Representative (SR) node acting as a **block production node**, the recommended configuration is:

* **CPU**: 32 Cores
* **Memory**: 64 GB
* **SSD**: 3.5 TB+
* **Network Bandwidth**: 100 Mbps


## Obtaining the java-tron Client

You can directly download the official client [here](https://github.com/tronprotocol/java-tron/releases), or you can compile the source code yourself to package the client.

### Prerequisites Before Compiling java-tron
Before compiling java-tron, make sure you have:

- Operating system: `Linux` or `macOS` (`Windows` is not supported).
- Git and correct JDK version installed based on your CPU architecture.

Step 1: Verify Git is installed

If Git is not installed, download it from [https://git-scm.com/downloads](https://git-scm.com/downloads).

```bash
git --version
```

Step 2: Check your CPU architecture and install the correct JDK

```bash
uname -m
```

- If your architecture is `x86_64` (Intel/AMD 64-bit):

    - Install Java SE 8 (Oracle JDK 8): [https://www.oracle.com/java/technologies/javase/javase8-archive-downloads.html](https://www.oracle.com/java/technologies/javase/javase8-archive-downloads.html)
    - Verify:
    ```bash
    java -version
    ```
    The output should show a version starting with `1.8`.

- If your architecture is `arm64` or `aarch64` (Apple Silicon / ARM servers):

    - Install Java SE 17 (JDK 17): [https://www.oracle.com/java/technologies/downloads/#java17](https://www.oracle.com/java/technologies/downloads/#java17)
    - Verify:
    ```bash
    java -version
    ```
    The output should show a version starting with `17`.

### Compiling java-tron Source Code

1. Clone the repo and switch to the `master` branch:
    ```
    git clone https://github.com/tronprotocol/java-tron.git
    git checkout -t origin/master
    cd java-tron
    ```
2. Then, run the following commands to build java-tron:
    ```
    ./gradlew clean build -x test
    ```
    * The parameter `-x test` indicates skipping the execution of test cases. You can remove this parameter to execute test code during compilation, but this will extend the compilation time.
    * If you encounter `DependencyVerificationException` during the build, refresh dependencies and regenerate verification metadata:
      ```
      ./gradlew clean build -x test --refresh-dependencies
      ```
    * After compilation is complete, the `FullNode.jar` file will be generated in the `java-tron/build/libs/` directory.

## Starting a java-tron Full Node
A full node acts as a gateway to the TRON network, exposing comprehensive interfaces via HTTP and RPC APIs. Through these endpoints, clients may execute asset transfers, deploy smart contracts, and invoke on-chain logic. It must join a TRON network to participate in the network's consensus and transaction processing.

### Network Types

The TRON network is mainly divided into:

- **Main Network (Mainnet)**  
  The primary public blockchain where real value (TRX, TRC-20 tokens, etc.) is transacted, secured by a massive decentralized network.

- **[Nile Test Network (Testnet)](https://nileex.io/)**  
  A forward-looking testnet where new features and governance proposals are launched first for developers to experience. Consequently, its codebase is typically ahead of the Mainnet.

- **[Shasta Testnet](https://shasta.tronex.io/)**  
  Closely mirrors the Mainnet’s features and governance proposals. Its network parameters and software versions are kept in sync with the Mainnet, providing developers with a highly realistic environment for final testing.

- **Private Networks**  
  Customized TRON networks set up by private entities for testing, development, or specific use cases.

Network selection is performed by specifying the appropriate configuration file upon full-node startup. Mainnet configuration: [config.conf](https://github.com/tronprotocol/java-tron/blob/master/framework/src/main/resources/config.conf); Nile testnet configuration: [config-nile.conf](https://github.com/tron-nile-testnet/nile-testnet/blob/master/framework/src/main/resources/config-nile.conf)

### Starting a FullNode on the TRON main network

Launch a main-network full node with the built-in default configuration:
```bash
nohup java -jar ./build/libs/FullNode.jar &
```

* `nohup ... &`: Runs the command in the background and ignores the hangup signal.

> For production deployments or long-running Mainnet nodes, please refer to the below [JVM Parameter Optimization for FullNode](#jvm-parameter-optimization-for-mainnet-fullnode-deployment) guide for the recommended Java commands.

Using the below command, you can monitor the blocks syncing progress:
```bash
tail -f ./logs/tron.log
```

Use [TronScan](https://tronscan.org/#/), TRON's official block explorer, to view main network transactions, blocks, accounts, witness voting, and governance metrics, etc.

Please refer to the subsequent sections for detailed instructions on deploying full nodes within the Nile Testnet and private networks.

#### JVM Parameter Optimization for Mainnet FullNode Deployment
For higher efficiency and stability when connecting to Mainnet, please refer to the following full Java startup parameters for different architectures:

##### x86_64 (JDK 8)
```bash
nohup java -Xms9G -Xmx12G -XX:ReservedCodeCacheSize=256m \
    -XX:MetaspaceSize=256m -XX:MaxMetaspaceSize=512m \
    -XX:MaxDirectMemorySize=1G -XX:+PrintGCDetails \
    -XX:+PrintGCDateStamps  -Xloggc:gc.log \
    -XX:+UseConcMarkSweepGC -XX:NewRatio=3 \
    -XX:+CMSScavengeBeforeRemark -XX:+ParallelRefProcEnabled \
    -XX:+HeapDumpOnOutOfMemoryError \
    -XX:+UseCMSInitiatingOccupancyOnly  -XX:CMSInitiatingOccupancyFraction=70 \
    -jar ./build/libs/FullNode.jar -c main_net_config.conf &
```
##### ARM64 (JDK 17)
```bash
nohup java -Xmx9G -XX:+UseZGC \
    -Xlog:gc,gc+heap:file=gc.log:time,tags,level:filecount=10,filesize=100M \
    -XX:ReservedCodeCacheSize=256m \
    -XX:+UseCodeCacheFlushing \
    -XX:MetaspaceSize=256m \
    -XX:MaxMetaspaceSize=512m \
    -XX:MaxDirectMemorySize=1g \
    -XX:+HeapDumpOnOutOfMemoryError \
    -jar ./build/libs/FullNode.jar -c main_net_config.conf &
```

##### Java Startup Parameters Explanation
**General & Memory Parameters:**

*   `-Xms` / `-Xmx`: Sets the initial and maximum JVM heap size.
    * For minimum hardware requirements (16 GB RAM servers): Suggested JDK 8 use `-Xms9G -Xmx12G`; JDK 17 use `-Xmx9G`.
    * For servers with ≥32 GB RAM, suggest setting the maximum heap size (`-Xmx`) to 40 % of total RAM, with the minimum to `-Xms9G`.
*   `-XX:MetaspaceSize` / `-XX:MaxMetaspaceSize`: Sets the initial and maximum size of Metaspace (class metadata).
*   `-XX:MaxDirectMemorySize`: Limits the memory used by NIO Direct Byte Buffers.
*   `-XX:ReservedCodeCacheSize`: Sets the maximum size of the JIT code cache.
*   `-XX:+UseCodeCacheFlushing`: Allows the JVM to flush the code cache when full.
*   `-XX:+HeapDumpOnOutOfMemoryError`: Dumps the heap to a file if an OutOfMemoryError occurs.

**JDK 8 (CMS GC) Specific:**

*   `-XX:+UseConcMarkSweepGC`: Enables the Concurrent Mark Sweep (CMS) garbage collector.
*   `-XX:NewRatio=3`: Sets the ratio of Old Generation to Young Generation to 3:1.
*   `-XX:+CMSScavengeBeforeRemark`: Triggers a minor GC before the CMS Remark phase to reduce pause time.
*   `-XX:+ParallelRefProcEnabled`: Enables parallel reference processing to reduce pause times.
*   `-XX:+UseCMSInitiatingOccupancyOnly` & `-XX:CMSInitiatingOccupancyFraction=70`: Forces CMS to start collection when Old Gen is 70% full.
*   `-XX:+PrintGCDetails`, `-XX:+PrintGCDateStamps`, `-Xloggc:gc.log`: Legacy GC logging settings.

**JDK 17 (ZGC) Specific:**

*   `-XX:+UseZGC`: Enables ZGC, a scalable low-latency garbage collector.
*   `-Xlog:gc...`: Unified JVM logging configuration. The example configures GC logs with file rotation (10 files, 100MB each).

### Staring a FullNode on the Nile test network
Utilize the `-c` flag to direct the node to the configuration file corresponding to the desired network. Since Nile TestNet may incorporate features not yet available on the MainNet, it is **strongly advised** to compile the source code following the [Building the Source Code](https://github.com/tron-nile-testnet/nile-testnet/blob/master/README.md#building-the-source-code) instructions for the Nile TestNet.

```bash
nohup java -jar ./build/libs/FullNode.jar -c config-nile.conf &
```

Nile resources: explorer, faucet, wallet, developer docs, and network statistics at [nileex.io](https://nileex.io/).

### Access Shasta test network
Shasta does not accept public node peers. Programmatic access is available via TronGrid endpoints; see [TronGrid Service](https://developers.tron.network/docs/trongrid) for details.

Shasta resources: explorer, faucet, wallet, developer docs, and network statistics at [shastaex.io](https://shasta.tronex.io/).

### Starting a FullNode on a private network
To set up a private network for testing or development, follow the [Private Network guidance](https://tronprotocol.github.io/documentation-en/using_javatron/private_network/).

### Starting a Block Production Node

By adding the `--witness` parameter to the FullNode startup command above, the `FullNode` will run as a **Block Production Node** (SR Node). In addition to supporting all FullNode functionalities, a Block Production Node also supports **block production** and **transaction packaging**.

**Important Notes**:

* Ensure that you own a Super Representative (SR) account and have received sufficient votes. If your vote count ranks among the top 27, you need to start an SR Node to participate in block production.
  * Note that even if your node doesn't make it into the top 27, a node started with the `--witness` parameter will still operate as a regular node; once its ranking reaches the top 27, it can immediately begin producing blocks.
* Fill in the **private key** of your Super Representative account in the `localwitness` list of `config.conf`.

Here is an example of the `localwitness` configuration:

```
localwitness = [
    650950B1...295BD812
]
```

For SR nodes running on high-performance servers (e.g., ≥ 64GB RAM), it is strongly recommended to use the following optimized Java startup commands. These configurations are designed to ensure maximum stability and efficiency for block production. Execute the command corresponding to your environment:

#### Option 1: JDK 8 on x86_64
```bash
nohup java -Xms9G -Xmx24G -XX:ReservedCodeCacheSize=256m \
    -XX:MetaspaceSize=256m -XX:MaxMetaspaceSize=512m \
    -XX:MaxDirectMemorySize=1G -XX:+PrintGCDetails \
    -XX:+PrintGCDateStamps  -Xloggc:gc.log \
    -XX:+UseConcMarkSweepGC -XX:NewRatio=3 \
    -XX:+CMSScavengeBeforeRemark -XX:+ParallelRefProcEnabled \
    -XX:+HeapDumpOnOutOfMemoryError \
    -XX:+UseCMSInitiatingOccupancyOnly  -XX:CMSInitiatingOccupancyFraction=70 \
    -jar ./build/libs/FullNode.jar --witness -c config.conf &
```

#### Option 2: JDK 17 on ARM64
```bash
nohup java -Xms9G -Xmx24G -XX:+UseZGC \
    -Xlog:gc,gc+heap:file=gc.log:time,tags,level:filecount=10,filesize=100M \
    -XX:ReservedCodeCacheSize=256m \
    -XX:+UseCodeCacheFlushing \
    -XX:MetaspaceSize=256m \
    -XX:MaxMetaspaceSize=512m \
    -XX:MaxDirectMemorySize=1g \
    -XX:+HeapDumpOnOutOfMemoryError \
    -jar ./build/libs/FullNode.jar --witness -c config.conf &
```

### Master-Slave Mode for Block Production FullNodes

To enhance the reliability of block production FullNodes, you can deploy multiple block production FullNodes for the same account, forming a master-slave mode. When an account with block production rights deploys two or more nodes **(Recommended number: 2)**, it's necessary to configure `node.backup` in each node's configuration file. The descriptions of the `node.backup` configuration items are as follows:

```ini
node.backup {
  # udp listen port, each member should have the same configuration
  port = 10001

  # my priority, each member should use different priority
  priority = 8

  # time interval to send keepAlive message, each member should have the same configuration unit: ms
  keepAliveInterval = 3000

  # peers' IP list, must not include myself
  members = [
    # "ip",
    # "ip"
  ]
}
```
For example, if an account with block production rights deploys two nodes with IPs 192.168.0.100 and 192.168.0.101 respectively, their `node.backup` configurations should be as follows:

- Configuration for IP 192.168.0.100
```ini
node.backup {
  port = 10001
  priority = 8
  keepAliveInterval = 3000
  members = [
    "192.168.0.101"
  ]
}
```

* Configuration for IP 192.168.0.101

```ini
node.backup {
  port = 10001
  priority = 7
  keepAliveInterval = 3000
  members = [
    "192.168.0.100"
  ]
}
```

**Note**:

* A node will only start the backup service when it has synchronized to the latest state. The latest state is defined as: (Node's system time - Latest successfully synchronized block time) < Block production interval (time per slot, currently 3s).
* When a node with high priority fails and loses its master node status, other slave nodes will compete to become the master node. When the high-priority node recovers and meets the conditions for block production again, it will not automatically regain master node status; it needs to wait until the current master node fails before it can compete for the role again.
* Time required for master-slave switchover: When the master node fails, the time it takes for a slave node to switch to a master node is at least 2 * `keepAliveTimeout`, where `keepAliveTimeout` = `keepAliveInterval` * 6. Two `keepAliveTimeout` periods are needed because the slave node needs to transition through an intermediate "preparatory" state (INIT) to become the master node: Slave -> INIT -> Master.

## Optimizations and Considerations

### Speeding Up Node Data Synchronization

For Mainnet and Nile Testnet, a newly launched node needs to synchronize a large amount of data, which will take a significant amount of time. You can use [data snapshots](https://tronprotocol.github.io/documentation-en/using_javatron/backup_restore/#main-net-data-snapshot) to accelerate node synchronization.

The operational steps are as follows:

1. Download the latest data snapshot.
2. Unzip it to the `output-directory` folder within your `tron` project (default is `output-directory`).
3. Then start the node; the node will continue to synchronize based on the data snapshot.

### Specifying Super Representative Account Private Key Using Keystore + Password

To avoid specifying the private key in plaintext within the configuration file, you can choose to use a `keystore` file and password.

1. **Configuration Steps**:
    * Comment out the `localwitness` configuration item in the node configuration file.
    * Uncomment the `localwitnesskeystore` configuration item and fill in the path to the `keystore` file.
    * Note that the `keystore` file needs to be placed in the current directory where the startup command is executed, or in its subdirectory.
        * For example, if the current directory is `A`, and the `keystore` file path is `A/B/localwitnesskeystore.json`, the configuration should be:

        ```
        localwitnesskeystore = ["B/localwitnesskeystore.json"]
        ```

    * You can generate the `keystore` file and password using the `registerwallet` command from the `wallet-cli` project.

2. **Starting a Block Production Node**:

    * **Starting the node interactively without `nohup` (Recommended)**
        * **Important Notes**: This method requires human interaction to enter the password during node startup. It is recommended to use a session persistence tool, such as `screen` or `tmux`.
  
        ```
        java -Xmx24g -XX:+UseConcMarkSweepGC -jar FullNode.jar --witness -c config.conf
        ```

        * During node startup, the system will prompt you to enter the password. After entering the password correctly, the node will complete its startup.

    * **Using `nohup` to pass the password directly in the command line via `--password`**

        ```
        nohup java -Xmx24g -XX:+UseConcMarkSweepGC -jar FullNode.jar --witness -c config.conf --password "your_password" > start.log 2>&1 &
        ```

### Optimizing Memory Usage with `tcmalloc`

To achieve optimal memory usage, use Google's `tcmalloc` instead of the system's `glibc malloc`.

1. **Install `tcmalloc`**:
    * **Ubuntu 20.04 LTS / Ubuntu 18.04 LTS / Debian stable**:

    ```
    sudo apt install libgoogle-perftools4
    ```

    * **Ubuntu 16.04 LTS**:

    ```
    sudo apt install libgoogle-perftools4
    ```

    * **CentOS 7**:

    ```
    sudo yum install gperftools-libs
    ```

2. **Modify the Startup Script**:

    * Add the following two lines to your node's startup script. Please note that the path to `libtcmalloc.so.4` might vary slightly across different Linux distributions.

    ```
    #!/bin/bash

    export LD_PRELOAD="/usr/lib/libtcmalloc.so.4" # Adjust path according to your system
    export TCMALLOC_RELEASE_RATE=10

    # original start command
    java -jar .....
    ```

    * **Ubuntu 20.04 LTS / Ubuntu 18.04 LTS / Debian stable**:

    ```
    export LD_PRELOAD="/usr/lib/x86_64-linux-gnu/libtcmalloc.so.4"
    export TCMALLOC_RELEASE_RATE=10
    ```

    * **Ubuntu 16.04 LTS**:

    ```
    export LD_PRELOAD="/usr/lib/libtcmalloc.so.4"
    export TCMALLOC_RELEASE_RATE=10
    ```

    * **CentOS 7**:

    ```
    export LD_PRELOAD="/usr/lib64/libtcmalloc.so.4"
    export TCMALLOC_RELEASE_RATE=10
    ```
