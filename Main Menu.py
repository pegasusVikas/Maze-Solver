
from travesal import run
#NOTE------------------------------------------------------------------------
''' 2k-perfect-maze.png and 4k-perfect-maze.png are perfect mazes
    that means there is a perfect and there may not be a path for
    the chosen starting and ending point.here are the start and ending point
    for perfect mazes'''
#2k-perfect-maze start(1009,1) finish(1897,1999)
#4k-perfect-maze start(3513,1)  finish(3441,3999)

#-----------------------------------------------------------------------------


#use paint for findind the starting and ending positions
start=(2,2)#pixels
finish=(799,799)#pixels


'''set this to False for 2k and above mazes because
   display window will exceed the screen size'''
#False #True boolean must start with capital
display=True

image_path="samples/maze5.png"


run(image_path,start,finish,display)
