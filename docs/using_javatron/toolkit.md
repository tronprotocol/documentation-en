# Toolkit: A Java-tron Node Maintenance Suite

The TRON Toolkit is a comprehensive utility that integrates various ecosystem tools for `java-tron`, designed to streamline node maintenance and management operations. We are continuously expanding its functionality in future releases to improve the developer experience. The Toolkit currently offers the following core features:

* [Database Partitioning](#database-partitioning-tool): Alleviates storage pressure caused by on-chain data growth.
* [Lite Fullnode Data Pruning](#lite-fullnode-data-pruning): Enables periodic pruning of Lite Fullnode data.
* [Fast Data Copy](#fast-data-copy-tool): Implements rapid database copying.
* [Data Conversion](#data-conversion-tool): Supports data format conversion from LevelDB to RocksDB.
* [LevelDB Startup Optimization](#leveldb-startup-optimization-tool): Accelerates the startup speed for nodes using LevelDB.
* [Merkle Root Computation](#merkle-root-computation-tool): Computes the Merkle root of a small database for verification purposes.
* [Keystore Management](#keystore-management): Generates, imports, lists, and updates account keystore files.

This document provides a detailed guide on how to acquire and use the TRON Toolkit.

**Note**: Because only RocksDB is supported on the arm64 architecture, LevelDB-specific tools like `db convert` and `db archive` can only be used on x86_64 architectures.

## Obtaining the Toolkit

You can obtain the `Toolkit.jar` file either by compiling the `java-tron` source code or by downloading a pre-compiled binary from the official releases. We recommend downloading the latest version from [GitHub Releases](https://github.com/tronprotocol/java-tron/releases).

### Compiling from Source


1. **Clone the `java-tron` source repository**：

   ```bash
   git clone https://github.com/tronprotocol/java-tron.git
   git checkout -t origin/master
   ```

2. **Build the project**：

   ```bash
   cd java-tron
   ./gradlew clean build -x test
   ```

Upon successful compilation, the `Toolkit.jar` artifact will be located in the `java-tron/build/libs/` directory.

## Command-Line Output and Exit Behavior

Toolkit uses command-specific output and exit codes. It does **not** currently provide a global JSON output option or a single error envelope shared by every command.

* When Toolkit is invoked with a command, the process exits with the integer returned by that command. Invalid command-line syntax is handled by Picocli and exits with code `2`.
* Invoking Toolkit without arguments prints the top-level usage and completes with exit code `0`.
* The `keystore` commands described below return `0` after a successful operation and normally return `1` after an execution failure. `keystore list` also returns `0` when the directory is missing or contains no keystores.
* `--json` is a per-command option supported only by `keystore new`, `keystore import`, `keystore list`, and `keystore update`. It controls successful output written to stdout. Errors and warnings remain plain text on stderr, including when `--json` is present.
* The `db` commands do not support JSON output and retain command-specific exit-code behavior. Automation must not assume a Toolkit-wide `0`/`1`/`2` contract beyond the behavior explicitly documented for a command.

For shell automation, check the exit code before parsing stdout. Do not attempt to parse stderr as JSON.

## Keystore Management

The `keystore` command group manages account keystore files in Web3 Secret Storage format. It replaces the deprecated interactive `FullNode.jar --keystore-factory` workflow.

```bash
java -jar build/libs/Toolkit.jar keystore --help
```

The default keystore directory is `Wallet` under the current working directory. Use `--keystore-dir <path>` to select another directory.

### Generate a Keystore

`keystore new` generates a random key pair and writes an encrypted keystore file:

```bash
# Interactive password entry
java -jar build/libs/Toolkit.jar keystore new

# Non-interactive password input and JSON result
java -jar build/libs/Toolkit.jar keystore new \
  --keystore-dir /data/keystores \
  --password-file /secure/path/password.txt \
  --json
```

Successful JSON output contains the generated address and filename:

```json
{"address":"T...","file":"UTC--...json"}
```

### Import a Private Key

`keystore import` imports a 32-byte private key written as 64 hexadecimal characters. A leading `0x` or `0X` is accepted.

```bash
# Interactive private-key and password entry
java -jar build/libs/Toolkit.jar keystore import

# Non-interactive import
java -jar build/libs/Toolkit.jar keystore import \
  --keystore-dir /data/keystores \
  --key-file /secure/path/private-key.txt \
  --password-file /secure/path/password.txt \
  --json
```

Successful JSON output has the same `address` and `file` fields as `keystore new`.

By default, the command refuses to import a key when a keystore for the derived address already exists in the target directory. Pass `--force` only when creating an additional keystore for the same address is intentional.

### List Keystores

`keystore list` lists structurally valid `.json` keystore files in a directory:

```bash
java -jar build/libs/Toolkit.jar keystore list --keystore-dir /data/keystores
java -jar build/libs/Toolkit.jar keystore list --keystore-dir /data/keystores --json
```

Successful JSON output wraps the results in a `keystores` array:

```json
{
  "keystores": [
    {"address":"T...","file":"UTC--...json"}
  ]
}
```

If the directory does not exist or contains no valid keystores, JSON mode returns `{"keystores":[]}` with exit code `0`. Unreadable or malformed `.json` files are skipped and may produce warnings on stderr.

`keystore list` does not decrypt each file. The displayed address is the address declared inside the keystore JSON and is not cryptographically verified by this command. Only trust keystores from sources you control.

### Update a Keystore Password

`keystore update` locates a keystore by address, decrypts it with the current password, and rewrites it with a new password through a temporary file. Toolkit attempts an atomic replacement and falls back to a regular replacement when the filesystem does not support atomic moves:

```bash
# Interactive password entry
java -jar build/libs/Toolkit.jar keystore update T... \
  --keystore-dir /data/keystores

# Non-interactive password update
java -jar build/libs/Toolkit.jar keystore update T... \
  --keystore-dir /data/keystores \
  --password-file /secure/path/passwords.txt \
  --json
```

For `update`, the password file must contain exactly two lines: the current password on the first line and the new password on the second line.

Successful JSON output contains the verified address, filename, and update status:

```json
{"address":"T...","file":"UTC--...json","status":"updated"}
```

The command fails if no matching keystore exists or if more than one valid keystore declares the requested address. It does not choose arbitrarily between duplicates.

### Keystore Options and Security

| Option | Commands | Behavior |
|---|---|---|
| `--keystore-dir <path>` | all | Keystore directory; defaults to `Wallet`. |
| `--json` | all | Writes the successful result as JSON to stdout; errors remain text on stderr. |
| `--password-file <file>` | `new`, `import`, `update` | Avoids an interactive password prompt. `new` and `import` require one line; `update` requires exactly two lines. |
| `--key-file <file>` | `import` | Reads the private key from a file instead of a terminal prompt. |
| `--force` | `import` | Allows another keystore to be created for an address already present in the directory. |
| `--sm2` | `new`, `import`, `update` | Uses SM2 instead of the default ECDSA engine. For `update`, it must match the algorithm used by the existing keystore. |

Password and private-key input files must be regular files no larger than 1,024 bytes; symbolic links are rejected. Passwords selected by `keystore new` and `keystore import`, and the new password supplied to `keystore update`, must contain at least six characters. `keystore update` does not apply this minimum to the existing password so that legacy keystores remain accessible. On POSIX systems, Toolkit creates or rewrites keystore files with owner-only `0600` permissions.

!!! warning "Protect temporary secret files"
    `--password-file` and `--key-file` make non-interactive execution possible, but the files contain secrets in plaintext. Store them outside the repository, restrict them to the current user with `chmod 600`, never commit them, and remove them when they are no longer required.


## Database Partitioning Tool

The continuous growth of TRON's on-chain data (Mainnet Fullnode database currently exceeds 2TB and grows by approximately 1.2GB daily) places increasing storage demands on nodes. To address single-disk capacity limitations, the TRON Toolkit includes a **database storage partitioning tool**. This tool enables you to migrate specific database components to different storage disks based on a configuration file. This allows you to expand storage capacity by adding new devices rather than replacing existing ones when disk space becomes insufficient.

### Command and Parameters

Use the `db mv` command to execute the data migration：

```bash
# full command
java -jar build/libs/Toolkit.jar db mv [-h] [-c=<config>] [-d=<database>]
# examples
java -jar build/libs/Toolkit.jar db mv -c framework/src/main/resources/config.conf -d /data/tron/output-directory
```

**Optional Parameters**：

*   `-c | --config <string>`: Specifies the FullNode configuration file path. Default: `config.conf`.
*   `-d | --database-directory <string>`: Specifies the FullNode database directory. Default: `output-directory`.
*   `-h | --help <boolean>`: Displays help information. Default: `false`.

### Usage Instructions

To use the database partitioning tool, follow these steps:

1. [Stop the FullNode service](#1-stop-the-fullnode-service)
2. [Configure database migration settings](#2-configure-database-storage-migration)
3. [Execute the migration command](#3-execute-the-database-migration)
4. [Restart the FullNode service](#4-restart-the-fullnode-service)


#### 1. Stop the FullNode Service

Before performing a database migration, you **must** stop the currently running FullNode service. You can use the following command to find the FullNode process ID (PID) and kill it:

```bash
kill -15 $(ps -ef | grep FullNode.jar | grep -v grep | awk '{print $2}')
```


#### 2. Configure Database Storage Migration

Database migration is configured via the `storage.properties `field in the `java-tron` node configuration file. You can find an example configuration in the [java-tron repository](https://github.com/tronprotocol/java-tron/blob/master/framework/src/main/resources/config.conf).

The following example demonstrates how to migrate the `block` and `trans` databases to the `/data1/tron` directory:


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

*   `name`：The name of the database to be migrated.
*   `path`：The target directory for the database migration.

The tool will move the database specified by `name` to the `path` directory and create a soft link in the original location pointing to the new directory. Upon restarting, the FullNode will use this link to locate the data.


#### 3. Execute the Database Migration

After configuration, run the following command to perform the migration. The command will display the current progress.

```bash
java -jar build/libs/Toolkit.jar db mv -c framework/src/main/resources/config.conf -d /data/tron/output-directory
```

#### 4. Restart the FullNode Service

Once the migration is complete, restart your `java-tron` node. 

[**FullNode Startup Command Example**](installing_javatron.md#starting-a-fullnode-on-the-tron-main-network)

[**Super Representative (SR) FullNode Startup Command Example**](installing_javatron.md#starting-a-block-production-node)

## Lite Fullnode Data Pruning

The TRON Toolkit provides a **data pruning tool** primarily used for generating and managing lite FullNode data.

A FullNode's complete data can be split into two parts: a Snapshot Dataset or a History Dataset.

* **Snapshot Dataset**: Used to start a lite FullNode. It does not contain historical data prior to the block height at the time of pruning.
* **History Dataset**: Used for querying historical data.

The Snapshot Dataset contains the latest state of the entire network plus the history of the most recent 65,536 blocks. It is far smaller than a FullNode's full database. Since a Lite Fullnode starts using only the Snapshot Dataset, it benefits from low disk usage and fast startup speeds.

The data pruning tool can split a FullNode's data into a **Snapshot Dataset** or a **History Dataset**. It also supports merging a history dataset back with a snapshot dataset. This enables the following use cases:

* **Convert FullNode Data into Lite Fullnode Data**: Split the full node data to generate a snapshot dataset, which is all that's needed to run a light node.
* **Periodically Pruning a Lite FullNode**: As a light node runs, its data grows. You can periodically prune it by using the tool to create a new, smaller snapshot dataset from the existing lite FullNode data.
* **Converting Lite FullNode Data Back to FullNode Data**: To enable historical queries on a lite FullNode, you can convert it back to a FullNode. First, split a FullNode to create a history dataset. Then, merge that history dataset with your lite FullNode's snapshot dataset to create a complete FullNode database.

> **Important Note**: Before using this tool for any operation, you need to stop the currently running node first.



### Command and Parameters

Use the `db lite` command to perform data pruning operations:

```bash
# full command
  java -jar build/libs/Toolkit.jar db lite [-h] -ds=<datasetPath> -fn=<fnDataPath> [-o=<operate>] [-t=<type>] [--exclude-historical-balance]
# examples
  #split and get a snapshot dataset
  java -jar build/libs/Toolkit.jar db lite -o split -t snapshot --fn-data-path output-directory/database --dataset-path /tmp
  #split and get a smaller snapshot without historical balance data
  java -jar build/libs/Toolkit.jar db lite -o split -t snapshot --fn-data-path output-directory/database --dataset-path /tmp --exclude-historical-balance
  #split and get a history dataset
  java -jar build/libs/Toolkit.jar db lite -o split -t history --fn-data-path output-directory/database --dataset-path /tmp
  #merge history dataset and snapshot dataset
  java -jar build/libs/Toolkit.jar db lite -o merge --fn-data-path /tmp/snapshot --dataset-path /tmp/history
```

**Optional Parameters**：

*   `-o | --operate <split | merge>`: Specifies the operation type. Default: `split`.
*   `-t | --type <snapshot | history>`：Used only with `-o split`. `snapshot` creates a snapshot dataset; `history` creates a history dataset.
*   `-fn | --fn-data-path <string>`：
    *   For `split`, this is the source directory of the data to be pruned.
    *   For `merge`, this is the directory of the lite FullNode's database (the snapshot dataset).
*   `-ds | --dataset-path <string>`：
    *   For `split`, this is the output directory for the generated snapshot or history dataset.
    *   For `merge`, this is the directory of the history dataset.
*   `--exclude-historical-balance`: Used only with `-o split -t snapshot`. Default: `false`. When enabled, the tool excludes the `balance-trace` and `account-trace` databases from the snapshot to reduce its size. `split -t history` and `merge` ignore this option.

    > **Warning:** If the source node has `storage.balance.history.lookup = true`, enabling this option permanently removes the data required for historical balance queries from the generated snapshot. A Lite FullNode started from that snapshot cannot safely serve `getblockbalance`, and `getaccountbalance` may return a balance of `0` when account trace data is unavailable. Merging a history dataset later does not restore the excluded databases. Do not enable this option if the resulting Lite FullNode must support historical balance queries.


### Usage Examples

The node database is typically located in the `output-directory/database` directory by default. The following examples will use this default directory for illustration.


#### Split to Create a Snapshot Dataset

This feature can be used to convert FullNode data into Lite FullNode data, or to periodically prune the data of a running Lite FullNode. Follow these steps:

First, stop the node, then execute the following command:

```shell
# For simplicity, the snapshot dataset will be stored in the /tmp directory
java -jar build/libs/Toolkit.jar db lite -o split -t snapshot --fn-data-path output-directory/database --dataset-path /tmp
```

* `--fn-data-path`: The source directory of the data to be pruned (the node's database directory).
* `--dataset-path`: The output directory for the generated snapshot dataset.

After the command completes, a directory named `snapshot` will be created in the `/tmp` directory. This directory contains the Lite FullNode data. To use it, copy the data from the snapshot directory to your node's database directory (e.g., rename the `snapshot` directory to database and move it to the Lite FullNode's `output-directory`), and then restart the node.

If historical balance queries are not required, you can generate a smaller snapshot by excluding the balance trace databases:

```shell
java -jar build/libs/Toolkit.jar db lite -o split -t snapshot --fn-data-path output-directory/database --dataset-path /tmp --exclude-historical-balance
```

This exclusion is permanent for the generated snapshot. Do not use it when `storage.balance.history.lookup` must remain available on the resulting Lite FullNode.



#### Split to Create a History Dataset

To split and create a history dataset, use the following command:

```bash
# For simplicity, the history dataset will be stored in the /tmp directory
java -jar build/libs/Toolkit.jar db lite -o split -t history --fn-data-path output-directory/database --dataset-path /tmp
```

*   `--fn-data-path`: The FullNode's database directory.
*   `--dataset-path`: The output directory for the generated history dataset.

After the command completes, a directory named `history` will be created in the /tmp directory, containing the generated history dataset.


#### Merge a History Dataset and a Snapshot Dataset

Both the history dataset and the snapshot dataset contain an `info.properties` file that records the block height at which the split occurred. 
> **Please Note**: To merge the two datasets, the block height of the history dataset must be greater than or equal to that of the snapshot dataset. After the `merge` operation, the Lite FullNode will be converted into a complete FullNode.

Use the following command to merge a history dataset and a snapshot dataset:

```shell
# Assuming the snapshot dataset is in /tmp/snapshot and the history dataset is in /tmp/history
java -jar build/libs/Toolkit.jar db lite -o merge --fn-data-path /tmp/snapshot --dataset-path /tmp/history
```

*   `--fn-data-path`: The directory of the snapshot dataset.
*   `--dataset-path`: The directory of the history dataset.

When the command finishes, the merged data will overwrite the snapshot dataset in the directory specified by `--fn-data-path`. Copy this merged data to your node's database directory to convert the Lite FullNode into a FullNode.
    

## Fast Data Copy Tool

Node databases are often large, and traditional copy operations can be time-consuming. The TRON Toolkit provides a **fast database copy feature** that uses hard links to efficiently copy a LevelDB or RocksDB database within a single disk partition.


### Command and Parameters

Use the `db cp` command to perform a data copy operation:

```shell
# full command
  java -jar build/libs/Toolkit.jar db cp [-h] <src> <dest>
# examples
  java -jar build/libs/Toolkit.jar db cp  output-directory/database /tmp/databse
```

**Optional Parameters**:

*   `<src>`: Specifies the source database directory. Default: `output-directory/database`.
*   `<dest>`: Specifies the target directory for the copy. Default: `output-directory-cp/database`.
*   `-h | --help <boolean>`: Displays help information. Default: `false`.

> **Important Note**: Before performing any operation with this tool, you **must** stop the currently running node.

## Data Conversion Tool

The TRON Toolkit includes a data conversion feature that allows you to convert a database from LevelDB format to RocksDB format.

### Command and Parameters

Use the `db convert` command to perform the data conversion:

```bash
# full command
  java -jar build/libs/Toolkit.jar db convert [-h] <src> <dest>
# examples
  java -jar build/libs/Toolkit.jar db convert  output-directory/database /tmp/database
```

**Optional Parameters**:

*   `<src>`: Specifies the source LevelDB data directory. Default: `output-directory/database`.
*   `<dest>`: Specifies the output directory for the RocksDB data. Default: `output-directory-dst/database`.
*   `-h | --help <boolean>`: Displays help information. Default: `false`.

> **Important Note**: Before performing any operation with this tool, you must stop the currently running node.

## LevelDB Startup Optimization Tool

As a LevelDB database operates, its `manifest` file continuously grows. An excessively large `manifest` file can slow down node startup and lead to persistent memory growth, which may cause the service to terminate unexpectedly. To solve these problems, the TRON Toolkit provides a **LevelDB Startup Optimization Tool**. It optimizes the `manifest` file size and the LevelDB startup process, reducing memory usage and accelerating node startup.

### Command and Parameters

Use the `db archive` command to perform the LevelDB startup optimization:

```bash
# full command
   java -jar build/libs/Toolkit.jar db archive [-h] [-b=<maxBatchSize>] [-d=<databaseDirectory>] [-m=<maxManifestSize>]
# examples
   #1. use default settings
   java -jar build/libs/Toolkit.jar db archive 
   #2. specify the database directory as /tmp/db/database
   java -jar build/libs/Toolkit.jar db archive -d /tmp/db/database 
   #3. specify the batch size to 64000 when optimizing manifest
   java -jar build/libs/Toolkit.jar db archive -b 64000
   #4. specify optimization only when Manifest exceeds 128M
   java -jar build/libs/Toolkit.jar db archive -m 128 
```

**Optional Parameters**:

*   `-b | --batch-size <integer>`: Specifies the batch size for `manifest` processing. Default: `80000`.
*   `-d | --database-directory <string>`: Specifies the LevelDB database directory. Default: `output-directory/database`.
*   `-m | --manifest-size <integer>`: The minimum size of the `manifest` file (in MB) to trigger the optimization. The tool will only process the file if its size exceeds this value. Default: `0`.
*   `-h | --help <boolean>`: Displays help information. Default: `false`.

> **Important Note**: Before performing any operation with this tool, you must stop the currently running node.

## Merkle Root Computation Tool

The TRON Toolkit provides a **Merkle root computation tool** that calculates the Merkle root of a specified database. This is useful for data verification and consistency checks across nodes.

> **Important Note**: This tool is intended for small databases. Running it against a large database may cause a `GC overhead limit exceeded` error.

### Command and Parameters

Use the `db root` command to compute the Merkle root:

```bash
# full command
   java -jar build/libs/Toolkit.jar db root [-h] [--db=<dbs>]... [<db>]
# examples
   #compute the merkle root of the `account` and `witness` dbs in the default database directory
   java -jar build/libs/Toolkit.jar db root --db account --db witness
   #specify the database directory
   java -jar build/libs/Toolkit.jar db root --db account /tmp/db/database
```

**Optional Parameters**:

*   `<db>`: Specifies the database directory. Default: `output-directory/database`.
*   `--db <string>`: Specifies the name of the database to compute the root for. This option can be repeated to compute roots for multiple databases.
*   `-h | --help <boolean>`: Displays help information. Default: `false`.
