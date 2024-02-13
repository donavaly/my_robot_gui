#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from turtlesim.msg import Pose
import tkinter as tk
import threading
from .draw_circle import DrawCircleNode

class MyGUI():
    def __init__(self, draw_circle_node=None):
        self.window_ = tk.Tk()
        self.lbl_ = tk.Label(self.window_, text="", font=("Arial", 48))
        self.lbl_.pack()

        self.cw = True
        self.btn_ = tk.Button(self.window_, text="Clockwise", command=self.toggle_state)
        self.btn_.pack()
    
    def run(self):
        self.window_.mainloop()
    
    def toggle_state(self):
        self.cw = not self.cw
        if self.cw:
            self.btn_.config(text="Clockwise")
        else:
            self.btn_.config(text="Counter Clockwise")

class PoseSubscriberNode(Node):
    def __init__(self, gui: MyGUI):
        super().__init__("pose_subscriber")
        self.gui = gui
        self.pose_sub_ = self.create_subscription(
            Pose, "/turtle1/pose", self.pose_callback, 10
        )
        self.get_logger().info("Draw Circle Node has been started!")
            
    def pose_callback(self, msg: Pose):
        msg_str = "x: %.2f\ny %.2f" % (msg.x, msg.y)
        #self.get_logger().info(msg_str)
        self.gui.lbl_.config(text=msg_str)
        #print(msg_str)

def start_nodes(gui):
    rclpy.init(args=None)
    node1 = PoseSubscriberNode(gui)
    node2 = DrawCircleNode(gui)
    #rclpy.spin(node)
    #rclpy.shutdown()

    # Create a MultiThreadedExecutor
    executor = MultiThreadedExecutor()
    
    # Add your nodes to the executor
    executor.add_node(node1)
    executor.add_node(node2)

    executor.spin()
    node1.destroy_node()
    node2.destroy_node()
    rclpy.shutdown()
    

def main():
    gui = MyGUI()
    t = threading.Thread(target=start_nodes, args=(gui,))
    t.start()
    gui.run()
