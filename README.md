# VR-chess-robot-arm OverView
VR chess project which uses  opencv and ROS to detect chess pieces ,get a board state and return a move recommended by stockfish.

## Basic working:
The camera detects the color of the pieces and also detects the corners of the squares ,compares the two and gives an output of a colour occupying a particular square of the chess board .This state is compared with the previous state of the chess board and an updated piece position on the chess board is provided to the stockfish chess engine which then provides the user with a move recommendation.

## PRE-REQUISITES:
1. Download Ubuntu 22.04  and set it up on your laptop/pc (download is recommended instead of using it on virtualbox(as some issues may arise with usb connection on virtual box))
2. Install Ros2
3. follow following tutorial to make a colcon workspace: https://www.youtube.com/watch?v=3GbrKQ7G2P0
4. Download the code's zip file or clone the repository
5. install realsense sdk
6. Realsense Camera (preferably D405)
7.  Chess board and Blue/red chess pieces
### Python Libraries to install:
1. rclpy
2. chess
3. stockfish
4. Numpy
5. std_msgs
6. pynput
7. opencv-python
## Steps:
1. name the workspace as chess_ws
2. copy the files in src folder of this repository to the src folder in the chess_ws

Now the workspace is ready to be used for the project.
To start with the project,follow the following steps:

### Setting up the camera:
1. use the realsense camera and place it in such a way that it is directly over the centre of the chess board.
2. A recommended way of doing this would be to use the selfie stick with the camera and use the robot dog leash as well as the stand the firmly setup the camera and place the chessboard beneath it.

### Setting up the chessboard :
1. Make sure that the chessboard's bottom left square is black and is the A1 square  and place the blue pieces towards this side and red pieces on the other side(DO NOT PLACE THE PIECES JUST YET!!)

### Steps to run the project:
1. Open a terminal and run : 
    1. ```cd chess_ws``` to get into the chess_ws
    2. run ```colcon build``` to build the workspace to be used.
2. run ```ros2 launch realsense2_camera rs_launch.py ```  .This launches the camera node and also publishes topics including images which can be used by the other nodes
3. The camera right now would not have auto exposure turned on which would result into chessboards squares not being detected (due to lighting/over exposure ).To turn auto exposure on ,Open another terminal and use the following command: 
    ```ros2 param set /camera/camera depth_module.enable_auto_exposure true ```.
4. Run ```ros2 run my_chess_controller my_listner``` to run the chessboard square detection.This node publishes coordinates of the chessboard corners in the image obtained from the camera this would be needed to compare the location of chess pieces and then get the location of current piece.
5. Open a new terminal and run ``` ros2 run my_chess_controller blue_pieces``` to get the location of blue pieces .This node detects "Blue" color in  the image and finds the centroid of the blue region(blue contours) and publishes all coordinates of blue pieces(contours) in the image feed.
6. Open yet another terminal and run ``` ros2 run my_chess_controller red_pieces``` to get the location of red pieces .This node detects red color in the image and finds the centroid of the red regions(red contours ) and publishes all coordinates of the red pieces in the image feed.
7. Open a new terminal and run ```ros2 run my_chess_controller key_board```. This node listens and waits for "Space button" to be pressed and then publishes that event
8. Open another terminal and run ``` ros2 run my_chess_controller board_state```.This the the node which subscribes to the information from the "red pieces","blue pieces","key_board" and "my_listner" node and outputs the current board state as well as the move recommendation.

## Playing the project:
1. Once all the nodes are running ,start placing the red pieces on the a8 side (red pieces are to be considered as black pieces)
2. Place all the blue pieces(blue pieces need to be considered as white pieces) starting from rook at A1,the way it is supposed to be in chess.
3. After setting up all the pieces,make a valid move and click space bar on the window where you ran keyboard node.
4. this should provide a recommended move and also show the current state of the board on the terminal where you ran board_state node
5. To restart the match, stop the board state node (place all pieces to the starting position )and rerun it.Make a move and press space bar on the keyboard terminal
7. To change the move recommendation from black to white or white to black,go to board_state.py and go to def printBoard() and change _myStr=getFen(moveBoard,'b',......) to _myStr=getFen(moveBoard,'w',......) or vice-versa



## Changes/Possible Improvements:
1. Giving the option to change the orientation of the board.
2. Give the option to change move recommmendation for the color by giving an input straight through the terminal
3. Add the ability to castle and do en-passante


## Things to take care about /troubleshoot
1. if the board_state node fails,it is probably due to the fact that keyboard button press was not pressed after making a single move or was pressed after making multiple moves.IT NEEDS TO BE PRESSED AFTER EACH MOVE BE IT BLACK OR WHITE.
2. another possible problem for pieces not being detected can be that the board was moved and hence the location of board was changed
3. Another current problem is that board state and my_listner/depth-sub(they are the same) are configured in such a way that board state waits to get data from depth sub.py(which is data about the current chess board squares.)The problem is that my_listner sometimes fails to send the coords of the squares because of the pieces on the board.To get rid of this problem ,the my_listner keeps on sending the same coordinates once it  is able to detect the chessboard on start of the my_listner node.So if the chess board is moved during the play(which is very rare),the board state won't tell the correct board position.To rectify this,my_listner can be rerun again(without the pieces on the board!!) and then once it starts printing the coordinates,pieces can be placed back and the board_state can be run again to get the desired result again.
4. another error can arise due to the position of chess pieces,i.e. the blue pieces being placed instead of red pieces.The initial board state is hard coded in the form of  ```  
r r r r r r r r <br/>
r r r r r r r r <br/>
0 0 0 0 0 0 0 0 <br/>
0 0 0 0 0 0 0 0 <br/>
0 0 0 0 0 0 0 0 <br/>
0 0 0 0 0 0 0 0 <br/>
b b b b b b b b <br/>
b b b b b b b b <br/>

with current board state hard coded as <br />
r n b q k b n r <br/>
p p p p p p p p <br/>
0 0 0 0 0 0 0 0 <br/>
0 0 0 0 0 0 0 0 <br/>
0 0 0 0 0 0 0 0 <br/>
0 0 0 0 0 0 0 0 <br/>
R N B Q K B N R <br/>
P P P P P P P P  <br/>
where Capital letters represent white(blue pieces) pieces and small letters represent black( red pieces).
The location is obtained based on the previous color state,current color location state and on the basis of this it updates the current piece location state(the board with letters)
If the camera is placed in the opposite way,the pieces would be recognised as <br/>
b b b b b b b b <br/>
b b b b b b b b <br/>
0 0 0 0 0 0 0 0 <br/>
0 0 0 0 0 0 0 0 <br/>
0 0 0 0 0 0 0 0 <br/>
0 0 0 0 0 0 0 0 <br/>
r r r r r r r r <br/>
r r r r r r r r <br/>
so try changing the camera orientation.
It should be placed in such a way that the usb connection port of realsense D405 camera points towards right side of the board(if you have white pieces).
There might a better way of setting up the orientation of the board ,so need to invest some time into this.

# If another error occurs ,feel free to reach out to me at ekambehl@gmail.com




