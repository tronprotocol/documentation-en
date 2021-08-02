# Leveldb Startup Optimization Plugins

## Introduction

With the operation of levelDB, manifest file will continue to grow, huge manifest file not only affects the node startup speed, but also may cause the problem of system exit with continuous memory growth.
For this reason, leveldb startup optimization plugin is introduced since `GreatVoyage-v4.3.0(Bacon)`, which optimizes the file size of manifest and the startup process of LevelDB, reduces the memory occupation and improves the node startup speed.


Remember stop the FullNode process before any operation. This tool provides the ability to reformat the manifest according to the current `database`.

For more design details, please refer to: [TIP298](https://github.com/tronprotocol/tips/issues/298).

## Usage

### Options

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

- 1. Make sure the FullNode service is stopped.
- 2. Execute the ArchiveManifest plugin.
- 3. Start the FullNode service.

``Step ii`` is not required every time, but it is recommended to run it every time to optimize the experience.

### How to use

After FullNode runs, the default database directory: `output-directory`, the optimization plugin will work with the `output-directory/database` directory.


#### Use it Independently
batch-size: 5120，directory: /tmp/output-directory/database,minimum required manifest file size:  4M.

First, stop the FullNode and execute:

```shell
# just for simplify, locate the snapshot into `/tmp` directory,
java -jar ArchiveManifest.jar -b 5120 -d /tmp/output-directory/database -m 4
```

After the command is executed, `archive.log` will be generated in the `. /logs` directory, you can see the result.

#### Integrated startup script


```shell
#!/bin/bash

APP=$1

MANIFEST_OPT=$2

ALL_OPT=$*



rebuildManifest() {

 APP=''

 ARCHIVE_JAR='ArchiveManifest.jar'

 if [[ $1 == '-r' ]] ; then

   buildManifest

 elif [[ $2 == '-r' ]]  ; then

   buildManifest

 fi

}


buildManifest() {

 ARCHIVE_JAR='ArchiveManifest.jar'

 echo $ALL_OPT

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

 total=`cat /proc/meminfo  |grep MemTotal |awk -F ' ' '{print $2}'`

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



stopService

rebuildManifest

sleep 5

startService
```
 example
`warn`:In the above script the `-r` argument is fixed in the first or second argument (optimized in subsequent versions).
```shell
# just for simplify, locate the snapshot into `/tmp` directory,
./start.sh -r -b 5120 -d /tmp/output-directory/database -m 4
````

