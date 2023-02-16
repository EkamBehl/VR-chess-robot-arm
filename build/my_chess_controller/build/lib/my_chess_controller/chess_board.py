import rclpy
from rclpy.node import Node

from std_msgs.msg import Float64MultiArray

import numpy as np

import cv2
from std_msgs.msg import MultiArrayDimension
import numpy as np
TIMER=1
class ChessBoard(Node):
    def __init__(self, color_topic):
        super().__init__('image_listener')
        self.corners=[]
       
        self.image_sub=self.create_subscription(Float64MultiArray,color_topic, self.Callback,10)
        #self.publisher_=self.create_publisher(Float64MultiArray,'BoardCorners',5)
        self.i=0
        
    def Callback(self,data):
        my_data=data
        my_arr=[]
        x=0
        print(data)
        while x <=len(my_data) /2:
            temp_array=[]
            temp_array.append(data[x])
            temp_array.append(data[x+1])
            my_arr.append(temp_array)

            x=x+2


        self.corners=my_arr
        print(my_arr)
    
        

def main(args=None):
    rclpy.init(args=args)

    topic = '/BoardCorners'
    il=ChessBoard(topic)
    rclpy.spin(il)
if __name__ == '__main__':
    main()
