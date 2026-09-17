# Development Example

This document walks through a small `java-tron` contribution: adding a read-only HTTP endpoint that returns the running node's software version. The endpoint is intentionally simple so that the example can focus on the current servlet, registration, testing, and contribution patterns without introducing database or wallet dependencies.

The `/wallet/getnodeversion` endpoint used below is an illustrative example, not an API that is currently provided by `java-tron`. Before proposing a new public endpoint, open an issue or discuss the use case with the maintainers, and check whether an existing endpoint such as `/wallet/getnodeinfo` already provides the required data.

Before you begin, configure the development environment described in the [IntelliJ IDEA Development Environment Setup Guide](run-in-idea.md).

## 1. Prepare the Development Environment

### 1.1 Fork and Clone `java-tron`

Fork [tronprotocol/java-tron](https://github.com/tronprotocol/java-tron) to your GitHub account. Clone your fork, then add the official repository as the `upstream` remote:

```shell
git clone https://github.com/yourname/java-tron.git
cd java-tron
git remote add upstream https://github.com/tronprotocol/java-tron.git
```

### 1.2 Synchronize the Repository

Synchronize your local `develop` branch before starting new work:

```shell
git fetch upstream
git checkout develop
git merge upstream/develop --no-ff
```

### 1.3 Create a Branch

Create a branch from `develop`. Follow the [branch naming conventions](java-tron.md#branch-naming-conventions); this example uses `feature/add_node_version_api`:

```shell
git checkout -b feature/add_node_version_api develop
```

## 2. Add the HTTP Endpoint

The FullNode HTTP API is implemented in the `framework` module. HTTP handlers are Spring-managed components that extend `RateLimiterServlet`, and `FullNodeHttpApiService` registers them with Jetty.

### 2.1 Create `GetNodeVersionServlet.java`

Create `framework/src/main/java/org/tron/core/services/http/GetNodeVersionServlet.java`:

```java
package org.tron.core.services.http;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.springframework.stereotype.Component;
import org.tron.json.JSONObject;
import org.tron.program.Version;

@Component
public class GetNodeVersionServlet extends RateLimiterServlet {

  @Override
  protected void doGet(HttpServletRequest request, HttpServletResponse response) {
    try {
      JSONObject result = new JSONObject();
      result.put("version", Version.getVersion());
      response.getWriter().println(result.toJSONString());
    } catch (Exception e) {
      Util.processError(e, response);
    }
  }

  @Override
  protected void doPost(HttpServletRequest request, HttpServletResponse response) {
    doGet(request, response);
  }
}
```

Extending `RateLimiterServlet` integrates the endpoint with java-tron's HTTP rate limiting, metrics, JSON content type, and request-scoped JSON formatting. `@Component` makes the servlet available for Spring injection. The handler delegates error serialization to `Util.processError`, matching current HTTP API implementations.

This endpoint accepts both GET and POST for consistency with similar read-only wallet endpoints. A new endpoint should expose only the methods it actually needs.

### 2.2 Register the Servlet

Open `framework/src/main/java/org/tron/core/services/http/FullNodeHttpApiService.java` and declare a `GetNodeVersionServlet` field annotated with `@Autowired`:

```java
@Autowired
private GetNodeVersionServlet getNodeVersionServlet;
```

Then register it in the existing `addServlet(ServletContextHandler context)` method:

```java
@Override
protected void addServlet(ServletContextHandler context) {
  // Existing registrations...
  context.addServlet(
      new ServletHolder(getNodeVersionServlet), "/wallet/getnodeversion");
}
```

Do not create a second `ServletContextHandler` or override `start()` for an individual endpoint. `FullNodeHttpApiService` inherits server lifecycle management from `HttpService`; `addServlet(...)` is the extension point for route registration.

If the endpoint is intended for SolidityNode or PBFT services as well, register an appropriate handler in those services explicitly. FullNode registration does not automatically expose the route on the other service ports.

### 2.3 Exercise the Endpoint

Start a FullNode locally, then call the default FullNode HTTP port:

```bash
curl --request GET 'http://127.0.0.1:8090/wallet/getnodeversion'
```

The response contains the version compiled into the running node:

```json
{"version":"<current-java-tron-version>"}
```

If `node.http.fullNodePort` has been changed in the configuration file, use the configured port instead of `8090`.

## 3. Add Unit Tests

`java-tron` currently uses JUnit 4 for these servlet tests. Place the test in the matching package under `framework/src/test/java`.

Create `framework/src/test/java/org/tron/core/services/http/GetNodeVersionServletTest.java`:

```java
package org.tron.core.services.http;

import static org.junit.Assert.assertEquals;

import org.junit.Before;
import org.junit.Test;
import org.springframework.mock.web.MockHttpServletRequest;
import org.springframework.mock.web.MockHttpServletResponse;
import org.tron.json.JSONObject;
import org.tron.program.Version;

public class GetNodeVersionServletTest {

  private GetNodeVersionServlet servlet;

  @Before
  public void setUp() {
    servlet = new GetNodeVersionServlet();
  }

  @Test
  public void testDoGet() throws Exception {
    MockHttpServletRequest request = new MockHttpServletRequest();
    MockHttpServletResponse response = new MockHttpServletResponse();

    servlet.doGet(request, response);

    JSONObject result = JSONObject.parseObject(response.getContentAsString());
    assertEquals(200, response.getStatus());
    assertEquals(Version.getVersion(), result.getString("version"));
  }

  @Test
  public void testDoPost() throws Exception {
    MockHttpServletRequest request = new MockHttpServletRequest();
    MockHttpServletResponse response = new MockHttpServletResponse();

    servlet.doPost(request, response);

    JSONObject result = JSONObject.parseObject(response.getContentAsString());
    assertEquals(200, response.getStatus());
    assertEquals(Version.getVersion(), result.getString("version"));
  }
}
```

The test calls `doGet` and `doPost` directly, as other focused servlet tests do. Tests that exercise the inherited rate limiter or the complete Jetty route require Spring-managed dependencies and should use the corresponding integration-test infrastructure instead of constructing the servlet directly.

Run the focused test from the repository root:

```bash
./gradlew :framework:test \
  --tests org.tron.core.services.http.GetNodeVersionServletTest \
  --no-daemon
```

## 4. Run Code Quality Checks

Run Checkstyle for the modified production and test sources:

```bash
./gradlew \
  :framework:checkstyleMain \
  :framework:checkstyleTest
```

The regular build runs broader verification tasks:

```bash
./gradlew clean build --no-daemon
```

On x86_64, the project requires JDK 8 and the regular test task uses LevelDB by default. Run the focused RocksDB engine tests separately:

```bash
./gradlew :framework:testWithRocksDb --no-daemon
```

On ARM64, the project requires JDK 17 and the regular framework test task already uses RocksDB, so the additional `testWithRocksDb` command is normally unnecessary.

GitHub Actions performs additional checks that may not be practical to reproduce completely on one development machine. See [java-tron CI Workflows](workflows.md) for the trigger matrix, coverage thresholds, and branch-specific behavior.

## 5. Commit and Open a Pull Request

Commit the source and test together. Follow the [commit message specification](java-tron.md#commit-message-specifications):

```bash
git add \
  framework/src/main/java/org/tron/core/services/http/GetNodeVersionServlet.java \
  framework/src/main/java/org/tron/core/services/http/FullNodeHttpApiService.java \
  framework/src/test/java/org/tron/core/services/http/GetNodeVersionServletTest.java
git commit -m 'feat: add node version HTTP API'
```

Push the branch to your fork:

```bash
git push origin feature/add_node_version_api
```

Open a pull request from your branch to `tronprotocol/java-tron:develop`. Explain the use case, API behavior, compatibility impact, tests, and documentation updates in the pull request description. Make sure all required checks pass before requesting final review.

![Example pull request](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/javatron_pr.png)
