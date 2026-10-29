# java-tron Node Metrics Monitoring

Starting from the GreatVoyage-4.5.1 (Tertullian) version, java-tron nodes expose metrics in the Prometheus exposition format on a `/metrics` endpoint, allowing node operators to monitor node health more conveniently. For the meaning of each exposed metric, see the [All Metrics section](https://github.com/tronprotocol/tron-docker/blob/main/metric_monitor/README.md#all-metrics) of the tron-docker metric_monitor README. To monitor various node metrics, you must first deploy a Prometheus service to communicate with the java-tron node and scrape metric data from this endpoint. Then you need to deploy a visualization tool, such as Grafana, to display the node data obtained by Prometheus in the form of a graphical interface. The following will introduce the deployment process of the java-tron node monitoring system in detail.

## Configure java-tron

To use Prometheus for monitoring, you must first enable Prometheus metric monitoring and set the HTTP port in your node's configuration file. Locate the `node.metrics` block in `config.conf` and set `prometheus.enable` to `true`:

```properties
node.metrics = {
  prometheus {
    enable = true
    port = 9527
  }
}
```

Prometheus monitoring is disabled by default. When enabled, it listens on port `9527` by default; the listening port can be changed through `node.metrics.prometheus.port`.

For details about Prometheus and legacy monitoring settings, see [Event subscription and monitoring](configuration.md#event-subscription-and-monitoring).

## Start the java-tron Node

After updating the configuration, start the node as described in [Starting a java-tron Full Node](installing_javatron.md#starting-a-java-tron-node).

## Deploy Prometheus Service

[Prometheus](https://prometheus.io/download/) officially provides precompiled binaries and Docker images. You can download them directly from the official website or pull the images from Docker Hub. For more detailed installation and configuration instructions, please refer to the [Prometheus documentation](https://prometheus.io/docs/introduction/overview/). For this guide, we will use Docker for a simple deployment:

1. Install Prometheus

    After installing Docker, enter the following command to pull the Prometheus image:

    ```bash
    docker pull prom/prometheus
    ```

2. Prepare the Prometheus configuration file

    The following is a Prometheus configuration file template `prometheus.yaml`:

    ```yaml
    global:
      scrape_interval: 30s
      scrape_timeout: 10s
      evaluation_interval: 30s
    scrape_configs:
    - job_name: java-tron
      honor_timestamps: true
      scrape_interval: 3s
      scrape_timeout: 2s
      metrics_path: /metrics
      scheme: http
      follow_redirects: true
      static_configs:
      - targets:
        - 192.0.2.10:9527
        labels:
          group: group-xxx
          instance: xxx-01
      - targets:
        - 192.0.2.20:9527
        labels:
          group: group-xxx
          instance: xxx-02
    ```

    This example monitors two java-tron nodes running on separate remote hosts. The IP addresses `192.0.2.10` and `192.0.2.20` are placeholders; replace them with the actual IP addresses or hostnames of your nodes and use each node's configured Prometheus metrics port. Save the file to a local directory, for example `/Users/test/deploy/prometheus/prometheus.yaml`.

3. Start a Prometheus container

    Start a Prometheus container with the following command, mounting the configuration file from the previous step (`/Users/test/deploy/prometheus/prometheus.yaml`):
    
    ```bash
    docker run --name prometheus \
        -d -p 9090:9090 \
        -v /Users/test/deploy/prometheus/prometheus.yaml:/etc/prometheus/prometheus.yml \
        prom/prometheus:latest
    ```

    After the container starts, you can view the running status of the Prometheus service at `http://localhost:9090/`.

    The addresses and number of targets shown in the following screenshots are examples and may differ from your configuration.

    Go to "Status" -> "Configuration" to verify that the container is using the correct configuration file:

    ![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/metrics_config.png)

    Click "Status" -> "Targets" to view the status of each monitored java-tron node:

    ![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/metrics_targets.png)

    In the example above, the status of the first endpoint is UP, meaning Prometheus can successfully fetch data from the node. The second endpoint shows DOWN, indicating an error (hover over the error label for details).

    When the status of the monitored java-tron nodes is normal, you can monitor the metrics through visualization tools such as Grafana. This article will use Grafana to display the data:

## Deploy Grafana

The deployment process of the Grafana visualization tool is as follows:

> **Grafana UI version note:** The Grafana interface may vary between versions. The screenshots and instructions below may not reflect the latest version. For up-to-date instructions, refer to the [Grafana Prometheus data source documentation](https://grafana.com/docs/grafana/latest/datasources/prometheus/configure/).

1. Install Grafana

    Please refer to the official documentation to install [Grafana](https://grafana.com/docs/grafana/latest/setup-grafana/installation/). This article uses the Docker image deployment, pulling the open source image (`grafana/grafana`):
    
    ```bash
    docker pull grafana/grafana
    ```

2. Start Grafana

    You can use the following command to start Grafana:

    ```bash
    docker run -d --name=grafana -p 3000:3000 grafana/grafana
    ```

3. Log in to the Grafana web UI

    After startup, log in to the Grafana web UI at `http://localhost:3000/`. The default username and password are both `admin`. After login, change the password according to the prompts, and then you can enter the main interface. Click "Connections" in the left-side menu and select "Data sources" to configure Grafana's data sources. Add a Prometheus data source.

    Enter the IP address and port of the Prometheus service in "Prometheus server URL". The URL shown is an example; use the address of your Prometheus service.

    ![Grafana Connections and Prometheus data source configuration](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/metrics_prometheus.png)
    
    Click the "Save & test" button at the bottom of the page. Grafana will test the connection and display a confirmation message if the test succeeds.

4. Import Dashboard

    For the convenience of java-tron node deployers, the TRON community provides a set of pre-configured Grafana dashboards, each provided as a JSON file. Refer to the [Import dashboard section](https://github.com/tronprotocol/tron-docker/blob/main/metric_monitor/README.md#import-dashboard) of the tron-docker metric_monitor README to import them into Grafana.

    > **Note:** The `node-exporter-full.json` dashboard displays host resource metrics, such as CPU, memory, disk, and network usage. It requires Node Exporter to be deployed separately on the host you want to monitor and configured as a scrape target in Prometheus. The java-tron metrics endpoint alone does not provide the metrics required by this dashboard. See the [official Node Exporter guide](https://prometheus.io/docs/guides/node-exporter/) for setup instructions. Skip this template if you only need the java-tron dashboards.

    Click "Dashboards" in the left-side menu, then select "New" → "Import". Click "Upload JSON file" to upload one of the JSON files mentioned above, select your Prometheus data source if prompted, and click "Import".
    
    ![Grafana Dashboards New Import menu](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/metrics_import.png)
    
    Grafana will then render the dashboard according to the imported JSON file, allowing you to monitor the running status of the node in real time.
