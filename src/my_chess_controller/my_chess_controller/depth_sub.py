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
from std_msgs.msg import MultiArrayDimension
import numpy as np
import matplotlib.pyplot as plt
TIMER=1
X=5.0
Y=5.0
def printMatrix(vertex):
     for i in range(0,81):
        
        print(vertex[i],end=" ")
        if (i+1)%9==0:
            print("\n")
    
def getTopVertices(corners):
    vertex=[]
    x=5
    y=5
    
    
    for i in range(0,7):
        if i == 0:
            vertex.append([corners[i][0][0]-(corners[i+1][0][0]-corners[i][0][0]-X),corners[i][0][1]-(corners[i+7][0][1]-corners[i][0][1])-Y])
        if i in range(0,7):
            vertex.append([corners[i][0][0],2*(corners[i][0][1])-corners[i+7][0][1]-Y])
        if i==6:
            vertex.append([corners[i][0][0]+corners[i][0][0]-corners[i-1][0][0] + X, 2*(corners[i][0][1])-corners[i+7][0][1]-Y])
            

    return vertex
def getBottomVertices(corners):
    vertex=[]
   
   
    for i in range(42 ,49):
        if i == 42:
            vertex.append([corners[i][0][0]-(corners[i+1][0][0]-corners[i][0][0])-X,corners[i][0][1]-(corners[i-7][0][1]-corners[i][0][1])+Y])
        if i in range(42,49):
            vertex.append([corners[i][0][0]-X,2*(corners[i][0][1])-corners[i-7][0][1]+Y])
        if i==48:
            vertex.append([corners[i][0][0]+corners[i][0][0]-corners[i-1][0][0] +X, 2*(corners[i][0][1])-corners[i-7][0][1]+Y])
            

    return vertex

def getRightVertices(corners):
    vertex=[]
    for i in range (0,len(corners)):
        if (i+1)% 7==0:
            vertex.append([2*(corners[i][0][0])-corners[i-1][0][0]+X,abs(2*corners[i][0][1]-corners[i-1][0][1])])
    return vertex


def getLeftVertices(corners):
    vertex=[]
    for i in range(0,len(corners)):
        if i%7==0:
            vertex.append([2*(corners[i][0][0])-corners[i+1][0][0]-X,abs(2*corners[i][0][1]-corners[i+1][0][1])])
    return vertex  

def getFullVertices(corners):
    temp=0
    _vertex=[]
    topVertices=getTopVertices(corners)
    leftVertices=getLeftVertices(corners)
    rightVertices=getRightVertices(corners)
    bottomVertices=getBottomVertices(corners)
    
    for i in topVertices:
        _vertex.append(i)
    
    for i in range(0,len(leftVertices)):
        _vertex.append(leftVertices[i])
        for j in range(temp,temp+7):
            _vertex.append(corners[j][0])
        _vertex.append(rightVertices[i])
        temp=temp+7
    for i in bottomVertices:
        _vertex.append(i)
    return _vertex

def getCorrectCorners(corners):
    _corners=[]
    for i in range (0,7):
    
        x=42+i
        while x>=0:
            _corners.append(corners[x])
            x=x-7
    return _corners
class ImageListener(Node):
    def __init__(self, color_topic,pub_topic):
        super().__init__('image_listener')
        self.allverts=[]
        self.pubVerts=[]
        self.found=False
        self.bridge = CvBridge()
        self.image_sub=self.create_subscription(msg_Image,color_topic, self.Callback,1)
        self.publisher_=self.create_publisher(Float64MultiArray,pub_topic,1)
        self.i=0
        self.timer=self.create_timer(TIMER,self.timerCallback)
    def Callback(self,data):
        try:
            self.image=self.bridge.imgmsg_to_cv2(data,data.encoding)
            
            
            
        except CvBridgeError as e:
            print(e)

        
        
        self.getCornerPoints()
    def timerCallback(self):
        
        my_arr=[]
        if self.found:
            if len(self.allverts) >0:
                
                    
                for i in range(len(self.allverts)):
                    
                    
                    my_arr.append(float(self.allverts[i][0]))
                    my_arr.append(float(self.allverts[i][1]))
                    

                
                width=2
                height=len(self.allverts)
                
                msg=Float64MultiArray()
                msg.layout.dim.append(MultiArrayDimension())
                msg.layout.dim.append(MultiArrayDimension())
                msg.layout.dim[0].label="height"
                msg.layout.dim[1].label="width"
                msg.layout.dim[0].size=height
                msg.layout.dim[1].size=width
                
                if(self.i<=5):
                    self.pubVerts=my_arr
                    msg.data=my_arr
                    self.publisher_.publish(msg)
                    print("-------------------Published message: ",self.i)
                    self.i=self.i+1
                
                """msg.layout.data_offset=0
                dim=[]
                dim.append(MultiArrayDimension("points",len(my_arr),2*len(my_arr)))
                dim.append(MultiArrayDimension("coords",2,1))
                msg.layout.dim=dim
                msg.data=my_arr"""

                
                
                
        if(self.i>5 and len(self.pubVerts) >0):
                width=2
                height=len(self.pubVerts)
                
                msgs=Float64MultiArray()
                msgs.layout.dim.append(MultiArrayDimension())
                msgs.layout.dim.append(MultiArrayDimension())
                msgs.layout.dim[0].label="height"
                msgs.layout.dim[1].label="width"
                msgs.layout.dim[0].size=height
                msgs.layout.dim[1].size=width
                msgs.data=self.pubVerts
                self.publisher_.publish(msgs)
                print("-------------------Published message: ",self.i)
                self.i=self.i+1


        
    def getCornerPoints(self):
        self.found,corners=cv2.findChessboardCorners(self.image,(7,7))
       
        imagex=self.image

        if self.found:
            cv2.drawChessboardCorners(imagex,(7,7),corners,self.found)
            
            if corners[0][0][0]-corners[1][0][0] >80:
                corners=corners[::-1]
            if corners[1][0][1] -corners[0][0][1] > 80:
                corners=getCorrectCorners(corners)
            if(corners[1][0][0]-corners[0][0][0] > 80): 
                corners=corners
            
            
            self.allverts=getFullVertices(corners)
            
            
         
                
        

def main(args=None):
    rclpy.init(args=args)

    topic = '/camera/color/image_rect_raw'
    pubTopic='BoardCorners'
    il=ImageListener(topic,pubTopic)
    rclpy.spin(il)
    
if __name__ == '__main__':
    main()

    
