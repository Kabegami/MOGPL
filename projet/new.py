import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import time

def test_block():
    assert(tryBlock(4,3,[1,-1,-1,-1,1]) == True)
    assert(tryBlock(3,3,[0,-1,-1,-1,0]) == True)  
    assert(tryBlock(4,3,[-1,-1,-1,-1,-1]) == True)
    assert(tryBlock(3,3,[0,-1,-1,-1,0]) == True)
    assert(tryBlock(2,3,[-1,-1,-1,0,0]) == True)
    assert(tryBlock(2,3,[-1,-1,1,0,0]) == True)

def memo(function):
    dico = dict()
    def helper(j,l,S, line):
        """ j : index case,  l : index block , S : sequence Block , line : vecteur ligne , i : indice ligne (i sert uniquement a la memoization """
        idS = id(S)
        key = (j,l, idS) + tuple(line)
        if key not in dico:
            dico[key] = function(j,l,S,line)
        return dico[key]
    return helper

def timer(f , *args):
    t1 = time.time()
    res = f(*args)
    t2 = time.time()
    diff = t2 - t1
    return res, diff

def read_file(fname):
    f = open(fname,'r')
    b = False
    l = []
    col = []
    for line in f:
        split = line.split()
        if len(split) != 0 and split[0] == "#":
            b = True
        else:
            split = line.split()
            #element vide:
            if len(split) == 0:
                split = [0]
            else:
                split = [int(i) for i in split]
            if not(b):
                l.append(split)
            else:
                col.append(split)
    f.close()
    d1 = len(l)
    d2 = len(col)
    Mat = np.zeros((d1,d2)) - np.ones((d1,d2))
    return l, col, Mat

def draw(Matrice):
    plt.imshow(Matrice, cmap='binary', interpolation='nearest')
    plt.colorbar()
    plt.show()

def colorIn(line, color):
    for i in line:
        if i == color:
            return True
    return False

def sameColor(line, color):
    for i in line:
        if i != color:
            return False
    return True

def tryBlock(j, sl, line):
    #on verifie que la case d'avant n'est pas noir + bornes
    if j + 1 < len(line) and line[j+1] == 1:
        return False
    for i in range(sl):
        case = j - i
        print('case : ', case)
        if case < 0:
            return False
        if line[case] == 0:
            return False
    if line[case - 1] == 1:
        return False
    return True

def T3(line, S):
    if line == [] and S != []:
        return False
    if line == [] and S == []:
        return True
    if S == []:
        return line == [0 for i in line]
    K = len(line)
    if K < S[:-1]:
        return False
    if K == S[:-1]:
        return K == 0 and line == [0 for i in line]
    if K > S[:-1]:
        last = line[:-1]
        if last == 1:
            pass
        

def T2(j, l, S, line):
    print(' l : ', l)
    print('j : ', j)
    sl = S[l]
    if l <= 0:
        return not(colorIn(line,1))
    if j < sl - 1:
        return False
    if j == (sl - 1):
        return l == 0 and not(colorIn(line,0))
    if j > sl - 1:
        if line[j] == 1:
            if (tryBlock(j, sl, line)) == False:
                   return False
            return T2(j-sl-1, l-1, S, line[:j-sl])
        #white
        if line[j] == 0:
            return T(j-1,l,S,line[:-1])
        #-1
        if (tryBlock(j, sl, line)):
            return T(j-sl-1, l-1, S, line[:j-sl])
        return T2(j-1, l, S, line[:-1]) 

@memo
def T(j, l, S, line):
    if j == 0 and l != -1:
        return False
    if j == 0 and l == -1:
        return True
    sl = S[l]
    if l == -1:
        return not(colorIn(line, 1))
    if j < sl - 1:
        return False
    if (j == sl - 1):
        return (l == 0 and not(colorIn(line,0)))
    if (j > sl - 1):
        #noir
        if line[j] == 1:
            if not(tryBlock(j,sl,line)):
                return False
            return T(j-sl-1, l -1, S,line[:j-sl])
        #blanc
        if line[j] == 0:
            return T(j-1,l,S,line[:-1])
        #-1
        if not(tryBlock(j, sl, line)):
            return T(j-1, l, S, line[:-1])
        return T(j-1, l, S, line[:-1])

def color_case(i, S, vecteur):
    if vecteur[i] != -1:
        #cas ou la case est deja coloré
        return None
    #black
    vecteur[i] = 1
    N = len(vecteur)
    black = T(N-1,len(S)-1,S,vecteur)
    #white
    vecteur[i] = 0
    white = T(N-1,len(S)-1,S,vecteur)
    if not(black) and not(white):
        #la grille n'a pas de solution
        return False
    if black and white:
        vecteur[i] = -1
        return None
    if black:
        #on colorie le vecteur en noir
        print('coloration black : ',i)
        vecteur[i] = 1
        return i
    if white:
        vecteur[i] = 0
        return i
    print('Erreur !')
    print('black : ', black)
    print('white : ', white)

def coloration(A, lines, col):
    N, M = A.shape
    L = set([i for i in range(N)])
    C = set([i for i in range(M)])
    cpt = 0
    while L != set() or C != set():
        for i in L:
            li = lines[i]
            linecolor = A[i]
            for j in range(M):
                new = color_case(j, li, linecolor)
                if new is False:
                    print('j : {}, li : {}, linecolor : {}'.format(j,li, linecolor))
                    print('last A : ', A)
                    return False
                if new is not None:
                    C.add(new)
        L = set()
        for j in C:
            cj = col[j]
            colcolor = A[:,j]
            for i in range(N):
                new = color_case(i, cj, colcolor)
                if new is False:
                    print('j : {}, li : {}, linecolor : {}'.format(i,cj, colcolor))
                    return False
                if new is not None:
                    L.add(new)
        C = set()
        print('cpt : ', cpt)
        cpt += 1
    return A

if __name__ == "__main__":
    test_block()
    lines, col, Mat = read_file('instances/1.txt')
    A, t = timer(coloration,Mat, lines, col)
    print('A : ', A)
    print("temps d'execution de la fonction : {} secondes".format(t))
#    draw(A)
