# Database Configuration Guide

In the TRON Java implementation (**java-tron**), the node data storage engine offers two options: **LevelDB** and **RocksDB**. By default, **LevelDB is used on x86 platforms, while RocksDB is used on ARM platforms**. If LevelDB is manually configured on an ARM system, the system will print a warning and still enforce the use of RocksDB. Developers can flexibly choose the appropriate storage engine based on the platform environment, hardware conditions, and performance requirements.

In comparison, **RocksDB provides richer configuration parameters and generally offers higher storage efficiency**. This article will introduce how to enable RocksDB and how to convert from LevelDB to RocksDB on x86 platforms.

## Using RocksDB

### 1. Configuring RocksDB as the Storage Engine

To enable RocksDB, set `storage.db.engine` to ``"ROCKSDB"`` in the configuration file:

```
storage {
  # Storage engine for persisting data
  db.engine = "ROCKSDB"
  db.sync = false
  db.directory = "database"
  transHistory.switch = "on"
}
```
### 2. RocksDB Optimization Parameters
RocksDB supports various tuning parameters that can be configured based on the performance of the node server. Below is an example of recommended parameters:
```
dbSettings = {
  levelNumber = 7
  # compactThreads = 32
  blocksize = 64                 # Unit: KB
  maxBytesForLevelBase = 256     # Unit: MB
  maxBytesForLevelMultiplier = 10
  level0FileNumCompactionTrigger = 4
  targetFileSizeBase = 256       # Unit: MB
  targetFileSizeMultiplier = 1
  maxOpenFiles= 5000
}
```

## Migrating from LevelDB to RocksDB on x86 Platforms
The data formats of LevelDB and RocksDB are not compatible, and direct switching of storage engines between nodes is not supported. To migrate from LevelDB to RocksDB, use the TRON Toolkit `Toolkit.jar`.
### 1. Data Conversion Steps
```
cd java-tron                                   # Source root directory
./gradlew build -xtest -xcheck                 # Compile the project
java -jar build/libs/Toolkit.jar db convert    # Perform data conversion
```
### 2. Optional Parameter Descriptions
If your node uses a custom data directory, you can include the following parameters when running the conversion script:

- `src_db_path`: LevelDB database path (default: `output-directory/database`)
- `dst_db_path`: RocksDB database storage path (default: `output-directory-dst/database`)

For example, if the node is run as follows:
```
nohup java -jar FullNode.jar -d your_database_dir &
```
Then use the following command for conversion:
```
java -jar build/libs/Toolkit.jar db convert  your_database_dir/database output-directory-dst/database
```
### 3. Perform Conversion After Stopping the Node

>**The node must be stopped before performing the data conversion operation.**

To minimize downtime, follow these steps:

1. Stop the node;
2. Copy the original LevelDB data directory to a new directory;
3. Restart the node (continuing to use the original directory);
4. Perform the data conversion in the new directory.

Example commands:
```
java -jar build/libs/Toolkit.jar db cp output-directory/database /tmp/output-directory/database
cd /tmp
java -jar build/libs/Toolkit.jar db convert output-directory/database output-directory-dst/database
```
> Note:
The entire data conversion process is expected to take approximately **10 hours**, depending on the data volume and disk performance.
## About LevelDB
LevelDB is the default data storage engine for java-tron on x86 platforms, suitable for resource-constrained or lightweight deployment scenarios. It has a simple structure and is easy to maintain, but it is less efficient than RocksDB in terms of data compression, backup capabilities, and performance for large-scale nodes.

For a detailed comparison between the two, refer to the documentation:
📘 [RocksDB vs. LevelDB Comparison](https://github.com/tronprotocol/documentation/blob/master/TRX/Rocksdb_vs_Leveldb.md)
