# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
#import test
from wrapper import *

#variable global
cpt = 0
debug = True

def silent(function):
    """ fonction wraper qui empeche les functions avec @silent de print si la variable global debug est à False, si debug est à True les fonctions s'affichent normalement """
    def stop_print(*args):
        """ prevent a function to print """
        global debug
        if debug == True:
            if not args:
                res = function()
            else:
                res = function(*args)
            return res
        else:
            sys.stdout = open(os.devnull, "w")
            if not args:
                res = function()
            else:
                res = function(*args)
            sys.stdout = sys.__stdout__
            return res
    return stop_print

@silent
def check_color_in(j, line, color):
    """ j : int plus grandes cases, lines : array, color : int {blanc : 0, noir = 1, indeter = -1}"""
    for i in range(0, j+1):
        if line[i] == color:
            return True
    return False

def T(j, l, S):
    #print('j : {}, l : {}, S : {}'.format(j,l,S))
    if l == -1:
        return True
    sl = S[l]
    if (j == sl - 1):
        #si on considere le dernier element de la serie.
        if l == 0:
            return True
        return False
    if ( j > (sl - 1)):
        return (T(j-sl-1, l-1,S) or T(j-1, l, S))

@silent
def possible_block(j, l, line):
    for i in range(0,l):
        print('case : {}'.format(j -i))
        if line[j-i] == 0:
            return False
        if j - i < 0:
            return False
    #dernier car
    print('derniere case apres le bloc : ', j - i - 1)
    if line[j - i - 1] == 1:
        return False
    return True

@silent
def T2(j, l, S, line):
    if j < 0 and l >= 0:
        return False
    if j < 0 and l < 0:
        return True   
    if l == -1:
        if line[j] == 1:
            print('bloc noir en {} alors que plus de séquence'.format(j))
            print('line :', line)
            return False
        if j == 0:
            return True
        return T2(j-1,l,S,line)
    sl = S[l]
    if sl == 0:
        return T2(j,l-1,S,line)
    #il faut verifier que chaque case n'est pas noir
    if (j == sl - 1):
        print('cas j = sl - 1')
        print('j : ', j)
        print('l : ', l)
        if l == 0 and not(check_color_in(j, line, 0)):
            print('cas j = sl-1 true')
            return True
        print('cas j = sl-1 false')
        return False
    if (j>(sl - 1)):
        #cas noir
        print('color : ', line[j])
        if line[j] == 1:
            if not(possible_block(j, sl, line)):
                return False
            return T2(j-sl-1, l-1,S, line)
        #cas blanc
        if line[j] == 0:
            return T2(j-1, l, S,line)
        #cas non determiner
        print('non determiner')
        #Quand on a pas de bloc forcement vrai.... du coup on peut toujours placer un bloc sur une case indeterminer
        if not(possible_block(j, sl, line)):
            return T2(j-1, l, S,line)
           
        b1 = T2(j-sl-1, l-1,S, line)
        #Pourquoi ce b1 s'active en mode silent ???
        print('b1 : ', b1)
        b2 = T2(j-1, l, S,line)
        return b1 or b2
#        print('b2 : ', b2)
#        return b1 or b2

def color_case(i, S, vecteur):
    v = np.copy(vecteur)
    #black
    v[i] = 1
    print('S : ', S)
    black = T2(len(v)-1,len(S)-1,S,v)
    #white
    v[i] = 0
    white = T2(len(v)-1,len(S)-1,S,v)
    if not(black and white):
        #la grille n'a pas de solution
        print("La grille n'est pas faisable")
        print("arguments de T2 : j = {}, l = {}, S = {}, v = {}".format(len(v)-1, len(S) -1, S, v))
        return False
    if black and white:
        return None
    if black:
        #on colorie le vecteur en noir
        vecteur[i] = 1
        return i
    vecteur[i] = 0
    return i
    
    

def coloration(A, lines, col):
    N, M = A.shape
    L = [i for i in range(N)]
    C = [i for i in range(M)]
    while L != [] or C != []:
        for i in range(len(L)):
            li = lines[i]
            new = color_case(i, li, A[i])
            if new == False:
                return False
            if new is not None:
                C += [new]
        L = []
        for j in range(len(C)):
            cj = col[j]
            new = color_case(j, cj, A[:,j])
            if new == False:
                return False
            if new is not None:
                L += [new]
        C = []
    return A
                
                
    
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
                #print('split : ', split)
            if not(b):
                l.append(split)
            else:
                col.append(split)
    d1 = len(l)
    d2 = len(col)
    Mat = np.zeros((d1,d2)) - np.ones((d1,d2))
    return l, col, Mat

def draw(Matrice):
    plt.imshow(Matrice, cmap='binary', interpolation='nearest')
    plt.colorbar()
    plt.show()
    

if __name__ == "__main__":
    S = [5,2]
    v = T(6, len(S)-1, S)
    print('v : ', v)
    lines, col ,Mat = read_file('instances/0.txt')
    print('lines :', lines)
    print('cols : ', col)
    print('Mat : ', Mat)
    A = coloration(Mat, lines, col)
    print('A : ', A)
    #test = np.zeros((5,6))
    #test[0][0] = 1
    #test[2][2] = -1
    #draw(test)
#plt.show()
