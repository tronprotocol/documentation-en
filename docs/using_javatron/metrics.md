# java-tron Node Metrics Monitoring
Starting from the GreatVoyage-4.5.1 (Tertullian) version, java-tron nodes provide a series of interfaces compatible with the Prometheus protocol, allowing node operators to monitor node health more conveniently. To monitor various node metrics, you must first deploy a Prometheus service to communicate with the java-tron node, and obtain the indicator data of the node through the node interface. Then you need to deploy a visualization tool, such as Grafana, to display the node data obtained by Prometheus in the form of a graphical interface. The following will introduce the deployment process of the java-tron node monitoring system in detail.

## Configure java-tron 
To use Prometheus for monitoring, you must first enable Prometheus metric monitoring and set the HTTP port in your node's configuration file:

```
node {
  ... ...
  p2p {
    version = 11111 # 11111: mainnet; 20180622: testnet
  }
 ####### add for prometheus start.
 metrics{
  prometheus{
  enable=true 
  port="9527"
  }
 }
 ####### add for prometheus end.
}

```
## Start java-tron node

Start java-tron node using the following command：

```shell
$  java -Xmx24g -XX:+UseConcMarkSweepGC -jar build/libs/FullNode.jar -c framework/src/main/resources/config.conf
```

## Deploy prometheus service

[Prometheus](https://prometheus.io/download/) officially provides precompiled binaries and Docker images. You can download them directly from the official website or pull the images from Docker Hub. For more detailed installation and configuration instructions, Please refer to the [prometheus documentation](https://prometheus.io/docs/introduction/overview/). For this guide, we will use Docker for a simple deployment:

1. After installing docker, enter the following command to pull the Prometheus image:

    ```
    $ docker pull prom/prometheus
    ```

2. Download the Prometheus configuration file

    The following is a Prometheus configuration file template `prometheus.yaml`:
    ```
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
        - 127.0.0.1:9527
        labels:
          group: group-xxx
          instance: xxx-01
      - targets:
        - 172.0.0.2:9527
        labels:
          group: group-xxx
          instance: xxx-02
    ```
    You can use this template and modify the targets configuration item, which specifies the IP address and Prometheus port of your java-tron node(s).

3. Start a Prometheus container

    Start a Prometheus container with the following command and specify to use the user-defined configuration file in the previous step:`/Users/test/deploy/prometheus/prometheus.yaml` 
    
    ```
    $ docker run --name prometheus \
        -d -p :9090:9090 \
        -v  /Users/test/deploy/prometheus/prometheus.yaml:/etc/prometheus/prometheus.yml \
        prom/prometheus:latest
    ```

    After the container starts, you can view the running status of the Prometheus service through `http://localhost:9090/`.
    
    Go to "Status" -> "Configuration" to verify that the container is using the correct configuration file:
    
     ![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/metrics_config.png)

     Click "Status" -> "Targets" to view the status of each monitored java-tron node:
     
     ![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/metrics_targets.png)
     
     In the example above, the status of the first endpoint is UP, meaning Prometheus can successfully fetch data from the node. The second endpoint shows DOWN, indicating an error (hover over the error label for details).

     When the status of the monitored java-tron nodes is normal, you can monitor the indicator data through visualization tools such as Grafana or Promdash, etc. This article will use grafana to display the data:

## Deploy Grafana
The deployment process of the Grafana visualization tool is as follows:

1. Install Grafana
    Please refer to the official documentation to install [Grafana](https://grafana.com/docs/grafana/next/setup-grafana/installation/). This article will adopt the docker image deployment, and the pulled image version is the open source version:
    
    ```
    $ docker pull grafana/grafana-oss
    ```

2. Start Grafana

    You can use the below command to start Grafana:
    ```
    $ docker run -d --name=grafana -p 3000:3000 grafana/grafana-oss
    ```

3. Log in to the Grafana web UI

    After startup, login the Grafana web UI through `http://localhost:3000/`. The default username and password are both `admin`. After login, change the password according to the prompts, and then you can enter the main interface. Click the settings icon on the left side of the main page and select "Data Sources" to configure Grafana's data sources:
    
    ![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/metrics_datasource.png)

    Enter the ip and port of the Prometheus service in `URL`:

    ![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/metrics_prometheus.png)
    
    Click the "Save & test" at the bottom of the page. Grafana will test the connection, and if successful, a 'Data source is working' notification will appear.

4. Import Dashboard

    Grafana's dashboard needs to be configured. For the convenience of java-tron node deployers, the TRON community provides a comprehensive dashboard configuration file [java-tron-template_rev1.json](https://grafana.com/grafana/dashboards/16567), which you can download directly and then import into Grafana.

     Click the Dashboards icon on the left, then select "+Import", then click "Upload JSON file" to import the downloaded dashboard configuration file:
    
    ![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/metrics_import.png)
    
    Then you can see the following types of monitoring metrics on the dashboard, and monitor the running status of the nodes in real time:
    
    ![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/metrics_dashboard.png)



