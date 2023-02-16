import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image as msg_Image
from std_msgs.msg import Float64MultiArray
from cv_bridge import CvBridge, CvBridgeError
import sys
import os
import numpy as np
import pyrealsense2 as rs2
import cv2
from std_msgs.msg import MultiArrayDimension , Float64MultiArray 
from sensor_msgs.msg import Image 
import numpy as np
TIMER=3
from pynput.keyboard import Key


LOW_BLUE=np.array([100,80,0])
HIGH_BLUE=np.array([140,255,255])

class ChessPiecesLoc(Node):
    def __init__(self,image_topic):
        super().__init__('image_listener')
        self.i=0
        self.centroid1=[]
     
        self.board=[]
        self.bridge = CvBridge()
        self.blue_pub=self.create_publisher(Float64MultiArray,"BluePieces",1)
        
        self.timer=self.create_timer(TIMER,self.publishPieces)
        #self.centroid_pub=self.create_publisher(Float64MultiArray, self.on_press,10)
        self.image_sub=self.create_subscription(msg_Image,image_topic, self.CallBack,1)
        self.buttonClicked=False
    def publishPieces(self):
            
            if len(self.centroid1) > 0:
                print("-----------------blue pieces----------------")
                print(self.centroid1)
                print("------------------------------")
                height1=len(self.centroid1)
                width1=2
                data1=[]
                for i in range(len(self.centroid1)):
                    data1.append(float(self.centroid1[i][0]))
                    data1.append(float(self.centroid1[i][1]))
                msg1=Float64MultiArray()
                
                
                msg1.layout.dim.append(MultiArrayDimension())
                msg1.layout.dim.append(MultiArrayDimension())
                msg1.layout.dim[0].label="height"
                msg1.layout.dim[1].label="width"
                msg1.layout.dim[0].size=height1
                msg1.layout.dim[1].size=width1
                msg1.data=data1
                self.blue_pub.publish(msg1)
    def getBlueCentroids(self):
        lowColor1=LOW_BLUE
        highColor1=HIGH_BLUE
        image1=self.image.copy()

        hsv=cv2.cvtColor(image1,cv2.COLOR_BGR2HSV)
        mask1=cv2.inRange(hsv,lowColor1,highColor1)

        res1=cv2.bitwise_and(image1,image1,mask=mask1)
        gray1=cv2.cvtColor(res1,cv2.COLOR_BGR2GRAY)

        blur1=cv2.blur(gray1,(10,10))
        ret1,thresh1=cv2.threshold(blur1,100,255,cv2.THRESH_OTSU)
        contours1,heirarchy1=cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(res1, contours1, -1, (255,0,0), 1)
        centroidsBlue=[]

        for cs in contours1:
            MS=cv2.moments(cs)
            if MS['m00'] != 0:
                cX=int(MS["m10"]/MS["m00"])
                cY=int(MS["m01"]/MS["m00"])

                centroidsBlue.append([cX,cY])
                

        self.centroid1=centroidsBlue
    def CallBack(self,data):

        try:
            self.image=self.bridge.imgmsg_to_cv2(data,data.encoding)

            self.image2=self.bridge.imgmsg_to_cv2(data,data.encoding)
            
        except CvBridgeError as e:
            print(e)
        
      
        self.getBlueCentroids()




           
def main(args=None):
    rclpy.init(args=args)
   
    imgTopic = '/camera/color/image_rect_raw'
    
    chessp=ChessPiecesLoc(imgTopic)
    rclpy.spin(chessp)
if __name__ == '__main__':
    main()