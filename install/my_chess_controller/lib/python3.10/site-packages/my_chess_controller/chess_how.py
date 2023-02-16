import numpy as np
def getPiecesLoc(current,previous,pieceBoard):
    new_board=[0,0,0,0,0,0,0,0]*8
    for i in range(8):
        
        for j in range(8):
            if previous[i][j]==current[i][j]:
                new_board[i][j]=pieceBoard[i][j]
            else:
                print("i: ",i)
                print('j: ',j)
                print("piece board",pieceBoard[i][j])


    return new_board

def main(args=None):
    previous=[[1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [2,2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2,2]]

    current=[[1,1,1,1,1,1,1,1],
                [1,1,1,0,1,1,1,1],
                [0,0,0,0,0,0,0,0],
                [0,0,0,1,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [2,2,2,2,2,2,2,2],
                [2,2,2,2,2,2,2,2]]
    pieceBoard=[['r','n','b','q','k','b','n','r'],
                ['p','p','p','p','p','p','p','p'],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                ['P','P','P','P','P','P','P','P'],
                ['R','N','B','Q','K','B','N','R']]

    newBoard=getPiecesLoc(current,previous,pieceBoard)
    print(newBoard)
if __name__=='__main__':
    main()