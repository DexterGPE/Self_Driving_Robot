# Team 3 (STILL WIP)

The repository for the Raspberry Pi robot that has to traverse an exciting and dangerous parkour!

# How to run
The git pipeline automatically deploys the code to the robot, so in order to connect to the robot and execute the code you'll have to use SSH.

```ssh pi@10.10.1.151```

When attempting to connect, the robot will ask for a password too. You should know what the password is but if you don't you'll have to ask someone for it. After that navigate to the repository, and execute the file by using the following command. (replace [filename] with the file you want to execute)

```sudo python [filename]```
The robot manual and self driving scripts are modes that can be started from the file RobotRunner.py making the default:
```sudo python RobotRunner.py```

# Other interesting things of note
Please check out the wiki, it has many interesting diagrams such as the flow diagram and will allegedly also have a class diagram and some other things!