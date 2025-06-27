# java-tron Node Maintenance Tool - Toolkit

The Toolkit integrates a series of tools of java-tron, and more functions will be added into it in the future for the convenience of developers. Currently Toolkit includes the following functions:

* [Database Partition Tool](#database-partition-tool)
* [Lite Fullnode Data Pruning](#lite-fullnode-data-pruning)
* [Data Copy](#data-copy)
* [Data Conversion](#data-conversion)
* [LevelDB Startup Optimization](#leveldb-startup-optimization)

The following describes the acquisition and use of the Toolkit toolbox in detail.

## Obtain Toolkit.jar
`Toolkit.jar` can be obtained from the [released version](https://github.com/tronprotocol/java-tron/releases) directly or by compiling the java-tron source code.

Compile the source code:

1. Obtain java-tron source code
   ```
   $ git clone https://github.com/tronprotocol/java-tron.git
   $ git checkout -t origin/master
   ```
2. Compile

   ```
   $ cd java-tron
   $ ./gradlew clean build -x test
   ```
    You will find the `Toolkit.jar` under `./java-tron/build/libs/` folder if build is successful.

## Database Partition Tool
As the data on the chain continues to grow, the pressure on data storage will increase. At present, the FullNode data of the TRON public chain has reached 1T, and the daily data growth is about 1.2G. According to the current data growth rate, the annual growth rate is about 450G. A single disk capacity may be insufficient and need to be replaced by a larger disk. To this end the Toolkit toolbox introduces the database storage partitioning tool. The tool can migrate some databases to other storage disks. When the user encounters insufficient disk space, he only needs to add another disk according to the capacity requirement and does not need to replace the original disk.

### Commands and parameters
To use the data partition function provided by Toolkit through the `db mv` command:

```
# full command
java -jar Toolkit.jar db mv [-h] [-c=<config>] [-d=<database>]
# examples
java -jar Toolkit.jar db mv -c main_net_config.conf -d /data/tron/output-directory
```

Optional command parameters are as follows:

- `-c | --config`: [ string ] This option is used to specify the FullNode configuration file. If not specified, the default value will be config.conf.
- `-d | --database-directory`: [ string ] This option is used to specify the FullNode database directory. If not specified, the default value will be output-directory.
- `-h | --help`: [ bool ] This option is used to view help description, default value: false.



### Usage Instructions
Follow the following steps to use the database partition tool:

1. [Stop FullNode service](#stop-fullnode-service)
2. [Configure for database storage migration](#configure-for-database-storage-migration)
3. [Perform database migration](#perform-database-migration)
4. [Restart FullNode service](#restart-fullnode-service)

#### Stop FullNode Service

Use the command kill -15 pid to close FullNode.jar, below is the FullNode process pid lookup command:

```
$ ps -ef |grep FullNode.jar |grep -v grep |awk '{print $2}'`
```

#### Configure For Database Storage Migration

The configuration of database migration is in the [storage.properties](https://github.com/tronprotocol/tron-deployment/blob/master/main_net_config.conf#L36) field in the java-tron node configuration file. The following is an example of migrating only the `block` and `trans` databases to illustrate how to migrate some databases to other storage disks:


```conf
storage {
 ......
  properties = [
    {
     name = "block",
     path = "/data1/tron",

    },
    {
     name = "trans",
     path = "/data1/tron",
   }
  ]
 ......
}

```
`name` is the database name which you want to migrate, and `path` is the destination directory for database migration. The tool will migrate the database specified by `name` to the directory specified by `path`, and then create a soft link under the original path pointing to `path` directory. After `FullNode` starts, it will find the `path` directory according to the soft link.


#### Perform Database Migration

When executed, the current migration progress will be shown.

```bash
$ java -jar Toolkit.jar db mv -c main_net_config.conf -d /data/tron/output-directory
```

#### Restart FullNode Service
After the migration is complete, restart the java-tron node.
```
# FullNode
$ nohup java -Xms9G -Xmx9G -XX:ReservedCodeCacheSize=256m \
                -XX:MetaspaceSize=256m -XX:MaxMetaspaceSize=512m \
                -XX:MaxDirectMemorySize=1G -XX:+PrintGCDetails \
                -XX:+PrintGCDateStamps  -Xloggc:gc.log \
                -XX:+UseConcMarkSweepGC -XX:NewRatio=2 \
                -XX:+CMSScavengeBeforeRemark -XX:+ParallelRefProcEnabled \
                -XX:+HeapDumpOnOutOfMemoryError \
                -XX:+UseCMSInitiatingOccupancyOnly  -XX:CMSInitiatingOccupancyFraction=70 \
                -jar FullNode.jar -c main_net_config.conf >> start.log 2>&1 &

# Super representative's FullNode
$ nohup java -Xms9G -Xmx9G -XX:ReservedCodeCacheSize=256m \
               -XX:MetaspaceSize=256m -XX:MaxMetaspaceSize=512m \
               -XX:MaxDirectMemorySize=1G -XX:+PrintGCDetails \
               -XX:+PrintGCDateStamps  -Xloggc:gc.log \
               -XX:+UseConcMarkSweepGC -XX:NewRatio=2 \
               -XX:+CMSScavengeBeforeRemark -XX:+ParallelRefProcEnabled \
               -XX:+HeapDumpOnOutOfMemoryError \
               -XX:+UseCMSInitiatingOccupancyOnly  -XX:CMSInitiatingOccupancyFraction=70 \
               -jar FullNode.jar --witness -c main_net_config.conf >> start.log 2>&1 &
```
## Lite Fullnode Data Pruning
Toolkit provides data pruning tool, which is mainly used for generating or pruning Lite Fullnode data.

The data pruning tool can divide the complete FullNode data into a snapshot dataset (Snapshot dataset) or a historical dataset (History dataset) according to the current `latest_block_number`, the snapshot dataset is used to start the Lite Fullnode (That is the Lite fullnode database), and the historical dataset is used for historical data query. Lite Fullnode started with a snapshot data set do not support querying historical data prior to the latest block height at the time of pruning. The data pruning tool also provides the function of merging historical data set with snapshot data set. The usage scenarios are as follows:



* **Convert FullNode data into Lite Fullnode data**

    The Lite Fullnode starts only based on the snapshot data set, use the data pruning tool to convert the full node data into the snapshot data set, and that will get the Lite Fullnode data
    
* **Prune Lite Fullnode data regularly**
    
    Since the Lite Fullnode saves the same data as the FullNode after startup, although the data volume of the Lite Fullnode is very small at startup, the data expansion rate in the later period is the same as that of the FullNode, so it may be necessary to periodically prune the data. Clipping the Lite Fullnode data is also to use this tool to cut the Lite Fullnode data into snapshot data set, that is, to obtain the Pruned Lite Fullnode data
    
* **Convert Lite Fullnode data back to FullNode data**

    Since Lite Fullnode does not support historical data query, if you want to support it, you need to change Lite Fullnode data into FullNode data, then the node will change from Lite Fullnode to FullNode. You can directly download the snapshot of the FullNode database, or you can use the data pruning tool: first, convert the FullNode data into historical data set, and then merge the historical data set and the snapshot data set of the Lite Fullnode to obtain the FullNode data.
    
Note: Before using this tool for any operation, you need to stop the currently running node first.


### Command and parameters
To use the data pruning tool provided by Toolkit through the `db lite` command:

```
# full command
  java -jar Toolkit.jar db lite [-h] -ds=<datasetPath> -fn=<fnDataPath> [-o=<operate>] [-t=<type>]
# examples
  #split and get a snapshot dataset
  java -jar Toolkit.jar db lite -o split -t snapshot --fn-data-path output-directory/database --dataset-path /tmp
  #split and get a history dataset
  java -jar Toolkit.jar db lite -o split -t history --fn-data-path output-directory/database --dataset-path /tmp
  #merge history dataset and snapshot dataset
  java -jar Toolkit.jar db lite -o merge --fn-data-path /tmp/snapshot --dataset-path /tmp/history
```

Optional command parameters are as follows:

- `--operation | -o`: [ split | merge ], this parameter specifies the operation as either to split or to merge, default is split.
- `--type | -t`: [ snapshot | history ], this parameter is used only when the operation is `split`. `snapshot` means clip to Snapshot Dataset and `history` means clip to History Dataset. Default is `snapshot`.
- `--fn-data-path | -fn`: The database path to be split or merged. When the operation type is `split`, `fn-data-path` is used to indicate the directory of the data to be pruned; when the operation type is `merge`, `fn-data-path` indicates the database directory of the Lite Fullnode or the directory of the snapshot dataset.
- `--dataset-path | -ds`: When operation is `split`, dataset-path is the path that store the snapshot or history, when operation is `merge`, dataset-path is the history data path.


### Usage Instructions
The node database is stored in the `output-directory/database` directory by default. The examples in this chapter will be explained with the default database directory.


The following three examples illustrate how to use the data pruning tool:

* **Split and get a `Snapshot Dataset`**
    
    This function can split FullNode data into Lite Fullnode data, and can also be used to regularly trim Lite Fullnode data. The steps are as follows:
    
    First, stop the FullNode and execute:

    ```shell
    # just for simplify, save the snapshot into /tmp directory
    java -jar Toolkit.jar db lite -o split -t snapshot --fn-data-path output-directory/database --dataset-path /tmp
    ```

    * --fn-data-path： The data directory to be trimmed, that is, the node data directory
    * --dataset-path： The directory where the output snapshot dataset is stored

    After the command is executed, a `snapshot` directory will be generated in `/tmp`, the data in this directory is the Lite Fullnode data, then rename the directory from `snapshot` to `database` (the default value of the storage.db.directory is `database`, make sure rename the snapshot directory to the specified value) and copy the `database` directory  to the Lite Fullnode database directory to finish the splitting. Finally start the Lite Fullnode. 
    

* **Split and get a `History Dataset`**
    
    The command to split the historical data set is as follows:

    ```shell
    # just for simplify, save the history into `/tmp` directory,
    java -jar Toolkit.jar db lite -o split -t history --fn-data-path output-directory/database --dataset-path /tmp
    ```

    * --fn-data-path： FullNode data directory
    * --dataset-path： The directory where the output historical dataset is stored

    After the command is executed, the `history` directory will be generated under the `/tmp` directory, and the data in it is the historical dataset.
    
* **Merge `History Dataset` and `Snapshot Dataset`**

    Both `History Dataset` and `Snapshot Dataset` have an `info.properties` file to identify the block height when they are split. Make sure that the `split_block_num` in `History Dataset` is not less than the corresponding value in the `Snapshot Dataset`. After the historical dataset is merged with the snapshot dataset through the merge operation, the Lite Fullnode will become a real FullNode.

    The command to merge the historical dataset and the snapshot dataset is as follows:
    
    ```shell
    # just for simplify, assume `History dataset` is locate in /tmp
    java -jar Toolkit.jar db lite -o merge --fn-data-path /tmp/snapshot --dataset-path /tmp/history
    ```

    * --fn-data-path： snapshot dataset directory
    * --dataset-path： history dataset directory


    After the command is executed, the merged data will overwrite the directory where the snapshot data set is located, that is, the directory specified by `--fn-data-path`, copy the merged data to the node database directory, and the Lite Fullnode becomes a FullNode.
    
    
## Data Copy
The node database is large, and the database copy operation is time-consuming. The Toolkit provides a fast database copy function, which can quickly copy the LevelDB or RocksDB database in the same file system by creating a hard link.


### Command and parameters
To use the data copy function provided by Toolkit through `db copy` :

```
# full command
  java -jar Toolkit.jar db cp [-h] <src> <dest>
# examples
  java -jar Toolkit.jar db cp  output-directory/database /tmp/database
```

Optional command parameters are as follows:

- `<src>`: Source path for database. Default: output-directory/database
- `<dest>`: Output path for database. Default: output-directory-cp/database
- `-h | --help`：[ bool ] provide the help info. Default: false

Note: Before using this tool for any operation, you need to stop the currently running node first.

## Data Conversion
Toolkit supports database data conversion function, which can convert LevelDB data into RocksDB data.


### Command and parameters
To use the data conversion function provided by Toolkit through `db convert` command:

```
# full command
  java -jar Toolkit.jar db convert [-h] [--safe] <src> <dest>
# examples
  java -jar Toolkit.jar db convert  output-directory/database /tmp/database
```

Optional command parameters are as follows:

- `<src>`:  Input path for leveldb, default: output-directory/database.
- `<dest>`: Output path for rocksdb, default: output-directory-dst/database.
- `--safe`：In safe mode, read data from leveldb then put into rocksdb, it's a very time-consuming procedure. If not, just change engine.properties from leveldb to rocksdb, rocksdb is compatible with leveldb for the current version. This may not be the case in the future, default: false.
- `-h | --help`：[ bool ]  Provide the help info, default: false。

Note: Before using this tool for any operation, you need to stop the currently running node first.

## LevelDB Startup Optimization

with the running of levedb, the manifest file will continue to grow. Excessive manifest file will not only affect the startup speed of the node, moreover, there may be an issue that the service is terminated abnormally due to the continuous growth of memory. To solve this issue, toolkit provides the leveldb startup optimization tool. The tool optimizes the file size of the manifest and the startup process of LevelDB, reduces memory usage, and improves node startup speed.


### Command and parameters
To use the LevelDB startup optimization function provided by Toolkit through `db archive` command:

```
# full command
   java -jar Toolkit.jar db archive [-h] [-b=<maxBatchSize>] [-d=<databaseDirectory>] [-m=<maxManifestSize>]
# examples
   #1. use default settings
   java -jar Toolkit.jar db archive 
   #2. specify the database directory as /tmp/db/database
   java -jar Toolkit.jar db archive -d /tmp/db/database 
   #3. specify the batch size to 64000 when optimizing manifest
   java -jar Toolkit.jar db archive -b 64000
   #4. specify optimization only when Manifest exceeds 128M
   java -jar Toolkit.jar db archive -m 128 
```

Optional command parameters are as follows:

- `-b | --batch-size`: Specify the batch manifest size, default: 80000.
- `-d | --database-directory`: Specify the database directory to be processed, default: output-directory/database.
- `-m | --manifest-size`: Specify the minimum required manifest file size, unit: M, default: 0.
- `-h | --help`：[ bool ]  Provide the help info, default: false.

Note: Before using this tool for any operation, you need to stop the currently running node first.
