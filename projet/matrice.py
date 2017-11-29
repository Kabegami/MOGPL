class Matrice(object):
    def __init__(self, lines, cols):
        """ 2 listes de pointeur """
        self.lines = lines
        self.cols = cols
        self.nblines = len(lines)
        self.nbcols = len(cols)

    def assign(self,i,j, valeur):
        self.lines[j][i] = valeur
        self.cols[i][j] = valeur

    def str_Line(self):
        s = '['
        for line in self.lines:
            s += '['
            for elem in line:
                s += str(elem) + ','
            s = s[:-1]
            s += ']' + '\n'
        s = s[:-1]
        s += ']'
        return s

    def printLine(self):
        print(self.str_Line())

if __name__ == '__main__':
    lines = [[0,1],[2,3]]
    cols = [[0,2],[1,3]]
    M = Matrice(lines, cols)
    M.printLine()
    M.assign(0,1, 5)
    M.printLine()
