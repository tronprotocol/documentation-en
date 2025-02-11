# Configure the IntelliJ IDEA IDE

For Java development, in order to reduce development difficulty and improve development efficiency, developers should first select and configure a Java integrated development environment, such as IntelliJ IDEA, NetBeans or Eclipse, etc. This article will take InteliJ IDEA as an example to introduce how to configure java-tron integration development environment.

This article describes the configuration of the java-tron integrated development environment in InteliJ IDEA. java-tron nodes support to be deployed on `Linux` or `MacOS` operating systems, and rely on `Oracle JDK 1.8`, other versions of JDK are not supported. Before configuring the InteliJ IDE development environment, please ensure the following prerequisites:

* Configure the development environment on `Linux` or `MacOS` operating system
* `Oracle JDK 1.8`, `git`, [InteliJ IDEA](https://www.jetbrains.com/idea/download/#section=mac) are installed 

        
## Configure InteliJ IDEA
The IntelliJ IDEA configuration steps are as follows:

* Install Lombok plugin

    Search for `lombok` in [IDEA]->[Preferences]->[Plugins] to install `Lombok` plugin, `Lombok` makes java-tron code more concise by adding annotations.

* Enable `Enable annotation processing` configuration item
      ![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/IDE_annotation.png)
* Check the JDK version and make sure that `Oracle JDK 1.8` is used in IntelliJ IDEA
      ![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/IDE_JDK.png)
  
* Download java-tron source code

    Clone the java-tron source code locally and switch to the `develop` branch.
    ```
    $ git clone https://github.com/tronprotocol/java-tron.git
    $ git checkout -t origin/develop
    ```
    

## Configure the code style check plugin
The java-tron code style needs to meet the `Google check style` specification. In IDEA, you can use the `Checkstyle` plugin to check whether the code conforms to the `Google check style` specification. The installation and configuration process of the plugin is as follows:

* Search for `checkstyle` in [IDEA]->[Preferences]->[Plugins] to install the plugin
    ![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/IDE_checkstyle.png)
    
* Code style configuration

    First, download the [java-tron code style check configuration file](https://github.com/tronprotocol/java-tron/blob/develop/config/checkstyle/checkStyleAll.xml), then in the Checkstyle configuration page, click "+ ", choose to use the "checkStyleAll.xml" just downloaded, after adding that, you can see this file in the "Configuration Files" list, and finally click "Apply" to complete the configuration.
    ![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/IDE_checkStyleAll.png)

    After configuring the `Checkstyle` plugin, you can use `Checkstyle` to check the code. `Checkstyle` can check a module or the whole project, and can also check a single file. Select "Check Current File" in the right-click menu of the file editor, and Checkstyle will check the file. If a code problem is detected, you need to modify it according to the prompts. Code can only be submitted when there are no code problems.
    ![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/IDE_stylecheck.png)
   

## Compile java-tron

You can use the terminal to compile java-tron with the following command in the java-tron project directory:

```
$ ./gradlew clean build
```
The above compile command will execute all test cases, you can use `-x test` to skip the execution of test cases:
```
$ ./gradlew clean build -x test
```

You can also compile java-tron in IDEA: Open the java-tron project in IDEA and click "Build" -> "Build Project" to compile the project.

## Run and Debug
Before running java-tron, you need to create a working directory to store the database files and log files generated when the node is running.
```
$ mkdir /Users/javatrondeploy
```

In the "Run/Debug Configurations" configuration panel, specify the JDK version running java-tron as `java 8`, and then configure the command parameters for running java-tron, for example, specify the node configuration file through the `-c` parameter as ` config.conf`.

"Working directory" is configured as the working directory of java-tron created earlier. When java-tron starts, it will look for the `config.conf` configuration file in this directory. Please make sure that `config.conf` has already been in this directory.

![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/IDE_RunDebug.png)

After the setting, click the "Apply" button to complete the configuration. Then you can click "Run"->"Run FullNode" in IDEA to start the java-tron node or click "Run"->"Debug FullNode" to start the node in debug mode. After the node is started, java-tron logs are stored in the working directory.
![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/IDE_runjavatron.png)


If you want to debug the java-tron code, you can set breakpoints in the java-tron code and start it in debug mode, so that you can trace the debug code line by line.
![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/IDE_debug.png)

