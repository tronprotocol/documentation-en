# java-tron Node Upgrade Guide

This guide provides detailed instructions on how to safely upgrade your java-tron node to the latest version.

For **mandatory upgrades**, it is crucial to strictly follow this guide to complete the deployment. For **optional upgrades**, you may choose whether to upgrade based on your specific needs.

  * For standard nodes, please refer to the [Standard Node Upgrade Process](#standard_process).
  * For nodes configured with a primary/backup high-availability setup, please follow the [Primary/Backup Node Upgrade Guide](#primary/backup_upgrade) to ensure a seamless service transition.

-----
<a id="standard_process"></a>
## Standard Node Upgrade Process

All Fullnodes, including block-producing Super Representative nodes, should follow these steps to complete the upgrade.

<a id="step1"></a> 
### Step 1: Prepare the New Version Package

You can either download the compiled java-tron executable directly or download the new version's source code and compile it yourself to obtain the new executable file. Please perform the following operations in a directory outside of the current java-tron running directory.

#### Option 1: Download the Executable (Recommended)

1. Visit the [java-tron GitHub Releases](https://github.com/tronprotocol/java-tron/releases) page to download the latest version of the `FullNode.jar` executable.
2. **Security Check**: To ensure the integrity and security of the file, it is essential to perform a signature verification on the downloaded JAR file according to the [java-tron Signature Verification](https://tronprotocol.github.io/documentation-en/releases/signature_verification/) guide.


#### Option 2: Compile from Source Code

1. Clone the `java-tron` repository and switch to the target version's branch.

    ```
    # clone the repository
    $ git clone https://github.com/tronprotocol/java-tron.git

    # Switch to the specified version branch
    $ cd java-tron
    $ git checkout -b release_vx.x.x
    ```    
2. Run the build command. Upon successful compilation, the new executable file, `FullNode.jar`, will be generated in the `build/libs/` directory.
    ```
    $ ./gradlew clean build -x test
    ```

### Step 2: Stop the Running Node

> **Note**: If this is your first time deploying the node, please skip directly to [Step 5: Start the Node](#step5).

1. Use the following command to find the `PID` of the java-tron process.

    ```
    $ ps -ef | grep java
    ```

2. Stop the node process.
    ```
    $ kill -15 <PID>
    ```

<a id="step3"></a> 
### Step 3: Back Up Critical Data

A full backup is strongly recommended before upgrading. Please perform the following backup steps in the specified order:

1. **Back up the current executable file**
    ```
    $ mv $JAVA_TRON.jar $JAVA_TRON.jar.`date "+%Y%m%d%H%M%S"`
    ```
2. **Back up the current `output-directory` database**
    ```
    $ tar cvzf output-directory.`date "+%Y%m%d%H%M%S"`.etgz output-directory
    ```
 3. **Back up the current configuration file**
    ```
    $ mv $config.conf $config.conf.`date "+%Y%m%d%H%M%S"`
    ```

This ensures that if the upgrade fails, you can quickly roll back to the previous version using the backup.

### Step 4: Replace Old Files

After preparing the new version of the executable file and backing up the original node data, follow these steps to replace the old files:

1. Copy the new `FullNode.jar` obtained in [Step 1](#step1) to the java-tron working directory.
2. Update the Configuration File (optional)
    - We recommend replacing your existing configuration file with the new version from the release. After replacing it, merge your previous custom settings (e.g., private key, keystore path) into the new file.
    - **Configuration Update Strategy**
        - **This step is optional**. You can decide whether to update the configuration file based on your specific needs. However, we highly recommend using the latest file to ensure full compatibility and access to new features.
        - If an update is required for a specific release, it will be explicitly stated in the release notes. Always review the release notes before upgrading.
  
> **Note on the Database**: The existing database in the working directory can be used as-is. Alternatively, you may restore from a pre-built [database snapshot](https://tronprotocol.github.io/documentation-en/using_javatron/backup_restore).

<a id="step5"></a> 
### Step 5: Start the Node

Please select the appropriate startup command based on your node type.

  * **Super Representative (Block-Producing Node)**

    ```
    nohup java -Xmx24g -XX:+UseConcMarkSweepGC -jar FullNode.jar  -p <your private key> --witness -c config.conf </dev/null &>/dev/null &
    ```
    > **Note**: We recommend managing your private key using a `keystore` file or within the configuration file, rather than passing it directly as a command-line argument.
    
  * **Regular Fullnode**

    ```
    nohup java -Xmx24g -XX:+UseConcMarkSweepGC -jar FullNode.jar -c config.conf </dev/null &>/dev/null &

    ```

### Step 6: Verify and Monitor

1.  **Wait for Node Synchronization**: After the node starts, it will begin to synchronize block data. Please wait patiently for it to catch up to the latest block height of the network.
2.  **Check the Logs**: Monitor the log output to ensure the node is running normally and without any error messages.
3.  **Confirm Synchronization Status**: You need to verify that synchronization is complete by comparing the latest block height of your local node with that of the TRON Mainnet. The upgrade is successful when the two heights are nearly identical.

    - To query local node block height, call the `/wallet/getnowblock` API:
        ```
        curl http://127.0.0.1:8090/wallet/getnowblock
        ```
    - To check the block height on Mainnet in real-time on [TRONSCAN](https://tronscan.org).

**Contingency Plan**: If you encounter any issues during the upgrade process that prevent the node from starting or running correctly, immediately use the data backed up in [Step 3](#step3) to restore the previous version. Please submit a GitHub Issue or report the problem to the TRON community for assistance.

-----
<a id="primary/backup_upgrade"></a> 
## Primary/Backup Node Upgrade Guide

To ensure high availability of the service, the upgrade of primary/backup nodes should adopt a rolling upgrade strategy.

1.  **Upgrade the Backup Node**
      * First, perform all the steps in the [Standard Node Upgrade Process](#standard_process) on the Backup Node.
2.  **Perform the Switchover**
      * After confirming that the Backup Node has been successfully upgraded and has completed block synchronization, stop the process on the **Master Node**.
      * At this point, the Backup Node will automatically take over, becoming the new **Active Node** and serving traffic.
3.  **Upgrade the Original Master Node**
      * After confirming that the new Active Node (the former Backup Node) is running stably, perform the [Standard Node Upgrade Process](#standard_process) on the original Master Node.
      * **Error Handling**: If the new Active Node fails during this period, immediately stop its upgrade process and restart the original Master Node to restore service. At the same time, please save the complete logs from the failed node for troubleshooting. For further support, please submit a GitHub Issue with the relevant logs or report it to the community.
4.  **Restore the Primary/Backup Architecture**
      * After the original Master Node has been upgraded, started, and fully synchronized, stop the currently active node (the former Backup Node).
      * The original Master Node will automatically take over again, resuming its role as the Active Node.
5.  **Restart the Backup Node**
      * Finally, restart the upgraded Backup Node to restore it to its backup status. This completes the entire primary/backup upgrade process.
