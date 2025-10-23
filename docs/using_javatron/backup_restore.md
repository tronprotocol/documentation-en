# Node Data Backup and Restore

java-tron nodes store their persistent data in a specified data directory, which defaults to `/output-directory/`. You can specify a different data storage location by adding the `-d` or `--output-directory` parameter to the java-tron node startup command. For example:

```
java -jar FullNode.jar -d ./outputdir
```


## Backing Up Node Data

Before backing up node data, it's crucial to **shut down the node process**. You can do this by following these steps:

First, get the PID of the java-tron process using the following command:

```
ps -ef | grep FullNode.jar | grep -v grep | awk '{print $2}'
```

Then, use the obtained PID to terminate the process. It's recommended to use the following shutdown script to safely close the java-tron process and avoid database corruption:

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

**Note:** 

- **LevelDB** and **RocksDB** data are not interchangeable. The database type for a FullNode is specified by the `db.engine` configuration item in the configuration file, with selectable values being `LEVELDB` or `ROCKSDB`.
- Internal transactions can be enabled/disabled through the configuration items `vm.saveInternalTx` or `vm.saveFeaturedInternalTx` in the configuration file. Internal transactions are saved only when `vm.saveInternalTx` is enabled. If `saveFeaturedInternalTx` is also enabled, all types of internal transactions will be saved; otherwise, only `call`, `create`, and `suicide` transactions will be saved. Affected interface: [`gettransactioninfobyid`](https://developers.tron.network/reference/gettransactioninfobyid-1)
- Historical accont balances can be enabled/disabled through the configuration item `storage.balance.history.lookup` in the configuration file. Affected interface: [`getaccountbalance`](https://developers.tron.network/reference/getaccountbalance)

#### Lite FullNode Data Snapshots

The TRON network has supported **Lite FullNode** type nodes since the GreatVoyage-V4.1.0 version. Compared to a regular FullNode, a Lite FullNode has a smaller database and faster startup speed because it only requires state data and necessary historical data to start. The table below lists the download addresses for Lite FullNode data snapshots.

| Lite FullNode Node Data Source | Download Address | Description |
| :----------------------------- | :--------------- | :---------- |
| Official Data Source (Asia: Singapore) | [http://34.143.247.77/](http://34.143.247.77/) | LevelDB data |

**Tip:** If you already have full data from a FullNode, you can use the [Lite FullNode Data Trimming Tool](toolkit.md/#lite-fullnode-data-pruning) to trim your FullNode data into Lite FullNode data yourself.


### Nile Testnet Data Snapshots

For detailed information on Nile Testnet data snapshots, please refer to the [official website](https://nileex.io/). The usage method is the same as for Mainnet data snapshots.

### Data Snapshot Usage Steps
The steps for using data snapshots are as follows:

1. Download the corresponding compressed backup database based on your needs.
2. Decompress the compressed file of the backup database to the `output-directory` directory (or specify another target directory as needed). For detailed decompression instructions, refer to the Data Snapshot Decompression Methods
 section below.
3. Start the node. The node reads data from the `output-directory` by default. If your data was decompressed into a different directory, add the `-d` parameter and specify the database directory name when starting the node.

#### Data Snapshot Download and Extraction Methods

The TRON network snapshot data size exceeds 2TB. To save disk space, we recommend using the streaming method, which downloads and extracts the data simultaneously. 

**Method 1: Streamed Download and Extract (Recommended, Saves Space)**

Create a script file named `download_snapshot.sh` and add the following content:

```bash
#!/bin/bash
wget -q -O - SNAPSHOT_URL/FullNode_output-directory.tgz | tar -zxvf -
```

Run the script:

```Text Bash
bash download_snapshot.sh
```

Note: This method avoids storing the complete compressed file and extracts the data on-the-fly, **significantly reducing disk space requirements**.

**Method 2: Full Download Before Extraction (Requires Sufficient Storage Space)**

```bash
# 1. Download the complete snapshot file
wget SNAPSHOT_URL/FullNode_output-directory.tgz

# 2. Extract the file
tar -zxvf FullNode_output-directory.tgz
```

Note: During extraction, both the compressed archive and the extracted files must be stored simultaneously. We recommend using two 3TB disks (3TB+ for the archive & 3TB+ for the extracted data. You can release the archive disk after extraction to reduce costs.).
