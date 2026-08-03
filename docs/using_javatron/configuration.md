# Node Configuration

java-tron uses [HOCON](https://github.com/lightbend/config/blob/main/HOCON.md) configuration files. The `-c` command-line option selects a configuration name or path; java-tron can resolve it to either a filesystem file or a resource bundled in the application.

This guide explains the current configuration model, the settings most node operators need, and when a restart is required.

## Configuration files and precedence

java-tron has two bundled configuration files with different purposes:

| File | Purpose |
|---|---|
| `common/src/main/resources/reference.conf` | Defines the complete set of default values and is always used as the fallback configuration. |
| `framework/src/main/resources/config.conf` | Provides the bundled Mainnet deployment configuration and operational overrides. It is loaded when the resolved name is `config.conf` and no corresponding filesystem file exists. |

The configuration is resolved and applied in this order:

1. The configuration name is the value passed through `-c`; if `-c` is omitted, FullNode uses the default name `config.conf`.
2. java-tron checks whether that name identifies an existing filesystem file. A relative name is resolved from the process's current working directory.
3. If the file does not exist, java-tron looks for a classpath resource with the same name. For example, `-c config.conf` can still load the `config.conf` bundled in the JAR when no filesystem `config.conf` exists.
4. If neither source exists, startup fails with a configuration-path error.
5. The selected configuration is loaded with `reference.conf` as its fallback.
6. Supported command-line parameter overrides are applied to the loaded values.
7. Platform-specific constraints are applied last.

An external configuration file, whether selected with `-c` or discovered as `./config.conf`, does **not** inherit values from the bundled `config.conf`. Therefore, a short external file may produce different behavior from the bundled configuration, even though every omitted key still receives a default from `reference.conf`.

Platform-specific constraints may override the resolved configuration. In particular, ARM64 supports only RocksDB, so java-tron forces `storage.db.engine` to `ROCKSDB` regardless of the configuration file or CLI setting.

For a production deployment, start from the current configuration template for the target network and keep its required network-specific values. The current java-tron sources are:

- [Complete defaults (`reference.conf`)](https://github.com/tronprotocol/java-tron/blob/master/common/src/main/resources/reference.conf)
- [Mainnet configuration template (`config.conf`)](https://github.com/tronprotocol/java-tron/blob/master/framework/src/main/resources/config.conf)

For Nile or another network, use the configuration template provided for that network. Peer discovery, the P2P version, seed nodes, and genesis settings must all identify the same network. See [Deploying java-tron](installing_javatron.md#network-types) for the supported network templates.

## Start a node with an external configuration

Pass the external file with `-c` and choose the node's output directory with `-d`:

```bash
java -jar FullNode.jar \
  -c /etc/java-tron/mainnet.conf \
  -d /var/lib/java-tron
```

To run a block-producing node, add `--witness`:

```bash
java -jar FullNode.jar \
  --witness \
  -c /etc/java-tron/mainnet.conf \
  -d /var/lib/java-tron
```

Command-line options override values loaded from the configuration file when both control the same behavior, subject to the platform-specific constraints described above.

HOCON accepts both nested objects and dotted keys. For example, the following is a configuration excerpt, not a complete Mainnet configuration:

```hocon
storage.db.directory = "database"

node {
  listen.port = 18888

  discovery {
    enable = true
    persist = true
  }

  http {
    fullNodeEnable = true
    fullNodePort = 8090
  }

  jsonrpc {
    httpFullNodeEnable = false
    httpFullNodePort = 8545
  }
}
```

Keep key names and value types exactly as shown in `reference.conf`. In particular, use unquoted `true` / `false` for booleans, numbers for numeric settings, quoted strings for text, and square brackets for lists.

## Network and peer configuration

The main peer-to-peer settings are:

| Configuration path | Purpose |
|---|---|
| `node.p2p.version` | Identifies the TRON network used by the P2P protocol. |
| `node.listen.port` | TCP port on which the node accepts P2P connections. |
| `node.discovery.enable` | Enables peer discovery. |
| `node.discovery.persist` | Persists discovered peers. |
| `node.discovery.external.ip` | Advertises a specific public IP address to peers. |
| `seed.node.ip.list` | Provides bootstrap peers. |
| `node.active` | Lists peers to which the node should actively maintain connections. |
| `node.passive` | Lists peer addresses trusted for incoming connections. |
| `node.maxConnections` | Limits the total number of peer connections. |
| `node.maxConnectionsWithSameIp` | Limits peer connections from one IP address. |

Open the P2P listen port in the host firewall when the node must accept inbound peers. If the node is behind NAT, make sure the advertised external address and port forwarding agree with the node configuration.

See [Connecting to the TRON network](connecting_to_tron.md) for discovery, seed, active, passive, IPv6, and connection-limit examples.

## Storage and output directories

The `-d` / `--output-directory` option selects the node's output root. `storage.db.directory` selects the database directory underneath that root. For example:

```bash
java -jar FullNode.jar -c /etc/java-tron/mainnet.conf -d /data/fullnode
```

```hocon
storage {
  db.engine = "LEVELDB"
  db.sync = false
  db.directory = "database"
}
```

With this example, the default database location is under `/data/fullnode/database`. Use a different `-d` directory for every java-tron process on the same machine. Do not point two running processes at the same database.

The `storage.properties` list can assign a separate path and LevelDB tuning values to individual databases. Each entry requires a `name`; its `path` applies to both LevelDB and RocksDB, while `blockSize`, `writeBufferSize`, `cacheSize`, and `maxOpenFiles` apply only to LevelDB.

See [Database Configuration](../architecture/database.md) before changing the database engine or performance settings. For operational data handling, see [Backup and Restore](backup_restore.md) and [Node Maintenance Tool](toolkit.md).

## API services and ports

The following defaults come from `reference.conf`. An external configuration can override each enable switch and port.

| Service | Enable switch | Port setting | Default |
|---|---|---|---|
| FullNode HTTP | `node.http.fullNodeEnable` | `node.http.fullNodePort` | Enabled, `8090` |
| Solidity HTTP | `node.http.solidityEnable` | `node.http.solidityPort` | Enabled, `8091` |
| PBFT HTTP | `node.http.PBFTEnable` | `node.http.PBFTPort` | Enabled, `8092` |
| FullNode gRPC | `node.rpc.enable` | `node.rpc.port` | Enabled, `50051` |
| Solidity gRPC | `node.rpc.solidityEnable` | `node.rpc.solidityPort` | Enabled, `50061` |
| PBFT gRPC | `node.rpc.PBFTEnable` | `node.rpc.PBFTPort` | Enabled, `50071` |
| FullNode JSON-RPC | `node.jsonrpc.httpFullNodeEnable` | `node.jsonrpc.httpFullNodePort` | Disabled, `8545` |
| Solidity JSON-RPC | `node.jsonrpc.httpSolidityEnable` | `node.jsonrpc.httpSolidityPort` | Disabled, `8555` |
| PBFT JSON-RPC | `node.jsonrpc.httpPBFTEnable` | `node.jsonrpc.httpPBFTPort` | Disabled, `8565` |

Request and message size limits are configured independently:

- `node.http.maxMessageSize` controls HTTP request bodies.
- `node.rpc.maxMessageSize` controls gRPC messages.
- `node.jsonrpc.maxMessageSize` controls JSON-RPC request bodies.
- `node.jsonrpc.maxBatchSize`, `maxResponseSize`, and filter limits constrain JSON-RPC workloads.

Use `node.disabledApi` to disable selected HTTP, gRPC, or PBFT methods. It does not disable JSON-RPC methods; disable a JSON-RPC service with its `node.jsonrpc.*Enable` switch.

Do not expose administrative or transaction-building APIs directly to an untrusted network. Restrict listening access with host or network controls, and place public services behind an appropriately configured gateway when necessary. See the [HTTP API](../api/http/index.md) and [JSON-RPC API](../api/json-rpc/index.md) guides for protocol-specific behavior.

## TVM and constant-call configuration

TVM simulation and Energy-estimation behavior is configured under `vm`:

| Configuration path | Default | Purpose |
|---|---:|---|
| `vm.supportConstant` | `false` | Enables read-only constant-contract execution. |
| `vm.maxEnergyLimitForConstant` | `100000000` | Maximum Energy available to one constant call. Values below 3,000,000 are raised to that minimum during configuration binding. |
| `vm.estimateEnergy` | `false` | Enables the dedicated `estimateenergy` implementation. |
| `vm.estimateEnergyMaxRetry` | `3` | Maximum retries while estimating Energy; values are constrained to the range 0–10. |
| `vm.constantCallTimeoutMs` | `0` | Optional execution deadline, in milliseconds, for calls routed through the constant-call path. |
| `vm.vmTrace` | `false` | Enables TVM trace output. |

`vm.constantCallTimeoutMs = 0` preserves the original behavior, in which a
constant call uses the network's `MAX_CPU_TIME_OF_ONE_TX` limit. A positive
value sets a constant-call-only deadline in milliseconds. Negative values, or
values too large to convert safely to the VM's microsecond deadline, cause
configuration loading to fail. The deadline is not enforced in debug mode or
by a standalone SolidityNode. Constant calls sent to a FullNode's
`/walletsolidity` endpoints are still subject to the deadline.

The setting applies to constant-call execution across HTTP, gRPC, and
JSON-RPC, including
[`/wallet/triggerconstantcontract`](../api/http/smart-contract/triggerconstantcontract.md),
[`/wallet/triggersmartcontract`](../api/http/smart-contract/triggersmartcontract.md)
when an ABI `view`/`pure` function is dispatched to the constant-call path,
[`/wallet/estimateenergy`](../api/http/smart-contract/estimateenergy.md),
[`eth_call`](../api/json-rpc/smart-contract/eth_call.md), and
[`eth_estimateGas`](../api/json-rpc/smart-contract/eth_estimateGas.md).

For production nodes, use `vm.constantCallTimeoutMs` when complex read-only
calls need more time. Changes to these `vm` settings require a process restart;
they are not part of dynamic configuration reload.

## Rate limiting

API limits are configured under `rate.limiter`:

- `rate.limiter.http` defines per-servlet HTTP rules.
- `rate.limiter.rpc` defines per-method gRPC rules.
- `rate.limiter.global.qps` limits total HTTP and gRPC requests.
- `rate.limiter.global.ip.qps` limits requests from one source IP.
- `rate.limiter.global.api.qps` supplies the default per-endpoint limit.
- `rate.limiter.apiNonBlocking` selects non-blocking or blocking permit acquisition.

When `rate.limiter.apiNonBlocking` is `true`, an over-limit request is rejected immediately. When it is `false`, QPS and per-IP QPS strategies block while waiting for a token. `GlobalPreemptibleAdapter` is different: it waits for a concurrency permit for at most two seconds, then rejects the request if no permit becomes available.

P2P message limits are separate and live under `rate.limiter.p2p`.

## Block production credentials

A node started with `--witness` needs access to the block producer's signing key. Prefer `localwitnesskeystore` for production deployments. `localwitness` stores a private key directly in the configuration file and therefore requires especially careful file protection.

Restrict the configuration and keystore files to the node's operating-system user, do not commit secrets to source control, and do not reuse a production key in test environments. See [Starting a Block Production Node](installing_javatron.md#starting-a-block-production-node) and [Specifying the private key with a keystore](installing_javatron.md#specifying-super-representative-account-private-key-using-keystore-password).

## Event subscription and monitoring

Event delivery is controlled by `event.subscribe`. Its settings select the native queue or event plugin, the plugin path or target server, and the enabled trigger topics. See [Event Subscription](../architecture/event.md) for a complete setup.

Prometheus monitoring is configured under `node.metrics.prometheus`, including its enable switch and listening port. See [Node Monitoring](metrics.md) for collection and dashboard instructions.

## Dynamic configuration reload

Dynamic reload is disabled by default:

```hocon
node.dynamicConfig {
  enable = true
  checkInterval = 600
}
```

`checkInterval` is measured in seconds. Use this feature with an on-disk configuration file, either selected through `-c` or discovered as `./config.conf`, because the reload service watches the selected file for modification.

Currently, a dynamic reload applies only changes to `node.active` and `node.passive`. Other settings, including ports, storage, API switches, rate limits, and `node.fastForward`, require a process restart. The successful reload messages use the `DEBUG` level and are hidden by the default `INFO` level of the `app` logger. After editing the file, enable `DEBUG` logging for the `app` logger to see the reload messages, or verify the updated peer connections through the node's runtime state.

## Validate a configuration change

Before applying a configuration in production:

1. Keep a recoverable copy of the last known-good file.
2. Check HOCON braces, commas, list syntax, key spelling, and value types.
3. Confirm that the file belongs to the intended network and contains the required network-specific overrides.
4. Confirm that every configured listening port is available and permitted by the firewall.
5. Start or restart the node and review `logs/tron.log` for configuration, binding, database, and peer-connection errors.
6. Verify block synchronization and each API that is intended to be exposed.

If a configuration edit appears to have no effect, first confirm which source was selected: the explicit `-c` path, an implicit `./config.conf`, or the bundled `config.conf`. Then restart the node unless the changed key is one of the two peer lists supported by dynamic reload.
