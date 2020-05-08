#  Maze Solver
### This is a simple maze solver made using  **python**  for fun 
### This programs  takes image of a maze as input and shows the shoretest path available.

## Modules used
- OpenCV

To covert image to 2D pixel array

- Numpy

To create array of single data type

- time

To measure the time taken to solve the maze

### Rest of the code is done using standard python by using the concept of trees and graphs.

### Make sure that you install these modules

## Input
---
This program takes image as input and draws the path with red color from specified starting to finishing point.

## *It also saves the solved image named as "final.png"*

## To run the program open MainMenu.py
 - Give the path of the image in string (path variable)
 - Give x,y of starting point (start variable)
 - Give x,y of finishing point (finish variable)
 - Put the display variable as False for 2K and above mazes because the display tab will exceed your screen
```python

start=(2,2)
finish=(799,799)
display=False
image_path="maze/maze5.png"
run(path,start,finish,display)

```
## Note(Must Read)
---
- ### For now it only works for straight mazes ,i.e doesnt work for circular mazes and etc. I will make sure that it will work for all types of mazes in the future.

- ### This maze solver is independent of scale size, that means even though you enlarge a small maze to a massive size the solve time will remain the same.

- ### starting and ending point must be ***strictly*** inside the maze.

- ### Use paint to locate the start point and finish point.
![maze pic]( https://i.ibb.co/1MLHzpc/final.png )

## Thats all



