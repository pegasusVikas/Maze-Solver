import numpy
import cv2
mn=""
bnw=""
bnw_img=""

"""White-255    black-0"""
def drawNodes(r,c):
    """detecting the fake greycorner and adding proper corner and removing the centre
        created by the two fake corners.if you want to know what this function does then
        comment the function call and see the differnce.

        note that it detects only the lower grey corner which is enough"""
    row,col=r,c #row and col are local variable
    for i in {-1,1}:
        if bnw_img[r-1][c+i]==85:
            if bnw_img[r-1][c-i]==255:
                bnw_img[row][col+i]=0#adding proper corner
                row+=-1
                bnw_img[row+(-1*(mn//2))][col+1+(-i*(mn//2))]=255#removing fake centre
                bnw_img[row+(-1*(mn//2))][col-1+(-i*(mn//2))]=255#
                print("case 1")
                #cv2.imwrite("bnw1.png",bnw_img)
            else:
                bnw_img[row-1][col]=0#adding proper corner
                col=c+i
                bnw_img[row-1+(1*(mn//2))][col+(i*(mn//2))]=255#removing fake centre
                print("case 2")
                #cv2.imwrite("bnw2.png",bnw_img)

                
    """adds centre for the corners aka adds node points"""
    for a in {(-1,1),(1,1),(1,-1),(-1,-1)}:
        if bnw_img[row+a[0]][col+a[1]]==0:
            bnw_img[row-(a[0]*(mn//2))][col-(a[1]*(mn//2))]=170
            #bracket at(mn//2) is must cuz -5//2=-3!=-2
            #and -(5//2)==-2

def location(path):
    global bnw
    global bnw_img
    global mn
    img=cv2.imread(path);
    gray_img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    (thresh,bnw_img)=cv2.threshold(gray_img,220,255,cv2.THRESH_BINARY)
    #cv2.imshow("black and white",bnw_img)
    #cv2.imwrite("blacknwhite1.png",bnw_img)
    bnw=bnw_img.copy()
    cp_bnw=bnw_img.copy()
    print("cutting boaders...   ",end="")
    for row in range(len(img)):
        if not 0 in cp_bnw[row]:
            for col in range(len(img[0])):
                bnw_img[row][col]=0
    #deleting horizontal white boaders
             
    cp_bnw=list(map(lambda n:list(map(lambda m:cp_bnw[m][n],range(len(cp_bnw)))),range(len(cp_bnw[0]))))         
    #creating vertical lists or transposing the matrix(row into col,col into row)
    for col in range(len(img[0])):
        if not 0 in cp_bnw[col]:
            for row in range(len(img)):
                bnw_img[row][col]=0            
    mn=100
    k=100
    print("|finished|")
    print("checking length...    ",end="")
    for row in range(len(img)//4,3*len(img)//4):
        for col in range(len(img[0])):
            if bnw_img[row][col]==255:
                k+=1
            else:
                if k==0:
                    continue
                if k<mn :#please change this for versetility
                    mn=k
                k=0
    print("|finished|",mn)
    print("adding nodes...    ",end="")
    if mn!=1:
        for row in range(1,len(img)-1):
            for col in range(1,len(img[0])-1):
                if bnw_img[row][col]==255:
                    if  not(bnw_img[row-1][col-1] and bnw_img[row+1][col+1]and bnw_img[row+1][col-1] and bnw_img[row-1][col+1]):
                        if ((bnw_img[row-1][col-1])and (bnw_img[row+1][col+1]))or((bnw_img[row+1][col-1]) and (bnw_img[row-1][col+1])):
                            if bnw_img[row-1][col] and bnw_img[row][col+1]and bnw_img[row+1][col] and bnw_img[row][col-1]:
                                bnw_img[row][col]=85
                                drawNodes(row,col)#resolves a proper corner and adding node
    else:
        for row in range(1,len(img)-1):
            for col in range(1,len(img[0])-1):
                if bnw_img[row][col]==255:
                    #         row-1,col
                    # row,col-1 [|] row,col+1
                    #         row+1,col
                    if (bnw_img[row-1][col] or bnw_img[row+1][col] )and(bnw_img[row][col+1] or bnw_img[row][col-1]):
                        bnw_img[row][col]=170
                        drawNodes(row,col)#resolves a proper corner and adding node
    print("|finished|")
        
    #cv2.imwrite("blacknwhite.png",bnw_img)
