from projetCompile import read_file, coloration, draw

S = [5,2]
v = T(6, len(S)-1, S)
lines, col ,Mat = read_file('instances/8.txt')
A = coloration(Mat, lines, col)
draw(A)
