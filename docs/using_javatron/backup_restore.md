# Node Data Backup and Restore

java-tron nodes store their persistent data in a specified data directory, which defaults to `/output-directory/`. You can specify a different data storage location by adding the `-d` or `--output-directory` parameter to the java-tron node startup command. For example:

```
java -jar fullnode.jar -d ./outputdir
```


## Backing Up Node Data

Before backing up node data, it's crucial to **shut down the node process**. You can do this by following these steps:

First, get the PID of the java-tron process using the following command:

```
ps -ef | grep FullNode.jar | grep -v grep | awk '{print $2}'
```

Then, use the obtained PID to terminate the process. It's recommended to use the following shutdown script to safely close the java-tron process and avoid database corruption:

```bash!
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

Once the java-tron process has successfully shut down, you can back up the data using the following command:

```
tar cvzf output-directory.`date "+%Y%m%d%H%M%S"`.etgz output-directory
```


## Restoring Node Data

Restoring data is straightforward: simply copy the backed-up data to the node's data directory.

If your database backup file is named `output-directory.20220628152402.etgz`, you can use the following command to restore the database files:

```
tar xzvf output-directory.20220628152402.etgz
```


## Using Public Backup Data (Data Snapshots)

For the Mainnet and Nile Testnet, new nodes require a significant amount of data to synchronize, leading to a lengthy synchronization process. To facilitate faster node deployment for developers, the TRON community regularly provides **data snapshots**.

A data snapshot is a compressed database backup file of a TRON network node at a specific point in time. Developers can significantly accelerate the node synchronization process by downloading and using these data snapshots.

### Mainnet Data Snapshots

#### FullNode Data Snapshots

The table below lists the download addresses for FullNode data snapshots. Please choose the most suitable data snapshot based on your geographical location, node database type, and whether you need to query historical internal transactions.

| FullNode Node Data Source | Download Address | Description |
| :------------------------ | :--------------- | :---------- |
| Official Data Source (Americas: Virginia, USA) | [http://34.86.86.229/](http://34.86.86.229/) | LevelDB data, does not include internal transactions |
| Official Data Source (Asia: Singapore) | [http://34.143.247.77/](http://34.143.247.77/) | LevelDB data, does not include internal transactions |
| Official Data Source (Americas: USA) | [http://35.197.17.205/](http://35.197.17.205/) | RocksDB data, does not include internal transactions |
| Official Data Source (Asia: Singapore) | [http://35.247.128.170/](http://35.247.128.170/) | LevelDB data, includes internal transactions |
| Official Data Source (Americas: Virginia, USA) | [http://34.48.6.163/](http://34.48.6.163/) | LevelDB data, does not include internal transactions, includes historical account balances |

**Note:** **LevelDB** and **RocksDB** data are not interchangeable. The database type for a FullNode is specified by the `db.engine` configuration item in the configuration file, with selectable values being `LEVELDB` or `ROCKSDB`.

#### Lite FullNode Data Snapshots

The TRON network has supported **Lite FullNode** type nodes since the GreatVoyage-V4.1.0 version. Compared to a regular FullNode, a Lite FullNode has a smaller database and faster startup speed because it only requires state data and necessary historical data to start. The table below lists the download addresses for Lite FullNode data snapshots.

| Lite FullNode Node Data Source | Download Address | Description |
| :----------------------------- | :--------------- | :---------- |
| Official Data Source (Asia: Singapore) | [http://34.143.247.77/](http://34.143.247.77/) | LevelDB data |

**Tip:** If you already have full data from a FullNode, you can use the [Lite FullNode Data Trimming Tool](https://tronprotocol.github.io/documentation-zh/using_javatron/toolkit/#_6) to trim your FullNode data into Lite FullNode data yourself.

#### Data Snapshot Decompression Methods

TRON network snapshot data typically exceeds 2TB in size. We strongly recommend using a streaming method (i.e., downloading and decompressing simultaneously) to effectively save disk space. The specific command is as follows:

```bash
wget -q -O - SNAPSHOT_URL/FullNode_output-directory.tgz | tar -zxvf -
```

##### Method 1: Stream Download and Decompress (Recommended, Saves Space)

This method does not require storing the complete compressed archive first. Instead, it directly decompresses the data into the target directory, significantly reducing disk usage.

##### Method 2: Download First, Then Decompress (Requires Ample Storage Space)

```
# 1. Download the complete snapshot file
wget SNAPSHOT_URL/FullNode_output-directory.tgz

# 2. Decompress the file
tar -zxvf FullNode_output-directory.tgz
```

This method downloads the complete snapshot file first and then decompresses it. Please note that during decompression, you will need to keep both the compressed archive and the decompressed files. Therefore, it's advisable to prepare at least two 3TB or larger disks (one for the compressed archive and one for the decompressed data. After decompression, you can free up the disk used for the compressed archive, thereby saving costs).

#### Data Snapshot Usage Steps

Whether it's a FullNode data snapshot or a Lite FullNode data snapshot, the usage steps are the same:

1.  Download the corresponding compressed backup database file based on your needs.
2.  Decompress the backed-up database compressed file into the `output-directory`. If you wish to specify another directory, you can decompress it into your designated target directory.
3.  Start the node. The node will default to reading from the `output-directory`. If your data was decompressed to another directory, add the `-d` parameter and specify the database directory name when starting the node.

### Nile Testnet Data Snapshots

For detailed information on Nile Testnet data snapshots, please refer to the [official website](https://nileex.io/). The usage method is the same as for Mainnet data snapshots.
