# Development Example

This document will detail the process of contributing to `java-tron` development, using the addition of a new `setPeer` HTTP API as a practical example. Before you begin, please ensure you have configured your development environment, for instance, by following the [IntelliJ IDEA Development Environment Setup Guide](run-in-idea.md).

**Background**: At times, a `java-tron` node may fail to connect to peers due to network issues. To enhance the stability of the node's network connections, we want to implement a feature that enables you to dynamically add trusted nodes while the node is running, ensuring connectivity even if the node discovery service fails.

## 1. Prepare the Development Environment

### 1.1 Fork the `java-tron` Repository

First, fork the official TRON GitHub repository, [tronprotocol/java-tron](https://github.com/tronprotocol/java-tron), to your personal GitHub account. Then, clone your forked repository to your local machine and add the `upstream` remote to track official updates:

```shell
git clone https://github.com/yourname/java-tron.git
git remote add upstream https://github.com/tronprotocol/java-tron.git
```

### 1.2 Synchronize the Repository

Before starting development on a new feature, it is crucial to synchronize your personal fork with the `upstream` repository to get the latest code updates:

```shell
git fetch upstream
git checkout develop
git merge upstream/develop --no-ff
```

### 1.3 Create a New Branch

Create a new branch from your local `develop` branch for your development work. Please follow the [branch naming conventions](java-tron.md/#branch-naming-conventions) for naming your branch. For this example, we will use `feature/add-new-http-demo` as the branch name.

```shell
git checkout -b feature/add-new-http-demo develop
```
## 2. Code Implementation: Add the `setPeer` HTTP API

Open the `java-tron` project in IntelliJ IDEA. Next, we will implement a `setPeer` HTTP API to allow users to add trusted nodes via a POST request.

### 2.1 Create `SetPeerServlet.java`

In the `java-tron/framework/src/main/java/org/tron/core/services/http` directory, create a new `Servlet` class named `SetPeerServlet.java`. This class will contain `doGet` and `doPost` methods to handle HTTP GET and POST requests, respectively. If a specific request type is not supported, you can leave the corresponding method empty.

```java
package org.tron.core.services.http;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.tron.core.net.peer.ChannelManager;
import org.tron.core.net.peer.Node;
import org.tron.core.config.CommonParameter;
import org.tron.core.Constant;
import org.tron.core.exception.BadItemException;
import org.tron.core.services.http.fullnode.PostParams;
import org.tron.core.services.http.fullnode.Util;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.net.InetAddress;
import java.net.InetSocketAddress;

import com.alibaba.fastjson.JSONObject;

@Component
@Slf4j(topic = "API")
public class SetPeerServlet extends HttpServlet {

  @Autowired
  private ChannelManager channelManager;

  protected void doGet(HttpServletRequest request, HttpServletResponse response) {
    // GETrequests are not handled in this example
  }

  protected void doPost(HttpServletRequest request, HttpServletResponse response) {
    try {
      PostParams params = PostParams.getPostParams(request);

      JSONObject jsonObject = JSONObject.parseObject(params.getParams());
      String peerIpPort = String.valueOf(jsonObject.get("peer"));

      boolean res = addPeer(peerIpPort);
      if (res) {
        response.getWriter().println("Success to set trusted peer:" + peerIpPort);
      } else {
        response.getWriter().println("Fail to set the trusted peer:" + peerIpPort);
      }

    } catch (Exception e) {
      logger.error("Exception occurs when setting peer: {}", e.getMessage());
      try {
        response.getWriter().println(Util.printErrorMsg(e));
      } catch (IOException ioe) {
        logger.error("IOException occurs when setting peer: {}", ioe.getMessage());
      }
    }
  }

  private boolean addPeer(String peerIP) {
    try {
      if (peerIP != null && !peerIP.isEmpty()) {
        Node node = Node.instanceOf(peerIP);
        if (!(CommonParameter.PARAMETER.nodeDiscoveryBindIp.equals(node.getHost())
            || CommonParameter.PARAMETER.nodeExternalIp.equals(node.getHost())
            || Constant.LOCAL_HOST.equals(node.getHost()))
            || CommonParameter.PARAMETER.nodeListenPort != node.getPort()) {

          InetAddress address = new InetSocketAddress(node.getHost(), node.getPort()).getAddress();
          channelManager.getTrustNodes().put(address, node);
          return true;
        }
      }
    } catch (Exception e) {
      logger.error("addPeer error - {}", e.getMessage());
    }
    return false;
  }
}
```

In the code above:

*   The `doPost` method handles incoming POST requests. It extracts the `peer` information (an IP address and port in `IP:Port` format) from the request parameters.
*   The `addPeer` method adds the peer to the list of trusted nodes. The logic of this function is as follows:
    1.  Check the user-provided parameters to ensure the node's IP and port are not empty.
    2.  Construct the node information using `Node.instanceOf(peerIP)`.
    3.  Ensure that the trusted node being added is not the current node itself.
    4.  Add the node to the `ChannelManager`'s trusted nodes list.

### 2.2 Register `SetPeerServlet` with the HTTP API Service

After implementing `SetPeerServlet`, you need to register it with the node's HTTP API service. The `FullNodeHttpApiService` class serves as the entry point for registering all HTTP interfaces. In its `start` method, use `context.addServlet` to register `SetPeerServlet` as an HTTP API at the endpoint `/wallet/setpeer`:

```java
package org.tron.core.services.http;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.eclipse.jetty.servlet.ServletContextHandler;
import org.eclipse.jetty.servlet.ServletHolder;
import org.tron.core.services.Service;

@Component
public class FullNodeHttpApiService implements Service {

  @Autowired
  private SetPeerServlet setPeerServlet;

  // ... other member variables and methods ...

  @Override
  public void start() {
    // ... other initialization code ...
    ServletContextHandler context = new ServletContextHandler(ServletContextHandler.SESSIONS);
    // ... other Servlet registrations ...
    context.addServlet(new ServletHolder(setPeerServlet), "/wallet/setpeer");
    // ... other startup code...
  }

  // ... other methods ...
}
```

### 2.3 Debuging and Testing

Once the code changes are complete, you can start the `java-tron` node in IntelliJ IDEA for debugging. Then, use the `curl` command in your terminal to access the newly added HTTP API:

```bash
curl --location --request POST 'http://127.0.0.1:16667/wallet/setpeer' \
--header 'Content-Type: application/json' \
--data-raw '{
    "peer":"192.163.3.2:16667"
}'
```

If the request is successful, you will receive the following response:

```text
Success to set trusted peer:192.163.3.2:16667
```
At this point, the implementation of the `setPeer` feature is complete. Next, you need to write unit tests for these changes.


## 3. Writing Unit Tests

The `java-tron` project uses the JUnit framework for unit testing. For detailed information on using JUnit, please refer to the [official JUnit documentation](https://junit.org). Below is an introduction to the specifications and common annotations for `java-tron` unit test cases.

### 3.1 `java-tron`  Unit Test Case Guidelines

When writing unit tests for `java-tron`, please adhere to the following guidelines:

* **Directory and Package Structure**: All test classes should be located in the `test` directory and maintain the same package structure as the class being tested. We recommend suffixing test class names with `Test`.
* **Test Method Definition**: Test methods must be annotated with `@Test` and declared as `public void`. We recommend prefixing method names with `test` to improve readability.
* **Method Independence**: Each method in a test class should be runnable independently. There should be no dependencies between methods, ensuring the stability and maintainability of the tests.

### 3.2 Common JUnit Annotations

The following are commonly used annotations in JUnit. For more details, please consult the [official JUnit documentation](https://junit.org).

*   `@Test`: Marks a method as a test method that will be executed by the test runner.
*   `@Ignore`: Ignores the current test method, preventing it from being executed (useful for temporarily skipping unstable or unfinished tests).
*   `@BeforeClass`: Runs once before any of the test methods in the class. Must be a `static` method (typically used for initializing shared resources).
*   `@AfterClass`: Runs once after all test methods in the class have been executed. Must be a `static` method (typically used for releasing shared resources).
*   `@Before`: Runs before each test method (used to prepare the test environment, such as initializing data).
*   `@After`: Runs after each test method (used to clean up the test environment, such as closing connections).

### 3.3 Composition of a Unit Test Class

A typical unit test class consists of the following three parts:

* **Initialization Method**: A method annotated with `@Before` or `@BeforeClass` that performs setup operations before tests are executed, such as preparing test data or configuring the environment.
* **Cleanup Method**: A method annotated with `@After` or `@AfterClass` that performs cleanup operations after tests are executed, such as releasing resources or restoring data.
* **Test Method**: A method annotated with `@Test` that contains the specific test logic to verify that the code behaves as expected.

```java
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

public class DemoTest {

  @Before
  public void init() {
    // Initialization work before the test case runs
  }

  @After
  public void destroy() {
    // Data cleanup work after the test case runs
  }

  @Test
  public void testDemoMethod() {
    // Test logic
  }
}
```

For this example, we should create a new test class file, `SetPeerServletTest.java`, in the `framework/src/test/java/org/tron/core/services/http/` directory to write the corresponding test cases.

```java
package org.tron.core.services.http;

import org.junit.After;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.tron.core.config.args.Args;
import org.tron.core.net.peer.ChannelManager;
import org.tron.core.services.http.fullnode.SetPeerServlet;
import org.tron.core.db.Manager;
import org.tron.core.db.TronApplicationContext;
import org.tron.core.Constant;
import org.tron.core.services.Application;
import org.tron.core.services.ApplicationFactory;

public class SetPeerServletTest {

  private static TronApplicationContext context;
  private static Application appT;
  public static ChannelManager channelManager;

  @Before
  public void init() {
    Args.setParam(new String[]{}, Constant.TEST_CONF);
    context = new TronApplicationContext(Manager.class);
    channelManager = context.getBean(ChannelManager.class);
    appT = ApplicationFactory.create(context);
    appT.initServices(Args.getInstance());
    appT.startServices();
    appT.startup();
  }

  @After
  public void destroy() {
    Args.clearParam();
    appT.shutdownServices();
    appT.shutdown();
  }

  @Test
  public void testAddPeer() {
    SetPeerServlet setPeerServlet = new SetPeerServlet();
    // Assuming 127.0.0.1 is the local IP, addPeer should return false
    // because it should not add itself as a trusted peer.
    Assert.assertFalse(setPeerServlet.addPeer("127.0.0.1"));
  }
}
```

## 4. CheckStyle Code Style Check

Before submitting your code, be sure to run a CheckStyle code style check on the files you have modified. In IntelliJ IDEA, you can right-click a file and select "Check Current File". Fix any code style issues based on the prompts until all warnings are resolved.

![CheckStyle 代码风格错误示例](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/demo_codestyle_error.png)

After fixing the code style issues, run the check again to ensure all warnings have been resolved:

![CheckStyle 代码风格修复后示例](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/demo_codestyle.png)

## 5. Submitting Code and Creating a Pull Request

### 5.1 Submit a Commit

After you have finished writing and testing your code, commit your changes. Please refer to the [Commit Specification](java-tron.md/#commit-messages).

```bash
git add .
git commit -m 'feat: add new http api setpeer'
```

### 5.2 Push the New Branch

Push your new branch to your personal remote repository:

```bash
git push origin feature/add-new-http-demo
```

### 5.3 Submit a Pull Request

On GitHub, create a Pull Request from your repository to `tronprotocol/java-tron`. This will propose your changes to the official repository.

![提交 Pull Request 示例](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/javatron_pr.png)

Please ensure your Pull Request description is clear and includes details about the changes you have made and their purpose.

