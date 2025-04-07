# Development Example
This article will take adding a new `setPeer` HTTP interface as an example to illustrate how to participate in the development of java-tron. Before developing, please configure the [InteliJ IDE development environment](run-in-idea.md).

Sometimes java-tron nodes may not be able to connect to peers due to network reasons, if you can add trusted nodes while the node is running, this will allow the node to connect to the peer even if the node discovery function is not working.

## Fork java-tron Repository

Fork a new repository from the [https://github.com/tronprotocol/java-tron](https://github.com/tronprotocol/java-tron) project to your personal repository, and then use the following command Clone the code locally:
    
```
$ git clone https://github.com/yourname/java-tron.git
$ git remote add upstream https://github.com/tronprotocol/java-tron.git
```
    
## Sync Repository
    
Before developing new features, please synchronize your fork repository with the upstream repository.
    
```
$ git fetch upstream 
$ git checkout develop 
$ git merge upstream/develop --no-ff
```

## Create New Branch
Pull a new branch from the `develop` branch of your own repository for local development, please refer to [branch naming convention](java-tron.md/#branch-naming-conventions). In this example, the name of the new branch is: `feature/ add-new-http-demo`.

```
$ git checkout -b feature/add-new-http-demo develop
```

## Code Development
Open the java-tron project in IDEA. Create a new servlet file in the `java-tron/framework/src/main/java/org/tron/core/services/http` directory to process HTTP requests: SetPeerServlet.java, the file should contain two functions `doGet` and `doPost`. `doGet` is used to handle http get requests and `doPost` is used to handle http post requests. If one of these types of requests is not supported, the method content can be empty.

```java
@Component
@Slf4j(topic = "API")
public class SetPeerServlet extends HttpServlet {
    protected void doGet(HttpServletRequest request, HttpServletResponse response) 
    {}
    protected void doPost(HttpServletRequest request, HttpServletResponse response) 
    {}
}
```
In this example, the setPeer request should be sent by post, so you need to add processing logic in the `doPost` method, and the content of the `doGet` method keeps empty.

The processing logic of the `doPost` method is:

1. Get the incoming parameters
2. Add peer information to the list of trusted nodes through the addPeer method
3. Return the processing result of addPeer to the front-end user

```java
@Component
@Slf4j(topic = "API")
public class SetPeerServlet extends HttpServlet {
  @Autowired
  private ChannelManager channelManager;
    
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
  ......
}
```

Put the processing logic of adding trust nodes in the `addPeer` method, which not only makes the code logic clearer, but also easier to test.

The logic of the `addPeer` method is:

1. Check the parameters the user entered to ensure that the node ip and port are not empty
2. Construct node information through `Node.instanceOf(peerIP)`
3. Make sure that the added trust node is not self
4. Add the node to the trusted node list


```java
  boolean addPeer(String peerIP) {
    try {
      if (peerIP != "") {
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
After completing the implementation of SetPeerServlet, you also need to register it in the node HTTP API service, [FullNodeHttpApiService](https://github.com/tronprotocol/java-tron/blob/develop/framework/src/main/java/org/tron/core/services/http/FullNodeHttpApiService.java) is the registration entry for the node HTTP API.

Call the `context.addServlet` method in the `start` function of the `FullNodeHttpApiService` class to register the SetPeerServlet to the service. The name of the HTTP interface is defined as `/wallet/setpeer`.

```java

public class FullNodeHttpApiService implements Service {
    ......
    @Autowired
    private SetPeerServlet setPeerServlet;
    .......
    
    @Override
    public void start() {
        ......
        context.addServlet(new ServletHolder(setPeerServlet), "/wallet/setpeer");
        .......
    }
    
}
```
Then you can debug the above code, start the java-tron node in IDEA, and interact with the node through the below Curl command in the terminal:

```curl
$ curl --location --request POST 'http://127.0.0.1:16667/wallet/setpeer' \
--header 'Content-Type: application/json' \
--data-raw '{
    "peer":"192.163.3.2:16667"
}'
```
Return:

```
Success to set trusted peer:192.163.3.2:16667
```

At this point, the code development is complete, and then you need to write unit tests for the changes. For simple changes, unit tests can be written after the development code is completed, but for larger changes, it is recommended to write unit tests at the same time as development.

## Write Unit Test

The unit test of the java-tron project is based on the JUnit framework. For the usage of JUnit, please refer to [JUnit official website](https://junit.org). The following is a brief introduction to the java-tron unit test case specification and common annotations.


### java-tron Unit Test Cases Writing Specification
When writing java-tron unit test cases, please follow the below guidelines:

* All test classes should be placed in the test directory, and the package of the test class should be consistent with the package structure of the tested code. Generally, use `Test` as the suffix of a class name
* The test method must be decorated with `@Test` and it must be `public` `void` type. Generally, `test` is used as the prefix of the method name
* Each test method in the test class must be independently testable, and there must be no dependencies between methods

### Common Annotations
The following are descriptions of some commonly used annotations. For other annotations, please refer to [JUnit official website documentation](https://junit.org).

* `@Test` - transforms a normal method into a test method
* `@Ignore` - the decorated test method will be ignored by the test runner
* `@BeforeClass` - the method will be executed before all methods, static method (only executed once globally, and it is the first running one)
* `@AfterClass` - the method will be executed after all methods, static methods ( only executed once globally, and it will be the last running one)
* `@Before` - it will be executed once before each test method
* `@After` - it will be executed once after each test method


### The Composition Of The Unit Test Class
A unit test class should contain the following three parts:

* `@Before` or `@BeforeClass` decorated function, used for initialization before test case execution
* `@After` or `@BeforeClass` decorated function, used to process data cleaning after the test case execution
* Test method decorated by `@Test`

```java
public class demoTest {

  @Before
  public void init() {
    // Initialization work before test case execution
  }
  @After
  public void destroy() {
      // Destroy work after test case execution

  }
  @Test
  public void testDemoMethod() { 
  }
}

```

For this example in the article, a new file should be created in the `framework/src/test/java/org/tron/core/services/http/` directory: SetPeerServletTest.java used to write test cases.


```java
public class SetPeerServletTest {
  private static TronApplicationContext context;
  private static Application appT;
  public static ChannelManager channelManager;
  @Before
  public void init() {
    
    Args.setParam(new String[]{}, Constant.TEST_CONF);
    context = new TronApplicationContext(DefaultConfig.class);
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
    Assert.assertFalse(setPeerServlet.addPeer("127.0.0.1"));
  }
}
```

## Code Style Check
Check the modified files one by one, and select `Check Current File` in the right-click menu. If there are code style problems, please modify them one by one according to the prompts.

![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/demo_codestyle_error.png)
Fix the code style warning in the picture, and then check the file again until there is no warning.
![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/demo_codestyle.png)

## Commit Code

Submit the code after development complete, please refer to the [commit specification](java-tron.md/#commit-messages).
```
git add .
git commit -m 'add a new http api setpeer'
```
     
Push the new branch to the personal remote repository:
     
```
git push origin feature/add-new-http-demo
```

## Submit Pull Request

Submit a pull request (PR) from your repository to `tronprotocol/java-tron`.

![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/javatron_pr.png)

