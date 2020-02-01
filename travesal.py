def run(path,point1,point2,display):
    import numpy
    import cv2
    import time
    global tt
    tt=time.time()
    global tm
    tm=0
    from mage import location

    location(path)
    from mage import mn
    from mage import bnw as r_img
    from mage import bnw_img
    
    global r_img
    r_img=cv2.cvtColor(r_img,cv2.COLOR_GRAY2BGR)
    #mn=4
    global mn2
    mn2=mn//2
    global visited_nodes
    visited_nodes=[]
    global visited_pos
    visited_pos=set()
    global stack
    stack=[]
    global lol
    lol=-1
    global pos_node
    pos_node=dict()
    class node:
        def __init__(self,pos):
            self.pos=pos
            self.direc=[None for x in range(4)]
            #index 0-right
            #index 1-down
            #index 2-left
            #index 3-up
    def createNode(r,c):
        """checks if the mean pixel position is in the instance
           variable pos of objects in visited_nodes list
           if it is not in the list, then it creates a class
           object and adds the object to the list"""
        global tm
        t=time.time()
        if (r,c) in visited_pos:
            tm+=time.time()-t
            return False
        
        a=node((r,c))
        visited_pos.add((r,c)) 
        visited_nodes.append(a)
        tm+=time.time()-t
        return True
    def groupNodes(img,r,c):
        """checks the group of grey pixel and groups them in a
        list of position(row,col) and returns the list

        There is a nested function,dfs_grey(y,x) which applies dfs on
         grey pixel and adds them to list"""
        s=[(r,c)]
        def dfs_grey(y,x):
            for i in [(-1,0),(0,1),(1,0),(0,-1)]:
                """,(1,-1,),(1,1),(-1,1),(-1,-1)"""
                try:
                    if img[y+i[0]][x+i[1]]==170:
                        if not (y+i[0],x+i[1]) in s:
                            s.append((y+i[0],x+i[1]))
                            #print(s)
                            dfs_grey(y+i[0],x+i[1])
                except:
                    pass
        dfs_grey(r,c)
        return s
    def meanNode(img,r,c):
        """takes list of grey pixels.finds the mean postion(rounds
        it to pixel which is near to mean) and returns it."""
        s=groupNodes(img,r,c)
        sumr=sumc=0
        for i in s:
            sumr+=i[0]
            sumc+=i[1]
        return (round(sumr/len(s)),round(sumc/len(s)))
    def x_trv(img,r,c,x):
        """goes either +ve or - ve x-axis(i.e row is const) depending on parameter
           if grey pixel is found the it returns its position in tuple
           else if it encounters a blockage, it returns None"""
        grey_r,grey_c=r,c
        try:
            while True:
                c=c+x
                st=set()
                #print(r,c)
                for k in range(r-mn2,r+mn2+1):
                    st.add(img[k][c])
                    '''if numpy.all(r_img[k][c]==255):
                        r_img[k][c]=numpy.array([224,214,255],dtype=numpy.uint8)'''
                if st<={255,85,0} and st!={0}:
                    continue
                elif st>={170}:#centre found(grey pixel)
                    for k in range(r-mn2,r+mn2+1):
                        if img[k][c]==170:
                            if not (grey_r,grey_c) in groupNodes(img,k,c):
                                #if the grey centre found is not in intial grey centre group
                                return (k,c)
                            #returns one of the grey pixel position
                        
                elif st=={0}:#obstructed by wall
                    return None
                else:
                    print("something is wrong, no wall found & no centre found")
                    break
        except IndexError:
            print("Exit found at ",(k,c)," but going to the specified path")
    def y_trv(img,r,c,y):
        """goes either +ve or - ve y-axis(i.e col is const) depending on parameter
           if grey pixel is found the it returns its position in tuple
           else if it encounters a blockage, it returns None"""
        grey_r=r
        grey_c=c
        try:
            while True:
                r+=y
                st=set()
                #print(r,c)
                for k in range(c-mn2,c+mn2+1):
                    st.add(img[r][k])
                    '''if numpy.all(r_img[r][k]==255):
                        r_img[r][k]=numpy.array([224,214,255],dtype=numpy.uint8)'''
                if st<={255,85,0} and st!={0}:
                    continue
                elif st>={170}:#centre found(grey pixel)
                    for k in range(c-mn2,c+mn2+1):
                        if img[r][k]==170:
                            if not (grey_r,grey_c) in groupNodes(img,r,k):
                                #if the grey centre found is not in intial grey centre group
                                return (r,k)
                            #returns one of the grey pixel position
                        
                elif st=={0}:#obstructed by wall
                    return None
                else:
                    print("something is wrong,no wall found &no centre found")
                    break
        except IndexError:
            print("Exit found at ",(r,k)," but going to the specified path")
    def tr_bfs(img,r1,c1,r2,c2):
        img[r2][c2]=170
        fin=meanNode(img,r2,c2)
        srt=meanNode(img,r1,c1)
        createNode(srt[0],srt[1])
        for r in visited_nodes:
            if(r.pos==(34,34)):
                print(r.pos)
                pass
            r.direc[0]=(x_trv(img,r.pos[0],r.pos[1],1))
            r.direc[1]=(y_trv(img,r.pos[0],r.pos[1],1))
            r.direc[2]=(x_trv(img,r.pos[0],r.pos[1],-1))
            r.direc[3]=(y_trv(img,r.pos[0],r.pos[1],-1))
            for i in range(4):
                if r.direc[i]:
                    #r.direc[i]=meanNode(img,r.direc[i][0],r.direc[i][1])
                    if not createNode(r.direc[i][0],r.direc[i][1]):
                        r.direc[i]=False
                    elif r.direc[i]==fin:
                        #cv2.imwrite("bfs.png",r_img)
                        global pos_node
                        pos_node={x.pos:x for x in visited_nodes}
                        return True
    '''def  dfs(r):
        if r.pos==visited_nodes[-1].pos:#position of node is destination node
            stack.append(r.pos)
            return True
        else:
            for i in range(4):
                if r.direc[i]:#if adjacent node exist
                    if not r.direc[i] in stack:#if it is not in stack
                        stack.append(r.pos)
                        k=dfs(pos_node[r.direc[i]])
                        if k==True:
                            return True
                        else:
                            stack.pop()
        return False'''
    def  dfs(r):
        stack.append(r.pos)
        stack_set=set(r.pos)
        while True:
            if r.pos==visited_nodes[-1].pos:#position of node is destination node
                #stack.append(r.pos)
                return True
            else:
                for i in range(4):
                    if r.direc[i] and r.direc[i] not in stack_set:
                        #if adjacent node exist and it is not in stack
                        stack_set.add(r.direc[i])
                        stack.append(r.direc[i])
                        r=pos_node[r.direc[i]]
                        break
                else:
                    try:
                        stack.pop()
                        r=pos_node[stack[-1]]
                    except IndexError:
                        pass
                        return False
    def draw_y(img,r,c,y):
        grey_r=r
        grey_c=c
        while True:
            r+=y
            st=set()
            #print(r,c)
            for k in range(c-mn2,c+mn2+1):
                if numpy.all(r_img[r][k]==255):
                    r_img[r][k]=numpy.array([0,0,255],dtype=numpy.uint8)
                st.add(img[r][k])
            if(display):                
                cv2.imshow("path",r_img)
                cv2.waitKey(1)
            if st>={170}:#centre found(grey pixel)
                for k in range(c-mn2,c+mn2+1):
                    if img[r][k]==170:
                        if not (grey_r,grey_c) in groupNodes(img,r,c):
                            for i in range(r-mn2,r+1+mn2):
                                for j in range(c-mn2,c+1+mn2):
                                    try:
                                        if numpy.all(r_img[i][j]==255):
                                            r_img[i][j]=numpy.array([0,0,255],dtype=numpy.uint8)
                                    except:
                                        pass
                                    
                            if(display):
                                cv2.imshow("path",r_img)
                                cv2.waitKey(1)
                            return
                            
    def draw_x(img,r,c,x):
        grey_r,grey_c=r,c
        while True:
            c=c+x
            st=set()
            #print(r,c)
            for k in range(r-mn2,r+mn2+1):
                if numpy.all(r_img[k][c]==255):
                    r_img[k][c]=numpy.array([0,0,255],dtype=numpy.uint8)
                st.add(img[k][c])
            if(display):
                cv2.imshow("path",r_img)
                cv2.waitKey(1)
            if st>={170}:#centre found(grey pixel)
                for k in range(r-mn2,r+mn2+1):
                    if img[k][c]==170:
                        if not (grey_r,grey_c) in groupNodes(img,r,c):
                            for i in range(r-mn2,r+1+mn2):
                                for j in range(c-mn2,c+1+mn2):
                                    try:
                                        if numpy.all(r_img[i][j]==255):
                                            r_img[i][j]=numpy.array([0,0,255],dtype=numpy.uint8)
                                    except:
                                        pass
                            if(display):
                                cv2.imshow("path",r_img)
                                cv2.waitKey(1)
                            return
                            
    def draw_path(img,nd):
        while True:
            if len(stack)>1:
                i=nd.direc.index(stack[1])#cuz 0 index is starting node
                if i%2==1:
                    draw_y(img,nd.pos[0],nd.pos[1],2-i)
                else:
                    draw_x(img,nd.pos[0],nd.pos[1],1-i)
                nd=pos_node[stack.pop(1)]
            else:
                break

    print("trying to connect the nodes")
    t=time.time()
    slol=tr_bfs(bnw_img,point1[1],point1[0],point2[1],point2[0])
    if slol:
        print("Nodes connected in the form of a tree    ||  time1:{}||time2:{}".format(time.time()-t,tm))
    else:
         print("Failed to connect the nodes")
    print("Trying to find the path")
    t=time.time()
    lol=dfs(visited_nodes[0])
    if lol:
        print("Path Found!    || time:",time.time()-t)
    else:
         print("Failed to Find the path")
    #cv2.imshow("path",r_img)
    #cv2.waitKey(0)
    print("Drawing path",end="")
    t=time.time()
    draw_path(bnw_img,visited_nodes[0])
    print("    || time:",time.time()-t,"\nFinished")
    print("Toltal Time taken: ",time.time()-tt)
    cv2.imwrite("final.png",r_img)
#run("maze/4k-maze.png",(3513,1),(3441,3999),False)

                    
        
        
                
                
        
