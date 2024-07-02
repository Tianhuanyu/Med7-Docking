import os

import xacro
from ament_index_python import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    robot_description = {
        "robot_description": xacro.process(
            os.path.join(
                get_package_share_directory("med7_dock_description"),
                "urdf/med7dock.urdf.xacro",
            ),
            mappings={"robot_name": "lbr"},
        )
    }

    joint_state_publisher_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
    )

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="both",
        parameters=[robot_description],
    )

    rviz = Node(
        package="rviz2",
        executable="rviz2",
        arguments=[
            "-d",
            os.path.join(
                get_package_share_directory("med7_dock_description"),
                "config/config.rviz",
            ),
        ],
    )

    return LaunchDescription(
        [joint_state_publisher_node, robot_state_publisher_node, rviz]
    )
