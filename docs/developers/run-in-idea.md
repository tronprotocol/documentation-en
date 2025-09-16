#  IntelliJ IDEA Configuration for java-tron

To simplify the Java development process and improve efficiency, selecting and configuring an Integrated Development Environment (IDE) is a crucial first step. This guide uses IntelliJ IDEA as an example to explain how to set up and configure the java-tron development environment.

java-tron nodes support deployment on `Linux` or `MacOS` operating systems. The JDK version requirements are as follows:

- **General Requirement**: **Oracle JDK 1.8**
- **For `v4.8.1` and later**: Support is also provided for JDK 17 on the ARM architecture


## Prerequisites

Before you begin, please ensure your development environment meets the following requirements:

  - Operating System: `Linux` or `MacOS`
  - **Oracle JDK 1.8** is installed
  - `git` is installed
  - [IntelliJ IDEA](https://www.jetbrains.com/idea/download/) is installed


## Configuring the IntelliJ IDEA Environment

### Step 1: Install the Lombok Plugin

Lombok simplifies Java code through annotations and is an essential plugin for java-tron development.

1. Open IntelliJ IDEA and navigate to `Preferences` -\> `Plugins`.
2.  In the Marketplace tab, search for `Lombok`.
3.  Click `Install` and restart the IDE when prompted.

### Step 2: Enable Annotation Processing

To ensure Lombok's annotations work correctly, you must enable the annotation processor.

1. Navigate to `Preferences` -\> `Build, Execution, Deployment` -\> `Compiler` -\> `Annotation Processors`.
2. Select the `Enable annotation processing` checkbox.
3. Click **Apply** to save the settings.

![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/IDE_annotation.png)

### Step 3: Verify and Unify the JDK Version

To ensure the project compiles and runs correctly, you must set the JDK version to Oracle JDK 1.8 in two key locations within IntelliJ IDEA.


#### 1. Configure Project SDK

This is the core JDK used for compiling the project's source code and performing syntax analysis.

1. Navigate to `File` -\> `Project Structure` -\>, and select "Project" from the left panel.
2.  In the `Project SDK` dropdown menu, confirm that version `1.8` is selected.

#### 2. Configure Gradle JVM

This is the JDK used to execute Gradle build tasks (e.g., build, clean).

1. Navigate to `Preferences` -> `Build, Execution, Deployment` -> `Build Tools` -> `Gradle`.
2. In the Gradle JVM dropdown menu on the right, ensure that the selected version is also `1.8`, consistent with the Project SDK.

![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/IDE_JDK.png)

> **Important Note**: The **Project SDK** and **Gradle JVM** settings must match and both be set to Oracle JDK 1.8. Otherwise, you may encounter unexpected errors during the build process.


## Getting and Compiling the Source Code

### Step 1: Clone the Source Code

Clone the java-tron source code to your local machine and switch to the `develop` branch.

```
git clone https://github.com/tronprotocol/java-tron.git
cd java-tron
git checkout -t origin/develop
```

### Step 2: Compile java-tron

You can compile the project in two ways:

  * **Compile using the terminal:**
 
    In the root directory of the `java-tron` project, execute the following Gradle command:

    ```
    # Perform a full build, including all test cases
    ./gradlew clean build
    ```
    To speed up the compilation process by skipping unit tests, you can use the `-x test` argument:

    ```
    # Compile while skipping tests
    ./gradlew clean build -x test
    ```
  * **Compile using the IntelliJ IDEA UI:**
    
    Open the `java-tron` project in IntelliJ IDEA, then click `Build` -\> `Build Project` in the top menu bar to compile the entire project.


## Configuring Code Style Checks

java-tron adheres to the `Google checkstyle` code standard. By configuring the `Checkstyle` plugin in IDEA, you can check your code style in real-time to ensure the quality of your commits.

### Step 1: Install the Checkstyle Plugin

1.  In IDEA, navigate to `Preferences` -\> `Plugins`。
2.  In the Marketplace, search for and install the `Checkstyle` plugin.

![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/IDE_checkstyle.png)

### Step 2: Configure Checkstyle Rules

1. First, locate the code style configuration file. You can use the local `config/checkstyle/checkStyleAll.xml` file within the project, or download it from the official [GitHub Repository](https://github.com/tronprotocol/java-tron/blob/develop/config/checkstyle/checkStyleAll.xml).
2. In IDEA, navigate to `Preferences` -\> `Tools` -\> `Checkstyle` to open the configuration panel.
3. In the `Configuration File` panel, click the `+` icon to add a new configuration.
![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/IDE_checkStyleAll.png)
4. In the dialog that appears, set the  `Description` to `tron-checkstyle` and select the `checkStyleAll.xml` file you just obtained.
5. Select the checkbox for the newly added `tron-checkstyle` rule and click **Apply** and **OK**.

Once configured, you can use the `Checkstyle` plugin to check your code style. It supports various scopes, allowing you to analyze the entire project, a single module, or the file you are currently editing. The most common operation is to check the current file:

1. Right-click in the code editor.
2. Select "Check Current File".

If any code style issues are detected, `Checkstyle` will list them in a window at the bottom. Before committing your code, correct all reported issues according to the prompts to maintain codebase consistency.

![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/IDE_stylecheck.png)
   

## Running and Debugging

<a id="rndstep1"></a>
### Step 1: Create a Working Directory

Before running java-tron, you need to create a working directory to store the database and log files generated by the node at runtime.

```
mkdir /Users/javatrondeploy
```

> **Important Note**: java-tron will look for the `config.conf` file in this directory. Before starting the node, ensure you have placed the correct configuration file in this directory.


### Step 2: Configure Run/Debug Options

Next, create a new run configuration in IntelliJ IDEA to define how the IDE launches the java-tron application.

1. In the top-right corner of IDEA, click `Add Configuration...`.
2. Click `+` -\> `Application` to create a new run configuration.
3. Find and set the following options in order:
      * **Name:** Give the configuration a name, e.g. `Fullnode`.
      * **JDK**: Ensure you select `java 8 1.8`.
      * **Main Class:** Set to `org.tron.program.FullNode`.
      * **Program Arguments:** Enter the node startup arguments. For example, use `-c config.conf` to specify the configuration file.
      * **Working Directory:** Set this to the directory you created in [Step 1](#rndstep1), e.g. `/Users/javatrondeploy`。
![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/IDE_RunDebug.png)
4. Click **Apply** to save the configuration.

### Step 3: Start the Node

Now you can start the java-tron node from within IDEA:

  * **Run the node:** Click `Run` -\> `Run 'FullNode'` in the top menu bar.
![image](https://raw.githubusercontent.com/tronprotocol/documentation-zh/master/images/IDE_runjavatron.png)
  * **Debug the node:** Set breakpoints in your code, then click `Run` -\> `Debug 'FullNode'`. The program will pause at the breakpoints, allowing you to perform step-by-step debugging.
![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/IDE_debug.png)

After the node starts, relevant log files will be written to the `Working directory` you configured.
