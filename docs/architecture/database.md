# Database configuration
java-tron data storage supports LevelDB or RocksDB, and LevelDB is used by default. You can also choose RocksDB, which provides lots of configuration parameters, allowing nodes to be tuned according to their own machine configuration. The node database occupies less disk space than LevelDB. At the same time, RocksDB supports data backup during runtime, and the backup time only takes a few seconds.

The following describes how to set the storage engine of the java-tron node to RocksDB, and how to perform data conversion between leveldb and rocksdb.

## RocksDB

### Configuration

Use RocksDB as the data storage engine, need to set `db.engine` to "ROCKSDB":

```
storage {
  # Directory for storing persistent data
  db.engine = "ROCKSDB",
  db.sync = false,
  db.directory = "database",
  index.directory = "index",
  transHistory.switch = "on",
```

The optimization parameters RocksDB support:

```
dbSettings = {
    levelNumber = 7
    //compactThreads = 32
    blocksize = 64  // n * KB
    maxBytesForLevelBase = 256  // n * MB
    maxBytesForLevelMultiplier = 10
    level0FileNumCompactionTrigger = 4
    targetFileSizeBase = 256  // n * MB
    targetFileSizeMultiplier = 1
  }
```

### Use RocksDB's data backup function

Choose RocksDB to be the data storage engine, you can use its data backup function while running:

```
backup = {
    enable = false  // indicate whether enable the backup plugin
    propPath = "prop.properties" // record which bak directory is valid
    bak1path = "bak1/database" // you must set two backup directories to prevent application halt unexpected(e.g. kill -9).
    bak2path = "bak2/database"
    frequency = 10000   // indicate backup db once every 10000 blocks processed.
  }
```

**Note:** FullNode can use data backup function. In order not to affect SuperNode's block producing performance, SuperNode does not support backup service, but SuperNode's backup service node can use this function.

### Convert LevelDB to RocksDB

The data storage structure of LevelDB and RocksDB is not compatible, please make sure the node use the same type of data engine all the time. We provide data conversion script which can convert LevelDB data to RocksDB data.

Usage:

```console
> cd /path/to/java-tron/source-code
> ./gradlew build  # build the source code
> java -jar build/libs/DBConvert.jar  # run data conversion command
```

**Note:** If the node's data storage directory is self-defined, before run DBConvert.jar, you need to add the following parameters:

- **src_db_path**: specify LevelDB source directory, default output-directory/database
- **dst_db_path**: specify RocksDb source directory, default output-directory-dst/database

Example, if you run the script like this:

```console
> nohup java -jar FullNode.jar -d your_database_dir </dev/null &>/dev/null &
```

then, you should run DBConvert.jar this way:

```console
> java -jar build/libs/DBConvert.jar your_database_dir/database output-directory-dst/database
```

**Note:** You have to stop the running of the node, and then to run the data conversion script.

If you do not want to stop the running of the node for too long, after node is shut down, you can copy leveldb's output-directory to the new directory, and then restart the node. Run DBConvert.jar in the previous directory of the new directory, and specify the parameters: `src_db_path` and `dst_db_path`.

Example:

```console
> cp -rf output-directory /tmp/output-directory
> cd /tmp
> java -jar DBConvert.jar output-directory/database output-directory-dst/database
```

All the whole data conversion process may take 10 hours.

## LevelDB

You can refer to the following documents for detailed information about [RocksDB vs LevelDB](https://github.com/tronprotocol/documentation/blob/master/TRX/Rocksdb_vs_Leveldb.md)
