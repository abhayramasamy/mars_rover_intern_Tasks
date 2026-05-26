# PART 2 QUESTIONS TO ANSWR 
## PART A
1) ROS 1 Master (roscore) handles node registration and discovery. It’s a SPOF because if it crashes, new nodes cannot connect and the system loses coordination.
Existing connections may continue briefly, but no new topics/services can form. Any node restart or network drop breaks communication, making the system fragile and unreliable.

2) ROS2 comms using a DDS system each node echoes and finds eachother through peer to peer discovery, Nodes automatically discover each other via multicast, eliminating the need for a central master node liek in ros1 .
Each node independently publishes/subscribes using shared protocols.

3) ROS 1 uses TCPROS (reliable, connection-based) and UDPROS (low-latency, unreliable). Data flows via direct node-to-node sockets after Master discovery, requiring manual transport tuning.

* ROS 2 uses DDS Wire Protocol (RTPS), enabling peer-to-peer, MIDDLEMAN-less communication with automatic discovery, QoS policies (reliability, durability), multicast support, and efficient, scalable real-time data exchange.

##PART B
1) ROS 2 has a  decentralized comms using DDS (Data Distribution Service), which eliminates the need for a central server like in the case of ros1. Each node acts as a DDS participant and automatically announces its presence on the network. This discovery happens through the Simple Discovery Protocol (SDP), where nodes send periodic UDP(User datagram Protocol) messages to a predefined address. 
* All other nodes on the same network listen to this multicast address. When a node receives discovery messages from another node, it compares the advertised topics and types to determine compatibility. If a publisher and subscriber match on topic name, message type, and QoS policies, they establish a connection. 
* The Simple Discovery Protocol consists of two stages: participant discovery, where nodes detect each other’s presence, and endpoint discovery, where publishers and subscribers are matched. 

* This entire process happens dynamically, allowing nodes to join or leave the system at any time without disrupting others. 

2)Major DDS vendors integrated into ROS 2 include:

* eProsima Fast DDS (default in many ROS 2 distributions)
* Eclipse Cyclone DDS
* RTI Connext DDS
we need to change the environment variable of : `RMW_IMPLEMENTATION`
eg lets use code: `export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp`

