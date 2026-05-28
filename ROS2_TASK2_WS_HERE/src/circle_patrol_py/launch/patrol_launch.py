from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    return LaunchDescription([

        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim'
        ),

        Node(
            package='circle_patrol_py',
            executable='server',
            name='server'
        ),

        Node(
            package='circle_patrol_py',
            executable='client',
            name='client'
        ),
    ])
