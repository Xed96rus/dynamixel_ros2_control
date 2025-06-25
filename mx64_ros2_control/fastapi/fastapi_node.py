import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from models.models import *
from pydantic import BaseModel
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
import uvicorn
import threading

# ROS2 узел
class FastAPIRos2Bridge(Node):
    def __init__(self):
        super().__init__('fastapi_node')
        self.publisher_ = self.create_publisher(JointTrajectory, '/mx64_trajectory_controller/joint_trajectory', 10)
        self.subscription_ = self.create_subscription(JointTrajectory, '/mx64_trajectory_controller/joint_trajectory', self.listener_callback, 10)
        self.last_message = None

    def publish_message(self, joint_names, positions):
        msg = JointTrajectory()
        msg.joint_names = joint_names

        point = JointTrajectoryPoint()
        point.positions = positions

        msg.points.append(point)
        self.publisher_.publish(msg)
        self.get_logger().info(f'Published JointTrajectory: {msg}')
        self.last_message = msg

    def listener_callback(self, msg: JointTrajectory):
        self.get_logger().info(f'Received JointTrajectory: {msg}')
        self.last_message = msg
# FastAPI-приложение

ros2_node: FastAPIRos2Bridge = None

def ros2_spin():
    rclpy.spin(ros2_node)
    pass

@asynccontextmanager
async def lifespan(app: FastAPI):
    global ros2_node
    rclpy.init()
    ros2_node = FastAPIRos2Bridge()
    thread = threading.Thread(target=rclpy.spin, args=(ros2_node,), daemon=True)
    thread.start()
    yield
    ros2_node.destroy_node()
    rclpy.shutdown()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "FastAPI ROS2 JointTrajectory bridge is running"}

@app.post("/send", response_model=ResponseModel)
async def send_command(data: RequestModel):

    try:
        ros2_node.publish_message(data.joint_names, data.positions)
        return {"status": "command sent"}
    except KeyError as e:
        return {"status": "error", "reason": f"Missing field: {str(e)}"}

@app.get("/read")
async def read_last():
    if ros2_node.last_message is None:
        return {"last_message": "No messages received yet"}

    return {
        "joint_names": ros2_node.last_message.joint_names,
        "positions": [pt.positions for pt in ros2_node.last_message.points],
    }

# Запуск uvicorn при старте
if __name__ == '__main__':
    uvicorn.run("fastapi_node:app", host="0.0.0.0", port=8000, reload=False)
