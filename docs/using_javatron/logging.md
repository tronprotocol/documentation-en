# Node Logging

java-tron uses Logback for node application logging. Starting with GreatVoyage-v4.8.2, logs emitted through Java Util Logging (JUL), including grpc-java diagnostics, are bridged into Logback so that node operators can control them with the same logging configuration. JVM-generated output, such as garbage-collection logs, is configured separately through JVM startup options.

## Default log files

The bundled Logback configuration writes different categories of runtime output to separate files:

| File | Contents |
| --- | --- |
| `./logs/tron.log` | Main node lifecycle, synchronization, P2P, API, consensus, and operational diagnostics |
| `./logs/db/db.log` | Logs routed through the dedicated `LEVELDB` and `ROCKSDB` loggers |
| `./logs/grpc/grpc.log` | grpc-java transport and protocol diagnostics routed through `io.grpc` |

Each default rolling file appender rolls over daily and when its active file reaches approximately 500 MB. For each appender, archived files are compressed with gzip and retained for up to seven daily periods, subject to a 50 GB archive size cap.

The console appender is defined but is not attached to the root logger by default.

The `LEVELDB` and `ROCKSDB` loggers write directly to `db.log` through the `DB` appender, without an asynchronous queue. The gRPC `GRPC` appender uses a non-blocking queue of 1,024 events. If the queue is full, new gRPC log events may be dropped instead of blocking gRPC threads. By contrast, the main `ASYNC` appender uses a queue of 100 events and blocks producers when its queue is full. Setting the gRPC appender's `discardingThreshold` to `0` prevents priority-based early discarding, but does not prevent drops when the non-blocking queue is full.

## JVM garbage-collection log

Garbage-collection logging is produced by the JVM and is independent of java-tron's Logback configuration. A GC log is created only when GC logging is enabled through JVM startup options.

For ARM64 with JDK 17, the options provided with java-tron include:

```text
-Xlog:gc,gc+heap:file=gc.log:time,tags,level:filecount=10,filesize=100M
```

This configuration writes GC and heap events to `gc.log`, rotates the log when it reaches 100 MB, and retains up to 10 rotated files in addition to the active `gc.log`.

For x86_64 with JDK 8, the options provided with java-tron include:

```text
-XX:+PrintGCDetails
-XX:+PrintGCDateStamps
-Xloggc:gc.log
```

This configuration writes detailed GC events with timestamps to `gc.log`. Unlike the JDK 17 configuration, these options do not configure size-based rotation or retention. The file continues to grow until it is rotated or archived externally.

For both JDK 8 and JDK 17, the relative `gc.log` path is resolved against the process working directory, not the directory containing `FullNode.jar`.

Follow the GC log with:

```bash
tail -f ./gc.log
```

Starting the node directly with `java -jar FullNode.jar` does not create a GC log unless an appropriate JVM logging option is supplied.

## Follow node logs

Use the main log to follow block synchronization and general node status:

```bash
tail -f ./logs/tron.log
```

For a gRPC connection, transport, or TLS problem, follow the dedicated gRPC log instead:

```bash
tail -f ./logs/grpc/grpc.log
```

To follow storage-engine diagnostics routed to the dedicated database logger, use:

```bash
tail -f ./logs/db/db.log
```

## Use a custom Logback configuration

Use the `logback.xml` bundled with the same java-tron version as the node as the starting point. The current reference file is [`framework/src/main/resources/logback.xml`](https://github.com/tronprotocol/java-tron/blob/master/framework/src/main/resources/logback.xml).

Start the node with the custom file:

```bash
java -jar FullNode.jar --log-config /absolute/path/to/logback.xml
```

If `--log-config` is omitted, java-tron uses the bundled Logback configuration. If the option is specified, its value must identify a readable regular file; otherwise, the node fails during startup.

A custom Logback configuration replaces the bundled configuration. Include any appenders and shutdown hooks required by your deployment, such as the dedicated gRPC appender, the Prometheus `METRICS` appender, and `TronLogShutdownHook`.

## Send logs to stdout

The default file defines a `CONSOLE` appender. Attach it to the root logger to write to both stdout and the main log:

```xml
<root level="INFO">
  <appender-ref ref="CONSOLE"/>
  <appender-ref ref="ASYNC"/>
  <appender-ref ref="METRICS"/>
</root>
```

To write the main node log to stdout only, omit the `ASYNC` reference. Keep `METRICS` if the node exposes Prometheus metrics and `tron:error_info_total` is used for alerting.

The default `CONSOLE` appender has an `INFO` threshold. To display `DEBUG` or `TRACE` events on stdout, lower the threshold of that appender filter or remove the filter, as well as changing the applicable logger level.

## Shutdown and log flushing

The default `TronLogShutdownHook` waits for application shutdown to complete before stopping Logback, up to a maximum wait window of 180 seconds. The main and gRPC asynchronous appenders then allow up to five seconds to drain their queues.

A forced process termination such as `kill -9`, a JVM crash, or an operating-system failure bypasses normal shutdown hooks and can still lose buffered log entries.

## Log-derived Prometheus metric

When Prometheus monitoring is enabled, the default `METRICS` appender attached to the root logger increments `tron:error_info_total` for `ERROR` events that reach the root logger. Its labels are the logger name and exception type.

Dedicated non-additive loggers do not propagate to the root logger. In the default configuration, `LEVELDB`, `ROCKSDB`, and `io.grpc` are non-additive. `ERROR` events written only to `db.log` or `grpc.log` therefore do not increment `tron:error_info_total`. The additive `DB` logger still propagates to the root and is counted. Treat the metric as a signal for root-propagated application errors, not as a count of every `ERROR` log entry across all log files. See [Node Monitoring](metrics.md) for Prometheus setup.

## Adjust log levels for troubleshooting

Change log levels only when troubleshooting a specific component, and restore the default levels after collecting the required diagnostics.

The root logger and many java-tron module loggers default to `INFO`. A module with an explicitly configured level does not inherit the root level, so update the relevant module logger when tuning its output.

For example, reduce P2P network output to `WARN` and above:

```xml
<logger name="net" level="WARN"/>
```

When Prometheus monitoring is enabled, java-tron collects database statistics at startup and then every six hours. Enable their debug output in the main log with:

```xml
<logger name="metrics" level="DEBUG"/>
```

The `io.grpc` logger is non-additive and writes only through the `GRPC` appender by default. Change its own level to control `grpc.log`:

```xml
<logger name="io.grpc" level="WARN" additivity="false">
  <appender-ref ref="GRPC"/>
</logger>
```

Avoid enabling `DEBUG` or `TRACE` globally on a production node for long periods. These levels can produce substantial log volume.
