# Lite FullNode
Lite FullNode runs the same code with FullNode, the difference is that Lite FullNode only starts based on state data snapshot, which only contains all account state data and historical data of the last 256 blocks. Moreover, during the running of the node, only the data related to the state data snapshot is stored, and the historical data of blocks and transactions are not saved. Therefore, Lite Fullnode has the advantages of occupying less disk space and startting up fast, but it does not provide historical block and transaction data query, and only provides part of HTTP API and GRPC API of fullnode. For APIs that are not supported by Lite Fullnode, please refer to [HTTP]( https://github.com/tronprotocol/java-tron/blob/develop/framework/src/main/java/org/tron/core/services/filter/LiteFnQueryHttpFilter.java), [GRPC](https://github.com/tronprotocol/java-tron/blob/develop/framework/src/main/java/org/tron/core/services/filter/LiteFnQueryGrpcInterceptor.java). These APIs can be forced open by configuring `openHistoryQueryWhenLiteFN = true` in the configuration file, but this is not recommended.

Therefore, if developers only need to use nodes for block synchronization, processing and broadcasting transactions, then Lite Fullnoe will be a better choice.

The deployment steps of a Lite fullnode are the same as fullnode. The difference is that the light node database needs to be obtained. You can directly download the light node data snapshot from the [public backup data](../../using_javatron/backup_restore/#lite-fullnode-data-snapshot) and use it directly; you can also use the lite fulnode tool to convert the fullnode database to lite fullnode database. The use of the light node tool will be described in detail below.


# Lite FullNode Tool

Lite FullNode Tool is used to split the database of a FullNode into a `Snapshot dataset` and a `History dataset`.

- `Snapshot dataset`: the minimum dataset for quick startup of the Lite FullNode.
- `History dataset`: the archive dataset that used for historical data queries.

Before using this tool for any operation, you need to stop the currently running FullNode process first. This tool provides the function of splitting the complete data into two datasets according to the current `latest block height` (latest_block_number). Lite FullNode launched from snapshot datasets do not support querying historical data prior to this block height. The tool also provides the ability to merge historical datasets with snapshot datasets.

For more design details, please refer to: [TIP-128](https://github.com/tronprotocol/tips/issues/128).

### Obtain Lite Fullnode Tool
LiteFullNodeTool.jar can be obtained by compiling the java-tron source code, the steps are as follows:

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

    After compiling, `LiteFullNodeTool.jar` will be generated in the `java-tron/build/libs/` directory.



### Use Lite Fullnode tool

**Options**

This tool provides independent cutting of `Snapshot Dataset` and `History Dataset` and a merge function.

- `--operation | -o`: [ split | merge ] specifies the operation as either to split or to merge
- `--type | -t`: [ snapshot | history ] is used only with `split` to specify the type of the dataset to be split; snapshot refers to Snapshot Dataset and history refers to History Dataset.
- `--fn-data-path`: FullNode database directory
- `--dataset-path`: dataset directory, when operation is `split`, `dataset-path` is the path that store the `Snapshot Dataset` or `History Dataset`,
otherwise `dataset-path` should be the `History Dataset` path.

**Examples**

Start a new FullNode using the default config, then an `output-directory` will be produced in the current directory.
`output-directory` contains a sub-directory named `database` which is the database to be split.

* **Split and get a `Snapshot Dataset`**

    First, stop the FullNode and execute:
    ```
    // just for simplify, locate the snapshot into `/tmp` directory,
    $ java -jar LiteFullNodeTool.jar -o split -t snapshot --fn-data-path output-directory/database --dataset-path /tmp
    ```
    then a `snapshot` directory will be generated in `/tmp`, pack this directory and copy it to somewhere that is ready to run a Lite Fullnode.
    Do not forget rename the directory from `snapshot` to `database`.
    (the default value of the storage.db.directory is `database`, make sure rename the snapshot to the specified value)

* **Split and get a `History Dataset`**

    If historical data query is needed, `History dataset` should be generated and merged into Lite FullNode.
    ```
    // just for simplify, locate the history into `/tmp` directory,
    $ java -jar LiteFullNodeTool.jar -o split -t history --fn-data-path output-directory/database --dataset-path /tmp
    ```
    A `history` directory will be generated in `/tmp`, pack this directory and copy it to a Lite Fullnode.
    `History dataset` always take a large storage, make sure the disk has enough volume to store the `History dataset`.

* **Merge `History Dataset` and `Snapshot Dataset`**

    Both `History Dataset` and `Snapshot Dataset` have an info.properties file to identify the block height from which they are segmented.
    Make sure that the `split_block_num` in `History Dataset` is not less than the corresponding value in the `Snapshot Dataset`.

    After getting the `History dataset`, the Lite FullNode can merge the `History dataset` and become a real FullNode.
    ```
    // just for simplify, assume `History dataset` is locate in /tmp
    $ java -jar LiteFullNodeTool.jar -o merge --fn-data-path output-directory/database --dataset-path /tmp/history
    ```