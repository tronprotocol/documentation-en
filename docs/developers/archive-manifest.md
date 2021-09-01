# Leveldb Startup Optimization Plugins

## Introduction

With the operation of levelDB, manifest file will continue to grow, huge manifest file not only affects the node startup speed, but also may cause the problem of system exit with continuous memory growth.
For this reason, leveldb startup optimization plugin is introduced since `GreatVoyage-v4.3.0(Bacon)`, which optimizes the file size of manifest and the startup process of LevelDB, reduces the memory occupation and improves the node startup speed.


Remember stop the FullNode process before any operation. This tool provides the ability to reformat the manifest according to the current `database`.

For more design details, please refer to: [TIP298](https://github.com/tronprotocol/tips/issues/298).

## Usage

### Options For Plug-in

- `-b | --batch-size`: [ int ]  specify the batch manifest size,default：80000.
- `-d | --database-directory`: [ string ]  Specify the database directory to be processed,default：output-directory/database.
- `-m | --manifest-size`: [ int ] Specify the minimum required manifest file size ，unit:M，default：0.
- `-h | --help`: [ bool ]  for usage help，default：false.

### How to get
- build by yourself.
  Under java-tron, execute ``. /gradlew build``, you can get ArchiveManifest.jar under `build/libs/`.
- Download directly.
  [Links](https://github.com/tronprotocol/java-tron/releases)

### Use Steps

- 1. Stop the FullNode service.
- 2. Execute the ArchiveManifest plugin.
- 3. Start the FullNode service.

> Note: ``Step ii`` is not required every time, but it is recommended to run it every time to optimize the experience.

### How to use

After FullNode runs, the default database directory: `output-directory`, the optimization plugin will work with the `output-directory/database` directory.
Developers can choose one of the following two ways  according to actual situation.

#### 1. Use it Independently

##### 1.Stop the FullNode service

Use `kill -15 ` to shutdown the FullNode.jar .

Query the pid: `ps -ef |grep FullNode.jar |grep -v grep |awk '{print $2}'`



##### 2.Execute the ArchiveManifest plugin

```shell
# Full command
java -jar ArchiveManifest.jar [-b batchSize] [-d databaseDirectory] [-m manifestSize] [-h]
# examples
   java -jar ArchiveManifest.jar #1. use default settings
   java -jar ArchiveManifest.jar -d /tmp/db/database #2. Specify the database directory as /tmp/db/database
   java -jar ArchiveManifest.jar -b 64000 #3. Specify the batch size to 64000 when optimizing Manifest
   java -jar ArchiveManifest.jar -m 128 #4. Specify optimization only when Manifest exceeds 128M
```

After the command is executed, `archive.log` will be generated in the `./logs` directory, you can see the result.

> Note: After the command is executed，If successful, the log will display something similar to the following,
> and will run generally within 120s, depending on how long the FullNode service keeps running,
> and if it fails there will be a corresponding error message
>
> `[main] [archive](ArchiveManifest.java:144) DatabaseDirectory:output-directory/database, maxManifestSize:0, maxBatchSize:80000,database reopen use 80 seconds total.`


##### 3.Start the FullNode service

```shell
 #FullNode
nohup java -Xmx24g -XX:+UseConcMarkSweepGC -jar FullNode.jar -c main_net_config.conf </dev/null &>/dev/null &
 #SR Node
nohup java -Xmx24g -XX:+UseConcMarkSweepGC  -jar FullNode.jar  -p  private key --witness -c main_net_config.conf </dev/null &>/dev/null &
```

#### 2. Integrated startup script


```shell
#!/bin/bash

APP=$1

MANIFEST_OPT=$2

ALL_OPT=$*

NEED_REBUILD=0

if [[ $1 == '--rewrite--manifest' ]]  ; then
   APP=''
   NEED_REBUILD=1

 elif [[ $2 == '--rewrite--manifest' ]]  ; then
   NEED_REBUILD=1
 fi


rebuildManifest() {

 if [[ $NEED_REBUILD == 1 ]] ; then
   buildManifest
 fi

}


buildManifest() {

 ARCHIVE_JAR='ArchiveManifest.jar'

 java -jar $ARCHIVE_JAR $ALL_OPT

 if [ $? == 0 ] ; then

     echo 'rebuild manifest success'

 else

     echo 'rebuild manifest fail, log in logs/archive.log'

 fi

}



APP=${APP:-"FullNode"}

START_OPT=`echo ${@:2}`

JAR_NAME="$APP.jar"

MAX_STOP_TIME=60

MEM_OPT=''





checkpid() {

 pid=`ps -ef | grep $JAR_NAME |grep -v grep | awk '{print $2}'`

 return $pid

}

checkPath(){
  path='output-directory/database'
  flag=1
  for p in ${ALL_OPT}
  do
   	 if [[ $flag == 0 ]] ; then
   	 	path=`echo $p`
   	 	break
   	 fi
   	 if [[ $p == '-d' || $p == '--database-directory' ]] ; then
   	 	path=''
   	 	flag=0
   	 fi
  done

  if [[ -z "${path}" ]]; then
     echo '-d /path or --database-directory /path'
     return 1
  fi

  if [[ -d ${path} ]]; then
    return 0
  else
    echo $path 'not exist'
    return 1
  fi
}



stopService() {

  count=1

  while [ $count -le $MAX_STOP_TIME ]; do

    checkpid

    if [ $pid ]; then

       kill -15 $pid

       sleep 1

    else

       echo "java-tron stop"

       return

    fi

    count=$[$count+1]

    if [ $count -eq $MAX_STOP_TIME ]; then

      kill -9 $pid

      sleep 1

    fi

  done

}

startService() {
 echo `date` >> start.log

 total=16*1024*1024

 xmx=`echo "$total/1024/1024*0.6" | bc |awk -F. '{print $1"g"}'`

 directmem=`echo "$total/1024/1024*0.1" | bc |awk -F. '{print $1"g"}'`

 logtime=`date +%Y-%m-%d_%H-%M-%S`

 export LD_PRELOAD="/usr/lib64/libtcmalloc.so"

  nohup java -Xms$xmx -Xmx$xmx -XX:+UseConcMarkSweepGC -XX:+PrintGCDetails -Xloggc:./gc.log\
  -XX:+PrintGCDateStamps -XX:+CMSParallelRemarkEnabled -XX:ReservedCodeCacheSize=256m -XX:+UseCodeCacheFlushing\
  $MEM_OPT -XX:MaxDirectMemorySize=$directmem -XX:+HeapDumpOnOutOfMemoryError -jar $JAR_NAME $START_OPT -c config.conf  >> start.log 2>&1 &

 pid=`ps -ef |grep $JAR_NAME |grep -v grep |awk '{print $2}'`

 echo "start java-tron with pid $pid on $HOSTNAME"

}

#1.Stop the FullNode service
stopService

checkPath

#2.Execute the ArchiveManifest plugin
if [[ 0 ==  $? ]] ; then
 rebuildManifest
else
 exit -1
fi

sleep 5
# Start the FullNode service
startService
```
 example
> Note: Save above script as start.sh,  In the above script the `--rewrite--manifest` argument is fixed in the first or second argument.
>
> OPTIONS
>
>            --rewrite--manifest       enable leveldb startup optimization plugins，The above plug-in option `-d -m -b -h` will take effect iff this option(--rewrite--manifest) is turned on


```shell
# Full command
./start.sh [FullNode|SolidityNode] [--rewrite--manifest] [-b batchSize] [-d databaseDirectory] [-m manifestSize]
# examples
  ./start.sh #1. Start the FullNode.jar service without the plugin
   ./start.sh SolidityNode #2. Start the SolidityNode.jar service without the plugin
   ./start.sh FullNode --rewrite--manifest #3. Execute the optimization plugin with default settings and start the FullNode.jar service
   ./start.sh --rewrite--manifest -d /tmp/db/database #4. Specify the database directory as /tmp/db/database, execute the optimization plugin, and start the FullNode.jar service
   ./start.sh --rewrite--manifest -b 64000 #5. Specify the batch size to 64000 when optimizing Manifest, and start the FullNode.jar service
   ./start.sh --rewrite--manifest -m 128 #6. Specify that optimization is performed only when the Manifest exceeds 128M, and start the FullNode.jar service
```

