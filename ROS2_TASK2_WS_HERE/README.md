# TASK2 ACTIONS AND TURTLE SIM  QOS LAUNCH FILES IMPLEMENTATION

----------------------------------------------
1) This project has two sub parts based of ROS2 ACTIONS communication methods, one is to learn how to communicate with turtlesim by subscribing to `turtle1/pose` topic to know position and `turtle1/cmd_vel` topic to move the node using custom `msg` formats, one must also implement a logic to force the turtle to turn away from walls so it can avoid any collisions, must use a QoS protocol to ensure info safety. Also must configure a launch file to launch all the nodes at once. Use cli tools to access parameters and goals.

2) One must implement a custom action that can make the turtle in a circle and must abort in case turtle may hit the wall and with proper server and clients.

## Concepts learnt:
1) Turtlesim handling using topics to recieve position and command movement
2) learnt about QoS protocols in recieving proper information
3) configured a launch file using python and `ros2 launch launch.py` to launch all nodes at once.
4) learned to configure and use a action in ros2
5) developed a usable template for actions in python to reuse anywhere.
6) As a part of the process learnt about cancel_callback, feedback Callbacks, runtime abort, cancelling etc.

## Issues faced:
1) Intialization issues in turtlesim like recieving and processing data in the two topics present and general debugging issues related to the nodes.

2) General debugging issues in part 2 and i was forced to relearn and redo everything in a new template where everything was working...

3) Faced timing issues which was resolved with multi threading

## work explained:
The package `collision_avoidance` implements the part a subpart 1 of task2 and has a `launch` directory that contains the python launch files to launch the nodes

The package `circle_patrol` is an `ament_cmake` file containing the `action` directory and has the action file `ExecuteCircle.action` used in implementation of action there and also has a another package `circle_patrol_py` that has the python based implementation of task a subpart2 and has two files where `server_new` and  `client_new` are the latest versions of the files whereas `server.py` and `client.py` are older and different versions.

*PART B is done in a separate readme file marked README_PART2.md*

*Screenshots added to screenshots folder inside src*
