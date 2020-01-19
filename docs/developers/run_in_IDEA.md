# Run the FullNode with IDEA
This document aims to facilitate developers with some experience to run the FullNode with IDEA.

**The following is for the master branch of java-tron.**
## Configure IDEA
**The configuration of IDEA**
- Oracle JDK 1.8 **OpenJDK is not currently supported**

- Install Lombok plugin


![](https://raw.githubusercontent.com/cathy-lishipu/documentation-zh/idea_instruction/imags/lombok.png)

- Tick Enable annotation processing

![](https://raw.githubusercontent.com/cathy-lishipu/documentation-zh/idea_instruction/imags/annnotation.png)

## Deployment guide
**1.Create a directory** _/deploy_

```text
mkdir deploy
```

**2.Clone the latest code**

```text
git clone https://github.com/tronprotocol/java-tron
```

**3.Switch to the master branch**

```text
cd java-tron
git checkout -t origin/master
```

**4.Compile the code**

```text
./gradlew build
```

The compilation process may take some time, please be patient. If the compilation is successful, you can see the information similar to the following:

![](https://raw.githubusercontent.com/cathy-lishipu/documentation-zh/idea_instruction/imags/build_success_test.png)

If you do not want to perform unit test tasks, you can run the following command:

```text
./gradlew build -x test
```

**5.Start the FullNode**

After compiling successfully, you can find the main function file through the path java-tron / src / main / java / org / tron / program / FullNode.java and then start a full node.

![](https://raw.githubusercontent.com/cathy-lishipu/documentation-zh/idea_instruction/imags/start.png)

After starting, you can check the log to verify whether the startup is successful. The log path is: /deploy/java-tron/logs/tron.log. If the startup is successful, you can see the following logs:

![](https://raw.githubusercontent.com/cathy-lishipu/documentation-zh/idea_instruction/imags/start_success.png)

Also,you can use this command like tail -f /logs/tron.log to view the real-time log, as follows:

![](https://raw.githubusercontent.com/cathy-lishipu/documentation-zh/idea_instruction/imags/start_successed.png)
