# Database Configuration Guide

In the TRON Java implementation (**java-tron**), the node data storage engine offers two options: **LevelDB** and **RocksDB**.

Database support varies by architecture:

- On x86_64 architecture, both LevelDB and RocksDB are supported, and the current version of RocksDB is v5.15.10.
- On arm64 architecture, only RocksDB is supported, and the current RocksDB version is v9.7.4.

Developers can choose the appropriate storage engine based on the platform environment, hardware conditions, and performance requirements.

In comparison, **RocksDB provides richer configuration parameters and generally offers higher storage efficiency**. This article introduces how to enable RocksDB and how to migrate from LevelDB to RocksDB on x86_64 platforms.

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

Key descriptions:

- `db.sync`: when `true`, the underlying engine waits for each write to be physically flushed to disk before returning — safer against power loss / hard crashes, but noticeably slower. Default `false`, in which case writes are buffered by the OS and recent ones may be lost on a crash. Honored by both LevelDB and RocksDB.
- `transHistory.switch`: when `"off"`, `TransactionHistoryStore` and `TransactionRetStore` silently drop new writes, so `gettransactioninfobyid` returns empty for any transaction processed while the switch was off. Reads of pre-existing data still work. Default `"on"`.

### 2. RocksDB Optimization Parameters

The `dbSettings` block applies only when `db.engine = "ROCKSDB"`. Under LevelDB, these values are silently ignored.

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

## Migrating from LevelDB to RocksDB on x86_64 Platforms

To migrate from LevelDB to RocksDB, use the TRON Toolkit `Toolkit.jar`.

> **Note:** The `db convert` subcommand is x86_64-only. On arm64 it prints an "unsupported architecture" message and exits without doing any work.
>
### 1. Data Conversion Steps

```
cd java-tron                                   # Source root directory
./gradlew build -xtest -xcheck                 # Compile the project
java -jar build/libs/Toolkit.jar db convert    # Perform data conversion
```

### 2. Positional Arguments

If your node uses a custom data directory, pass the LevelDB source and RocksDB destination as two positional arguments after `db convert`:

```
java -jar build/libs/Toolkit.jar db convert <src> <dst>
```

- `<src>`: LevelDB database path (default: `output-directory/database`)
- `<dst>`: RocksDB database storage path (default: `output-directory-dst/database`)

For example, if the node is run as follows:
```
nohup java -jar build/libs/FullNode.jar -d your_database_dir &
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
> **Note:** The entire data conversion process is expected to take approximately **10 hours**, depending on the data volume and disk performance.
>
## About LevelDB

LevelDB is the default data storage engine for java-tron nodes on x86_64 platforms, suitable for resource-constrained or lightweight deployment scenarios. It has a simple structure and is easy to maintain, but it is less efficient than RocksDB in terms of data compression, backup capabilities, and performance for large-scale nodes.
