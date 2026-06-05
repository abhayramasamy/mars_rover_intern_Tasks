# TASK3 EXPLORING URDF, SDF, GAZEBO AND RVIZ.

This task we explore various aspects of urdf files, sdf files and how to spawn and simualte robotic movement in gazebo in general, then use the `ros_gz_bridge` to connect ROS2 AND GAZEBO and using a `teleop_node` to move the robot in gazebo.
Then we use the bridges again to publish various states like `/robot_description` and `/tf` and `/joint_states` to obtain robot data to be visualized on RVIZ2 and study the tf trees as well. Finally one must design a capable launch file to launch gazebo and other parts.

## concepts learnt

1) handling of urdf, xml, sdf files and writing them
2) spawning the robot on gazebo and simulating it.
3) using the `ros_gz_bridge` to connect ROS2 AND GAZEBO (VICE VERSA) for communication
4) connecting the Gazebo to Rviz2 again using the bridge for understanding.
5) obtain tf trees using `ros run tf2tools viewframes` to obtain tf tree pdf and study them.

## issues faced
1) overall no issues except with `ros_gz_bridge` where i was unable to connect gazebo's topic channel data to rviz2
2) resolved sim_time issues and removing unknown nodes by `pkill` command to remove interference
3) finally used an appropriate launch file to launch the code.

## How to start?
1) Download the packages `gx_xplore` and `urdf_xplore` , the latter has no executables there except a launch file.
2) `urdf_xplore` has a dir named `urdf` that has both the .sdf and .urdf files for launching (*copy file paths*).
3) open `urdf_xplore` --> `launch` directory ... and find a launch file named `spawn_robot.launch2.py` change the .urdf and .sdf file paths and replace inside the launch file.
4) Build the package `gx_xplore` for the `teleop_node` executable to control the robot.

## How to launch:
1) open a terminal and source the ROS2 AND THE gx-xplore.  run `ros2 run gx_xplore teleop_node` and use it to control the robot.
2) then navigate to `urdf_xplore/launch` directory and run `ros2 launch spawn_robot.launch2.py` it starts the `ros_gz_bridges` and `gazebo` with robot in it click play or || button to start.
3) start `rviz2` command in another terminal and add `tf` and `robot model` to the map.
4) use the teleop keys to command the robot move and visualize.

*A SIMULATION VIDEO FILE attached in a directory named sim_videos for the demo*
