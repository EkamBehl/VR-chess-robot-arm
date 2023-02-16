import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image as msg_Image
from sensor_msgs.msg import CameraInfo
from cv_bridge import CvBridge, CvBridgeError
import sys
import os
import numpy as np
import pyrealsense2 as rs2
import cv2

class ImageListener(Node):
    def __init__(self, color_topic):
        super().__init__('image_listener')
        
        self.bridge = CvBridge()
        self.image_sub=self.create_subscription(msg_Image,color_topic, self.Callback,10)

    def Callback(self,data):
        try:
            cv_image=self.bridge.imgmsg_to_cv2(data,data.encoding)
        except CvBridgeError as e:
            print(e)

        
        cv2.waitKey(3)
def main(args):
    rclpy.init(args=args)

    topic = '/camera/color/image_rect_raw'
    il=ImageListener(topic)
    rclpy.spin(il)
if __name__ == '__main__':
    main(sys.argv)

    
