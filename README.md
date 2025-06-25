# dynamixel_ros2_control

## Set up

1. [Install ROS 2 Humble on Ubuntu 22.04](http://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html)
2. Then, create a workspace and clone the [dynamixel_hardware](https://github.com/dynamixel-community/dynamixel_hardware.git) (branch `humble`)package there, following all the instructions in the package

```shell
source /opt/ros/humble/setup.bash
mkdir -p ~/ros/humble && cd ~/ros/humble
git clone https://github.com/youtalk/dynamixel_control.git src
vcs import src < src/dynamixel_control.repos
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install --cmake-args -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
. install/setup.bash
```
3. Use this command to copy this package in your workspace:

```shell
source /opt/ros/humble/setup.bash
git clone https://github.com/Xed96rus/dynamixel_ros2_control.git
cd ~/ros/humble
colcon build --symlink-install
```

## Launch

To start controlling one motor by posting messages to the /Joint topic

```shell
ros2 launch mx64_ros2_control mx64_start.launch.py
```


Example of a message that accepts the name of the motor and its goal position

```shell
ros2 topic pub -1 /mx64_trajectory_controller/joint_trajectory trajectory_msgs/JointTrajectory "{ \
 joint_names: ['joint1'], \
 points: [ { positions: [1.5], velocities: [0.0] } ] \
```