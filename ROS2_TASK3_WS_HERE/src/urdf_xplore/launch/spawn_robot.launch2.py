import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch.substitutions import Command
from launch_ros.actions import Node

def generate_launch_description():
    world_path = '/home/abhay-07/gz_worlds/world_no_2.sdf' #change the file path here (moved)
    urdf_file = '/home/abhay-07/my_robo_2.urdf'

    return LaunchDescription([
        # Gazebo
        ExecuteProcess(
            cmd=['ign', 'gazebo', world_path],
            output='screen'
        ),

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            parameters=[{
                'robot_description': Command(['xacro ', urdf_file]),
                'use_sim_time': True 
            }]
        ),
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            arguments=['/model/my_robo/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist'],
            output='screen'
        ),

        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            name='joint_state_bridge',
            arguments=['/world/empty/model/my_robo/joint_state@sensor_msgs/msg/JointState[gz.msgs.Model'],
            remappings=[
                ('/world/empty/model/my_robo/joint_state', '/joint_states')
            ],
            parameters=[{'use_sim_time': True}],
            output='screen'
        ),

        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            name='tf_bridge',
            arguments=['/model/my_robo/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V'],
            remappings=[
                ('/model/my_robo/tf', '/tf')
            ],
            parameters=[{'use_sim_time': True}],
            output='screen'
        ),

    ])
