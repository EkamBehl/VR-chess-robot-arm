import numpy as np
import chess
import chess.svg
import chess.engine
from stockfish import Stockfish
def  printBoard(board):
    for i in range(len(board)):
        for j in board[i]:
            print(j,end=" ")
        print("\n")
RED='r'
BLUE='b'
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
    previous=[[1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,2,0,0,0],
            [0,0,0,0,0,0,0,0],
            [2,2,2,2,0,2,2,2],
            [2,2,2,2,2,2,2,2]]

    current=[[1,1,1,1,1,1,1,1],
                [1,1,1,0,1,1,1,1],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,1,0,0,0],
                [0,0,0,0,0,0,0,0],
                [2,2,2,2,0,2,2,2],
                [2,2,2,2,2,2,2,2]]
    pieceBoard=[['r','n','b','q','k','b','n','r'],
                ['p','p','p','p','p','p','p','p'],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                ['P','P','P','P','P','P','P','P'],
                ['R','N','B','Q','K','B','N','R']]
    moveBoard=nextBoard(current,previous,pieceBoard)
    """newBoard=getPiecesLoc(current,previous,pieceBoard)
    print(newBoard)"""
    myboard=chess.Board(chess.STARTING_BOARD_FEN)
    
    pieceBoard=[['r','n','b','q','k','b','n','r'],
                ['p','p','p','p','p','p','p','p'],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                ['P','P','P','P','P','P','P','P'],
                ['R','N','B','Q','K','B','N','R']]
    
    print("------------------------------------")
    printBoard(moveBoard)
    print("------------------------------------")
    print(myboard.board_fen)
    _myStr=getFen(moveBoard,'w','KQkq',"-",0,1)
    engine=chess.engine.SimpleEngine.popen_uci("stockfish")
    board=chess.Board(_myStr)
    
    stockfish=Stockfish()
    stockfish.set_fen_position(_myStr)
    print(board)
    print(stockfish.get_best_move())
    
   

    while True:
        chess.svg.board(myboard,size=350)
if __name__=='__main__':
    
    main()