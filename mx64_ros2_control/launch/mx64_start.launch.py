from launch import LaunchDescription
from launch.actions import OpaqueFunction, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node
from launch.launch_description_sources import load_python_launch_file_as_module
from ament_index_python import get_package_share_directory
import os
import xacro

def launch_setup(*args, **kwargs):
    robot_description_path = os.path.join(get_package_share_directory('mx64_ros2_control'), "urdf", "mx64_ros2_control.urdf.xacro")
    robot_description = xacro.process_file(robot_description_path).toprettyxml(indent='  ')
    controller_config = os.path.join(get_package_share_directory('mx64_ros2_control'), "launch", "mx64_controllers.yaml")

    ros2_control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[
            {"robot_description": robot_description},
            controller_config],
        output="screen",
    )
    
    mx64_trajectory_controller=Node(
        package="controller_manager",
        executable="spawner",
        arguments=["mx64_trajectory_controller", "-c", "/controller_manager"],
        output="screen",
    )

    joint_state_broadcaster=Node(
            package="controller_manager",
            executable="spawner",
            arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
            output="screen",
        )

    return [ros2_control_node,
            TimerAction(period=4.0, actions=[mx64_trajectory_controller]), 
            TimerAction(period=2.0, actions=[joint_state_broadcaster]),
            ]

def generate_launch_description():
    return LaunchDescription([
        OpaqueFunction(function=launch_setup)
    ])