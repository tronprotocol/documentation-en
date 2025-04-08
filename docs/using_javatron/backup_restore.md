# Data Backup & Restore

Everything `java-tron` persists gets written inside its data directory. The default data directory is: `/output-directory/`. If you need to specify other directories, you can add `-d` or `--output-directory` parameter to the java-tron node startup command to specify the data storage location.

```
$ java -jar fullnode.jar -d ./outputdir
```

## Data Backup
Please shut down the node process before backing up the node data, for details, please refer to the following steps:

First, use the command `$ ps -ef |grep FullNode.jar |grep -v grep |awk '{print $2}'` to get the process id of java-tron, and then use the command `kill -15 process id` to kill the process. Or use a stop script like this:

```
#!/bin/bash
while true; do
  pid=`ps -ef |grep FullNode.jar |grep -v grep |awk '{print $2}'`
  if [ -n "$pid" ]; then
    kill -15 $pid
    echo "The java-tron process is exiting, it may take some time, forcing the exit may cause damage to the database, please wait patiently..."
    sleep 1
  else
    echo "java-tron killed successfully!"
    break
  fi
done
```

Then, backup the data by the following command.

```
$ tar cvzf output-directory.`date "+%Y%m%d%H%M%S"`.etgz output-directory
```

## Data Restore

When restoring the data, just copy the corresponding backup data to the node directory. Take the database backup file name `output-directory.20220628152402.etgz` as an example, the command to restore the database file is:

```
$ tar xzvf output-directory.20220628152402.etgz
```

## Public Backup Data 

For the TRON mainnet and Nile testnet, since the amount of data to be synchronized is large after the new node is started, it takes a long time to synchronize the data. In order to facilitate rapid node deployment for developers, the community provides data snapshots on a regular basis. A data snapshot is a compressed file of the database backup of a TRON network node at a certain time. Developers can download and use the data snapshot to speed up the node synchronization process.

### Main Net Data Snapshot

#### FullNode Data Snapshot

The following table shows the download address of Fullnode data snapshots. Please select a suitable data snapshot according to the location and node database type, and whether you need to query historical internal transactions.


| Fullnode Data Source | Download site | Description |
| -------- | -------- | -------- |
| Official data source (North America: Virginia)   | [http://34.86.86.229/](http://34.86.86.229/)     | LevelDB, exclude internal transactions     |
| Official data source (Singapore)    | [http://34.143.247.77/](http://34.143.247.77/)    | 	LevelDB, exclude internal transactions     |
| Official data source (North America: America)    | [http://35.197.17.205/](http://35.197.17.205/)   | RocksDB, exclude internal transactions     |
| Official data source (Singapore)    | [http://35.247.128.170/](http://35.247.128.170/)   | LevelDB, include internal transactions    |
| Official data source ((North America: Virginia))    | [http://34.48.6.163/](http://34.48.6.163/)   | LevelDB, exclude internal transactions, include account history TRX balance     |


**Note**：The data of LevelDB and RocksDB are not allowed to be mixed. The database can be specified in the config file of the full node, set db.engine to LEVELDB or ROCKSDB. 



#### Lite FullNode Data Snapshot


The TRON Public Chain has supported the type of the Lite FullNode since the version of GreatVoyage-v4.1.0 release. All the data required by the Lite FullNode for running is whole of the status data and a little essential block data, so, it is much more lightweight (smaller database and faster startup) than the normal FullNode. TRON officially offers database snapshots of the Lite FullNode.


| Lite Fullnode Data Source | Download site | Description |
| -------- | -------- | -------- |
| Official data source (Singapore)  | [http://34.143.247.77/](http://34.143.247.77/)     | LevelDB  |


**Tips**: You can split the data from the whole data with the help of the [Lite FullNode Data Pruning Tool](toolkit.md/#lite-fullnode-data-pruning).

#### Use the Data Snapshot 

The steps for using data snapshots are as follows:

1. Download the corresponding compressed backup database according to your needs.
2. Decompress the compressed file of the backup database to the output-directory directory or to the corresponding directory according to your needs.
3. Startup the node. The node reads the output-directory directory by default. If you need to specify another directory，please add the `-d directory` parameter when the node starts.


### Nile TestNet Data Snapshot
For detailed information about the Nile TestNet data snapshot, please refer to the [official website](https://nileex.io/), for both FullNode and Lite FullNode. The usage method is the same as that of the [Main Net](#use-the-data-snapshot).
