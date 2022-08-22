# Database Partition Tool

As the data on the chain continues to grow, the pressure on data storage will increase. At present, the FullNode data of the TRON public chain is close to 1T, and the daily data growth is about 1.2G. According to the current data growth rate, the annual growth rate is about 450G. A single disk capacity may be insufficient and need to be replaced by a larger disk. To solve it, a database storage partition tool has been introduced in `GreatVoyage-v4.5.2 (Aurelius)`. The tool can migrate some databases to other storage disks. When the user encounters insufficient disk space, he only needs to add another disk according to the capacity requirement and does not need to replace the original disk.

## Compile
Under the java-tron project directory, execute the command `./gradlew build -x test` to compile the tool, and the tool will be generated in `build/libs/Toolkit.jar`.

  
## Options

This tool provides data migration and storage functions. The optional command parameters are as follows:

- `-c | --config`: [ string ]  This option is used to specify the FullNode configuration file. If not specified, the default value will be `config.conf`.
- `-d | --database-directory`: [ string ]  This option is used to specify the FullNode database directory. If not specified, the default value will be `output-directory`.
- `-h | --help`: [ bool ]  This option is used to view help description, default value: false.



## Usage Instructions
Follow the following steps to use the database partition tool:

1. [Stop FullNode service](#stop-fullnode-service)
2. [Configure for database storage migration](#configure-for-database-storage-migration)
3. [Perform database migration](#perform-database-migration)
4. [Restart FullNode service](#restart-fullnode-service)


### Stop FullNode Service

Use the command `kill -15 pid` to close FullNode.jar, below is the FullNode process pid lookup command:
```
$ ps -ef |grep FullNode.jar |grep -v grep |awk '{print $2}'`
```


### Configure For Database Storage Migration

The configuration of database migration is in the [storage.properties](https://github.com/tronprotocol/tron-deployment/blob/master/main_net_config.conf#L37) field in the Java-tron node configuration file. The following is an example of migrating only the `block` and `trans` databases to illustrate how to migrate some databases to other storage disks:

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


### Perform Database Migration

When executed, the current migration progress will be shown.

```bash
$ java -jar Toolkit.jar db mv -c main_net_config.conf -d /data/tron/output-directory
```

### Restart FullNode Service
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
