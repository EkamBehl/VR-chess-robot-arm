import rclpy
from rclpy.node import Node

from std_msgs.msg import Float64MultiArray ,String

import numpy as np

from pynput import keyboard
from pynput.keyboard import Listener,Key
import cv2
from std_msgs.msg import MultiArrayDimension
import numpy as np


import numpy as np
import chess
import chess.svg
import chess.engine
from stockfish import Stockfish



RED='r'
BLUE='b'
TIMER=1

class ChessBoard(Node):
    def __init__(self, chess_board_topic,red_pieces_topic,blue_pieces_topic,name=None):
        super().__init__('board_listener')
        self.node = rclpy.create_node(name or type(self).__name__)
        self.isPressed=False
        self.corners=[]
        self.redPieces=[]
        self.bluePieces=[]
        self.image_sub=self.create_subscription(Float64MultiArray,chess_board_topic, self.Callback,1)
        self.red_sub=self.create_subscription(Float64MultiArray,red_pieces_topic,self.getRedPieces,1)
        self.blue_sub=self.create_subscription(Float64MultiArray,blue_pieces_topic,self.getBluePieces,1)
        #self.publisher_=self.create_publisher(Float64MultiArray,'BoardCorners',5)

        self.previousPosition=[['r','r','r','r','r','r','r','r'],
            ['r','r','r','r','r','r','r','r'],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            ['b','b','b','b','b','b','b','b'],
            ['b','b','b','b','b','b','b','b']]
        self.piecePositions=[['r','n','b','q','k','b','n','r'],
                ['p','p','p','p','p','p','p','p'],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                ['P','P','P','P','P','P','P','P'],
                ['R','N','B','Q','K','B','N','R']]
        self.currentPosition=[]
        self.bestMove=""
        self.key_sub=self.create_subscription(String,"/keys",self.printBoard,1)
        self.i=0
    
        self.timer=self.create_timer(1,self.printMyBoard)
    def getRedPieces(self,msg):
        my_arr=Float64MultiArray()
        my_arr=msg
        data=my_arr.data
        piecesArray=self.getArray(data)
        self.redPieces=piecesArray
   
    def printMyBoard(self):
        
        boards=[0]*64
        if(len(self.corners)) >50:
            
           
            resultBoard=getBoard(self.redPieces,self.bluePieces,self.corners,boards)
            

    def get2DBoard(self,board):
        g2DBoard=[]
        i=0
        
        while i <64:
            temp=[]
            j=0
            while j < 8:
                temp.append(board[i])
                i=i+1
                j=j+1
            g2DBoard.append(temp)
        return g2DBoard

            

    def printBoard(self,msg):
        if(msg.data=="space"):
            
            boards=[0]*64
            if(len(self.corners)) >50:
                
                
                    resultBoard=getBoard(self.redPieces,self.bluePieces,self.corners,boards)
                    self.currentPosition=self.get2DBoard(resultBoard)
                    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                    print(resultBoard)
                    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                    print("#############################################################")
                    print(self.currentPosition)
                    print("#############################################################")
                    moveBoard=nextBoard(self.currentPosition,self.previousPosition,self.piecePositions)
                    _myStr=getFen(moveBoard,'b','KQkq',"-",0,1)
                    engine=chess.engine.SimpleEngine.popen_uci("stockfish")
                    board=chess.Board(_myStr)
                    
                    stockfish=Stockfish()
                    stockfish.set_fen_position(_myStr)
                
                    self.bestMove=stockfish.get_best_move()
                    """print("---------------------------------------")
                    for i in range(0,64):
                        print(resultBoard[i],end=" ")
                        if(i+1)%8==0:
                            print("\n")
                    print("---------------------------------------")"""
                    print("---------------------------------------move------------------------------")
                    print(self.bestMove)
                    print("-----------------------------------------------------------------------")
                    print(stockfish.get_board_visual())
            self.previousPosition=self.currentPosition
            self.piecePositions=moveBoard
            
           

           
            

    
    def getBluePieces(self,msg):
        my_arr=Float64MultiArray()
        my_arr=msg
        data=my_arr.data
        piecesArray=self.getArray(data)
        self.bluePieces=piecesArray

        

    def getArray(x,my_data):
        my_data=np.array(my_data)
        i=0
        newArr=[]
        while i < len(my_data)-1 :
            temp_array=[]
            temp_array.append(my_data[i])
            temp_array.append(my_data[i+1])

            i=i+2
            newArr.append(temp_array)

        if len(newArr) >0:
            return newArr
        else:
            print("----------data not found error at getArray--------------")
            return 0

                
    
        

    def Callback(self, msg):
        
        my_arr=Float64MultiArray()
        my_arr=msg
        
     
        
        dataArr=np.array(my_arr.data)
        cornerArray=self.getArray(dataArr)
        
        if(my_arr !=0):

            self.corners=cornerArray
            
        else:
            print("Not found")

    
                
        
def getBoard(centroids2,centroids1,corners,board):
        
        for i in range (0,len(centroids1)):
            
            x=0
            found=False
            square=0
            temp=0
            while x <= 70 and found==False:
                if(temp==8):
                    temp=0
                if centroids1[i][0] > corners[x][0] and centroids1[i][0] < corners[x+10][0] and centroids1[i][1] > corners[x][1] and centroids1[i][1] < corners[x+10][1]:
                    board[square]="r"
                    
                    found=True
                
                square=square+1
                if(temp+1)%8==0:
                    x=x+2
                else:
                    x=x+1
                temp=temp+1
        for i in range (0,len(centroids2)):
            
            x=0
            found=False
            square=0
            temp=0
            while x <= 70 and found==False:
                if(temp==8):
                    temp=0
                if centroids2[i][0] > corners[x][0] and centroids2[i][0] < corners[x+10][0] and centroids2[i][1] > corners[x][1] and centroids2[i][1] < corners[x+10][1]:
                    board[square]="b"
                    
                    found=True
                
                square=square+1
                if(temp+1)%8==0:
                    x=x+2
                else:
                    x=x+1
                temp=temp+1
        
        return board       

def nextBoard(current,previous,pieceBoard):
    newBoard=[]
    for i in range (len(pieceBoard)):
        temp=[]
        for j in range (len(pieceBoard)):
            temp.append(0)
        newBoard.append(temp)
    vars=[]
    for i in range(len(newBoard)):
        for j in range(len(newBoard)):
            if(current[i][j]==previous[i][j]):
                newBoard[i][j]=pieceBoard[i][j]
            else:
                vars.append([pieceBoard[i][j],i,j])
    print(vars)
    if(len(vars)>0):
        if(vars[0][0]==0 or vars[1][0]==0):
            if(vars[0][0])==0:
                newBoard[vars[0][1]][vars[0][2]]=pieceBoard[vars[1][1]][vars[1][2]]
            elif(vars[1][0])==0:
                newBoard[vars[1][1]][vars[1][2]]=pieceBoard[vars[0][1]][vars[0][2]]
        if(vars[0][0]!=0 and vars[1][0]!=0):

            if(current[vars[0][1]][vars[0][2]]==RED and current[vars[1][1]][vars[1][2]]==0):
                
                if(str(vars[0][0]).islower()):
                    newBoard[vars[0][1]][vars[0][2]]=vars[0][0]
                elif(str(vars[1][0]).islower()):
                    newBoard[vars[0][1]][vars[0][2]]=vars[1][0]
            elif(current[vars[0][1]][vars[0][2]]==0 and current[vars[1][1]][vars[1][2]]==RED):
                if(str(vars[0][0]).islower()):
                    newBoard[vars[1][1]][vars[1][2]]=vars[0][0]
                elif(str(vars[1][0]).islower()):
                    newBoard[vars[1][1]][vars[1][2]]=vars[1][0]

            if(current[vars[0][1]][vars[0][2]]==BLUE and current[vars[1][1]][vars[1][2]]==0):
                
                if(str(vars[0][0]).isupper()):
                    newBoard[vars[0][1]][vars[0][2]]=vars[0][0]
                elif(str(vars[1][0]).isupper()):
                    newBoard[vars[0][1]][vars[0][2]]=vars[1][0]
            elif(current[vars[0][1]][vars[0][2]]==0 and current[vars[1][1]][vars[1][2]]==BLUE):
                if(str(vars[0][0]).isupper()):
                    newBoard[vars[1][1]][vars[1][2]]=vars[0][0]
                elif(str(vars[1][0]).isupper()):
                    newBoard[vars[1][1]][vars[1][2]]=vars[1][0]
    return newBoard
    
def getFen(board,active,castle,enPassant,half,full):
    s=""
    for i in range(len(board)):
        counter=0
        for j in range(len(board[i])):
            if board[i][j]==0:
                counter=counter+1
                if j==len(board)-1:
                    s=s+str(counter)
            else:
                if counter !=0:
                    s=s+str(counter)
                s=s+board[i][j]
                counter=0
        if(i!=len(board)-1): s=s+"/"
    s=s+' '+str(active)+' '
    s=s+' '+castle+' '
    s=s+' '+enPassant+' '
    s=s+' '+str(half)+ ' '
    s=s+' '+str(full)+ ' '
    return s


def main(args=None):
    rclpy.init(args=args)
   
    
    topic = '/BoardCorners'
    redTopic='/RedPieces'
    blueTopic='/BluePieces'
    il=ChessBoard(topic,redTopic,blueTopic)
    BOARD=il

    
   
    rclpy.spin(il)
if __name__ == '__main__':
    main()
