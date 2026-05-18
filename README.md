# mars_rover_intern_Tasks
Various tasks given during my intern at Mars Rover club IIITDM
----------------------------------------------
This project implements publisher-subscriber based ROS2 nodes written in python and cpp, also an attempted implementation of services between python node, subscriber nodes... verifying output using CLI tools including RQT.
## Concepts learnt:
1) Nodes, Topics, Services(basic) in ros2 humble
2) Node implementation using python, cpp
3) Topic implementation using python, cpp
4) basic service implementation using python
5) Handling CLI and RQT to monitor ROS2 nodes

## Issues faced:
1) Cpp syntax, new concepts like sharedptrs, templates, namespaces seemed new had to learn how to handle oops in cpp.
2) service was slighlty hard to implement, its packages and service still faces synchronization issues.

## work explained:
The package `ros2_task1` contains python with two nodes `node1.py` `node2.py` with one of them being a publisher and otherbeing a subscriber to the topic `Topic`. Attempted implementation of a basic service `SetSpeed` where the share speeds and respond.

The package `cpp_pkg` contains two cpp nodes `node3cpp` `cpp_publisher` with node3cpp subscribes to the same node `Topic` and cpp_publisher publishes to the same topic but slighlty different data. There are no service implementations in here

The package `my_interface` is an `ament_cmake` package containing `SetSpeed.srv` a service file to implement services.
