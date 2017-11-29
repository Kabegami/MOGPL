from projetv2 import *

lines, col, Mat = read_file('instances/8.txt')
A = coloration(Mat, lines, col)
draw(A)
