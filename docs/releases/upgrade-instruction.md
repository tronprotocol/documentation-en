# New Version Deployment Manual of java-tron
For the mandatory upgrade versions, please strictly follow this guide to deploy the new version. For the non-mandatory upgrade ones, you can decide whether to deploy it according to your needs. 

Please directly refer to [java-tron New version deployment Process](#new-version-deployment-process) to upgrade your node. If you have deployed 'Active and Backup nodes', please follow the process of [Active and Backup Nodes Upgrade Guide](#active-and-backup-nodes-upgrade-guide). 


## New version deployment Process
Please follow the below steps to upgrade your FullNode, FullNode that produces blocks to the latest version.

### 1. Prepare the executable file of the new version

You can directly download the java-tron executable file, or download the code of the latest version and compile it to get the executable file of the new version. Please download the latest version of the code or jar file to a file directory other than the java-tron running directory:

* Way 1: Download the published executable file
    
    Directly download the latest version of the executable file FullNode.jar from the release page [https://github.com/tronprotocol/java-tron/releases](https://github.com/tronprotocol/java-tron/releases).
    
    Before using it, please verify the file signature first to ensure the consistency and integrity of the jar file. For the verification steps, please refer to [java-tron Consistency Verification](https://tronprotocol.github.io/documentation-en/releases/signature_verification/).
    
    
* Way 2: Compile the source code
    
    Download the source code and switch to the branch of the new version.
    ```
    $ git clone https://github.com/tronprotocol/java-tron.git
    $ git checkout -b relase_vx.x.x
    ```
    
    Compile the project: In the code directory of the new version, execute the following command to compile the project, and the compiled executable file will be generated in the `build/libs` directory.
    ```
    $ ./gradlew clean build -x test
    ```
    

### 2. Shut down the java-tron process
Shut down the node process. Note: If a java-tron node has not been deployed on this machine before, please skip to step 5.

* First, get the process ID of the java-tron node through the following command
    ```
    $ ps -ef | grep java
    ```
    
* Shut down the node process
    ```
    $ kill -15 the process id
    ```


### 3. Backup
Please back up the executable file, database, and configuration file before the upgrade in sequence. The backup data is used to restore to the old version when a problem is encountered that leads to fail deploying during the upgrade.

* Backup the current executable jar file
    ```
    $ mv $JAVA_TRON.jar $JAVA_TRON.jar.`date "+%Y%m%d%H%M%S"`
    ```
* Backup the current database `output-directory`
    ```
    $ tar cvzf output-directory.`date "+%Y%m%d%H%M%S"`.etgz output-directory
    ```
* Backup the current configuration file
    ```
    $ mv $config.conf $config.conf.`date "+%Y%m%d%H%M%S"`
    ```


### 4. Replace old version files
After preparing the executable file of the new version and backing up the original node data, please follow the steps below to replace the old files:

1. Copy the newest jar package obtained in the previous step to the java-tron working directory to replace the old executable file.
2. Replace the old configuration file with the latest configuration file. If you need to modify the configuration, such as adding a keystore file, private key, etc, please modify it yourself.

Note: For the database file, you can use the original database file in the java-tron working directory, or you can choose to use [database backup snapshot](https://tronprotocol.github.io/documentation-en/using_javatron/backup_restore/#public-backup-data).


### 5. Start the nodes
The startup commands of FullNode which produces blocks and ordinary FullNode are different, please choose the startup command according to the actual situation:

* For the super representative's FullNode, the startup command is:
    ```
    nohup java -Xmx24g -XX:+UseConcMarkSweepGC  -jar FullNode.jar  -p  private key --witness -c main_net_config.conf </dev/null &>/dev/null &
    ```
    Note: It is not necessary to use the above command parameter to set the private key. If you use the keystore file or configure the private key in the configuration file, please set it up your way.

* For a FullNode, the startup command is:
    ```
    nohup java -Xmx24g -XX:+UseConcMarkSweepGC -jar FullNode.jar -c   main_net_config.conf </dev/null &>/dev/null &
    ```
             
### 6. Wait for syncing completion
After the node is successfully started, please wait patiently for the node block synchronization to complete.
### 7. Upgrade completed
After the node is synchronized to the latest block of the network, it means that the deployment of the new version is completed.

If you encounter any problems during the upgrade leading to fail deploying the new version, please use the data backed up in the third step to restore to the old version, and give your feedback in GitHub or the community in time to help you complete the deployment of the new version as soon as possible.


## Active and Backup Nodes Upgrade Guide
To upgrade the active and backup nodes, please follow the steps below:

1. Upgrade the backup node

    Upgrade the backup node according to the [java-tron new version deployment Process](#new-version-deployment-process).

2. Shut down the master node

    After the backup node is successfully upgraded to the new version, please wait for the completion of synchronization of the backup node before shutting down the master node. At this time, the backup node will automatically take over from the master node and become the active node.

3. Upgrade the master node

    If the backup node works normally, follow [java-tron New Version Deployment Process](#new-version-deployment-process) to upgrade the master node. Otherwise, shut down the backup node and start the master node. If an error occurs during the upgrade, please contact TRON technical support team and send the node’s log for root cause analysis.

4. Shut down the backup node

    After the master node is upgraded and fully synchronized, shut down the backup node. After the backup node shuts down, the master node will take over as the active node again.

5. Start the backup node
