
import rclpy
from rclpy.node import Node

from std_msgs.msg import Float64MultiArray ,String

import numpy as np
from pynput import keyboard
from pynput.keyboard import Listener,Key
import cv2
from std_msgs.msg import MultiArrayDimension
import numpy as np

TIMER=1

from sshkeyboard import listen_keyboard ,stop_listening



class keyBoard(Node):
    def __init__(self):
        super().__init__('key_listener')
        self.pub=self.create_publisher(String,'/keys',1)
        self.key="0"
    def press(self,key):
        print(f"'{key}' pressed")
        if(key=="space"):
            msg=String()
            msg.data=key

            self.pub.publish(msg)
        else:
            msg=String()
            msg.data="0"
            self.pub.publish(msg)

        
    def release(self,key):
        print(f"'{key}' released")

    def listenKey(self):
        listen_keyboard(
            on_press=self.press,
            on_release=self.release,
        )
def main(args=None):
    rclpy.init(args=args)

    
    il=keyBoard()
    il.listenKey()

    rclpy.spin(il)
    
    
if __name__ == '__main__':
    main()