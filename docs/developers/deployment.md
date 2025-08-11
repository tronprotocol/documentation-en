# Deploying a `java-tron` Node

This document guides developers on how to deploy a TRON `java-tron` node on `Linux` or `macOS` operating systems. 

**Requirement:** The `java-tron` node currently requires **Oracle JDK 1.8**. Other JDK versions are not supported.


## Hardware Configuration Requirements

The minimum hardware configuration required to run a `java-tron` node is as follows:
* **CPU**: 8 Cores
* **Memory**: 16 GB
* **SSD**: 3 TB
* **Network Bandwidth**: 100 Mbps

The recommended configuration is:
* **CPU**: 16 Cores
* **Memory**: 32 GB
* **SSD**: 3.5 TB+
* **Network Bandwidth**: 100 Mbps

To run a Super Representative (SR) node for **block production**, the recommended configuration is:
* **CPU**: 32 Cores
* **Memory**: 64 GB
* **SSD**: 3.5 TB+
* **Network Bandwidth**: 100 Mbps

## Obtaining the `java-tron` Client

You can directly download the official client [here](https://github.com/tronprotocol/java-tron/releases), or you can compile the source code yourself to package the client.

### Compiling `java-tron` Source Code

Before you begin compiling, ensure that **git** is installed on your system.

1. First, clone the `java-tron` source code to your local machine using the `git` command and switch to the `master` branch:

```shell!
git clone https://github.com/tronprotocol/java-tron.git
git checkout -t origin/master
```

2. Then, execute the following commands to compile the `java-tron` source code:

```shell!
cd java-tron
./gradlew clean build -x test
```

* The parameter `-x test` indicates skipping the execution of test cases. You can remove this parameter to execute test code during compilation, but this will extend the compilation time.
* After compilation is complete, the `FullNode.jar` file will be generated in the `java-tron/build/libs/` directory.


## Starting a `java-tron` Node

You can choose different configuration files to connect the `java-tron` node to different TRON networks:

* For Mainnet FullNode configuration file: [main_net_config.conf](https://github.com/tronprotocol/tron-deployment/blob/master/main_net_config.conf)
* For other network node configuration:
    * Nile Testnet: https://nileex.io/
    * Private Network: https://github.com/tronprotocol/tron-deployment

### Starting a FullNode

A **FullNode** serves as an entry point to the TRON network, possesses complete historical data, and provides external access via **HTTP API**, **gRPC API**, and **JSON-RPC API**. You can interact with the TRON network through a FullNode for activities such as asset transfers, smart contract deployments, and smart contract interactions.

Below is the command to start a **Mainnet FullNode**, specifying the configuration file with the `-c` parameter:

```shell
java -Xmx24g -XX:+UseConcMarkSweepGC -jar FullNode.jar -c main_net_config.conf
```

* `-XX:+UseConcMarkSweepGC`: Specifies the **Concurrent Mark Sweep (CMS) garbage collector**. This parameter must be placed before the `-jar` parameter.
* `-Xmx`: Sets the maximum Java Virtual Machine (JVM) heap size, typically recommended to be **80% of physical memory**.
* To start a **Nile Testnet FullNode** or **Private network FullNode**, use the corresponding configuration file links provided at the beginning of this section.


### Starting a Super Representative Node

By adding the `--witness` parameter to the FullNode startup command above, the `FullNode` will run as an **SR Node**. In addition to supporting all FullNode functionalities, an SR Node also supports **block production** and **transaction packaging**.

**Important Notes**:
* Ensure that you own an **SR account** and have received sufficient votes. If your vote count ranks among the top 27, you need to start an SR Node to participate in block production. 
    * Note that even if your node doesn't make it into the top 27, a node started with the `--witness` parameter will still operate as a regular node; it can begin producing blocks immediately once its ranking reaches the top 27. 
* Fill in the **private key** of your Super Representative account in the `localwitness` list of `main_net_config.conf`.

Here is an example of the `localwitness` configuration:

```json
localwitness = [
    650950B193DDDDB35B6E48912DD28F7AB0E7140C1BFDEFD493348F02295BD812
]
```

Then execute the following command to start the SR Node:

```shell
java -Xmx24g -XX:+UseConcMarkSweepGC -jar FullNode.jar --witness -c main_net_config.conf
```

## Optimizations and Considerations

### Speeding Up Node Data Synchronization

For Mainnet and Nile Testnet, a newly launched node needs to synchronize a large amount of data, which will take a significant amount of time. You can use [data snapshots](https://tronprotocol.github.io/documentation-en/using_javatron/backup_restore/#main-net-data-snapshot) to accelerate node synchronization.

The operational steps are as follows:
1. Download the latest data snapshot.
2. Unzip it to the `output-directory` within your `tron` project.
3. Then start the node; the node will continue to synchronize based on the data snapshot.

### Specifying Super Representative Account Private Key Using Keystore + Password

To avoid specifying the private key in plaintext within the configuration file, you can choose to use a `keystore` file and password.

1. **Important Notes**:
    * This method requires human interaction to enter the password during node startup, so **do not** use the `nohup` command.
    * It is recommended to use a session persistence tool, such as **screen** or **tmux**.

2. **Configuration Steps**:
    * Comment out the `localwitness` configuration item in the node configuration file.
    * Uncomment the `localwitnesskeystore` configuration item and fill in the path to the `keystore` file.
    * Note that the `keystore` file needs to be placed in the current directory where the startup command is executed, or in its subdirectory.
        * For example, if the current directory is `A`, and the `keystore` file path is `A/B/localwitnesskeystore.json`, the configuration should be:

    ```json
    localwitnesskeystore = [
      "B/localwitnesskeystore.json"
    ]
    ```

    * You can generate the `keystore` file and password using the `registerwallet` command from the `wallet-cli` project.

3. **Starting a SR Node**:

    ```
    java -Xmx24g -XX:+UseConcMarkSweepGC -jar FullNode.jar --witness -c main_net_config.conf
    ```

4. **Entering the Password**:
    * During node startup, the system will prompt you to enter the password. After correctly entering the password, the node will complete its startup.

### Optimizing Memory Usage with `tcmalloc`

To achieve optimal memory usage, you can use Google's `tcmalloc` instead of the system's `glibc malloc`.

1. **Install `tcmalloc`**:

    * **Ubuntu 20.04 LTS / Ubuntu 18.04 LTS / Debian stable**:

    ```shell
    sudo apt install libgoogle-perftools4
    ```

    * **Ubuntu 16.04 LTS**:

    ```shell
    sudo apt install libgoogle-perftools4
    ```

    * **CentOS 7**:

    ```shell
    sudo yum install gperftools-libs
    ```

2. **Modify the Startup Script**:

    * Add the following two lines to your node's startup script. Please note that the path to `libtcmalloc.so.4` might vary slightly across different Linux distributions.

    ```bash!
    #!/bin/bash

    export LD_PRELOAD="/usr/lib/libtcmalloc.so.4" # Adjust path according to your system
    export TCMALLOC_RELEASE_RATE=10

    # original start command
    java -jar .....
    ```

    * **Ubuntu 20.04 LTS / Ubuntu 18.04 LTS / Debian stable**:

    ```bash!
    export LD_PRELOAD="/usr/lib/x86_64-linux-gnu/libtcmalloc.so.4"
    export TCMALLOC_RELEASE_RATE=10
    ```

    * **Ubuntu 16.04 LTS**:

    ```bash!
    export LD_PRELOAD="/usr/lib/libtcmalloc.so.4"
    export TCMALLOC_RELEASE_RATE=10
    ```

    * **CentOS 7**:

    ```bash!
    export LD_PRELOAD="/usr/lib64/libtcmalloc.so.4"
    export TCMALLOC_RELEASE_RATE=10
    ```