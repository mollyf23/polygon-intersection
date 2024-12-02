run with python 3.13
run `pip install -r requirements.txt` to install dependencies.

in VSCode:

- Open folder
- View > Command Palette > Python: Select Interpreter
- Create Virtual Environment (venv)
- Select Python 3.13
- Install requirements.txt
- virtual environment will be set up and you can use "Run and Debug" or "Run Without Debugging" on Gui.py

The graphical interface can be started by running the GUI.py file.

Sample Inputs for GUI:
Two Intersecting Right Triangles
0,0 10,0 0,10
1,1 11,1 1,11

Square Contained in a Square (containment):
-1,-1 2,-1 2,2 -1,2
0,0 1,0 1,1 0,1

Disjoint Polygons:
-1,-1 -1,-2 -3,-2 -3,-1
0,0 1,0 1,1 0,1

Square and Rotated Square (Octagonal Intersection):
0,0 1,0 1,1 0,1
-0.414213562,.5 .5,1.414 1.414,.5 .5,-0.414213562

The Sutherland-Hodgman algorithm can be run individually by first uncommenting one of the test cases at the end of the file and the block that displays the results.  Both sections start with a TODO comment.