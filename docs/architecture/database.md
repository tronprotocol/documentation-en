
## Rocksdb
<h3>1. Configuration </h3>
 Use rocksdb as the data storage engine, need to set db.engine to "ROCKSDB"
 ![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/db_engine.png)
 Note: rocksdb only support db.version=2, do not support db.version=1

 The optimization parameters rocksdb support:
 ![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/rocksdb_tuning_parameters.png)

<h3>2. Use rocksdb's data backup function </h3>
 Choose rocksdb to be the data storage engine, you can use it's data backup funchtion while running
 ![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/db_backup.png)
 Note: FullNode can use data backup function. In order not to affect SuperNode's block producing performance, SuperNode does not support backup service, but SuperNode's backup service node can use this function.

<h3>3. Convert leveldb data to rocksdb data </h3>
 The data storage structure of leveldb and rocksdb is not compatible, please make sure the node use the same type of data engine all the time. We provide data conversion script which can convert leveldb data to rocksdb data.

 Usage:
```text
 cd to the source code root directory
 ./gradlew build   #build the source code
 java -jar build/libs/DBConvert.jar  #run data conversion command
```
 Note: If the node's data storage directory is self-defined, before run DBConvert.jar, you need to add the following parameters:

 **src_db_path**: specify LevelDB source directory, default output-directory/database
 **dst_db_path**: specify RocksDb source directory, default output-directory-dst/database

Example, if you run the script like this:
```text
 nohup java -jar FullNode.jar -d your_database_dir &
```
then, you should run DBConvert.jar this way:
```text
 java -jar build/libs/DBConvert.jar  your_database_dir/database  output-directory-dst/database
```
 Note: You have to stop the running of the node, and then to run the data conversion script.

 If you do not want to stop the running of the node for too long, after node is shut down, you can copy leveldb's output-directory to the new directory, and then restart the node. Run DBConvert.jar in the previous directory of the new directory, and specify the parameters: `src_db_path`和`dst_db_path`.

Example:
```text
 cp -rf output-directory /tmp/output-directory
 cd /tmp
 java -jar DBConvert.jar output-directory/database  output-directory-dst/database
```
 All the whole data conversion process may take 10 hours.

<h3>4. rocksdb vs leveldb  </h3>
you can refer to:
[rocksdb vs leveldb](https://github.com/tronprotocol/documentation/blob/master/TRX_CN/Rocksdb_vs_Leveldb.md)
[ROCKSDB vs LEVELDB](https://github.com/tronprotocol/documentation/blob/master/TRX/Rocksdb_vs_Leveldb.md)


