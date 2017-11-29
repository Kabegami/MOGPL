from projetv2 import *

lines, col, Mat = read_file('instances/10.txt')
A = coloration(Mat, lines, col)
draw(A)
