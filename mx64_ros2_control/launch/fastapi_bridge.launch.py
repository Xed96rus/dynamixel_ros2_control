from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
from ament_index_python import get_package_share_directory
import os

def generate_launch_description():
    package_path = get_package_share_directory('mx64_ros2_control')
    fastapi_script = os.path.join(package_path, 'fastapi', 'fastapi_node.py')


    return LaunchDescription([
        ExecuteProcess(
            cmd=[
                'python3',
                fastapi_script
            ],
            shell=True,
            output='screen'
        )
    ])