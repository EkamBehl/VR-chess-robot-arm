def printMatrix(vertex):
     for i in range(0,81):
        
        print(vertex[i],end=" ")
        if (i+1)%9==0:
            print("\n")
    
def getTopVertices(corners):
    vertex=[]
   
            
    for i in range(0,7):
        if i == 0:
            vertex.append([corners[i][0][0]-(corners[i+1][0][0]-corners[i][0][0]),corners[i][0][1]-(corners[i+7][0][1]-corners[i][0][1])])
        if i in range(0,7):
            vertex.append([corners[i][0][0],2*(corners[i][0][1])-corners[i+7][0][1]])
        if i==6:
            vertex.append([corners[i][0][0]+corners[i][0][0]-corners[i-1][0][0] , 2*(corners[i][0][1])-corners[i+7][0][1]])
            

    return vertex
def getBottomVertices(corners):
    vertex=[]
   
            
    for i in range(42 ,49):
        if i == 42:
            vertex.append([corners[i][0][0]-(corners[i+1][0][0]-corners[i][0][0]),corners[i][0][1]-(corners[i-7][0][1]-corners[i][0][1])])
        if i in range(42,49):
            vertex.append([corners[i][0][0],2*(corners[i][0][1])-corners[i-7][0][1]])
        if i==48:
            vertex.append([corners[i][0][0]+corners[i][0][0]-corners[i-1][0][0] , 2*(corners[i][0][1])-corners[i-7][0][1]])
            

    return vertex

def getRightVertices(corners):
    vertex=[]
    for i in range (0,len(corners)):
        if (i+1)% 7==0:
            vertex.append([2*(corners[i][0][0])-corners[i-1][0][0],abs(2*corners[i][0][1]-corners[i-1][0][1])])
    return vertex


def getLeftVertices(corners):
    vertex=[]
    for i in range(0,len(corners)):
        if i%7==0:
            vertex.append([2*(corners[i][0][0])-corners[i+1][0][0],abs(2*corners[i][0][1]-corners[i+1][0][1])])
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