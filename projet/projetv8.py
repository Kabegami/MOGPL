# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
from wrapper import *
from matrice import *
#import test

#variable global
cpt = 0

#pour changer la variable debug utiliser
#set_debug(boolean)

        


def check_color_in(j, line, color):
    """ j : int plus grandes cases, lines : array, color : int {blanc : 0, noir = 1, indeter = -1}"""
    for i in range(0, j+1):
        if line[i] == color:
            return True
    return False

def T(j, l, S):
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


def possible_block(j, l, line):
    for i in range(0,l):
        if line[j-i] == 0:
            return False
        if j - i < 0:
            return False
    #dernier car
    if line[j - i - 1] == 1:
        return False
    return True

#il faut utiliser la memoisation

@memo
def T2(j, l, S, line):
    if j < 0 and l >= 0:
        return False
    if j < 0 and l < 0:
        return True   
    if l == -1:
        if line[j] == 1:
            return False
        if j == 0:
            return True
        return T2(j-1,l,S,line[:-1])
    sl = S[l]
    if sl == 0:
        b =  check_color_in(j, line, 1)
        return not(b)
    #il faut verifier que chaque case n'est pas noir
    if (j == sl - 1):
        if l == 0 and not(check_color_in(j, line, 0)):
            return True
        return False
    if (j>(sl - 1)):
        #cas noir
        if line[j] == 1:
            if not(possible_block(j, sl, line)):
                return False
            return T2(j-sl-1, l-1,S, line[:j-sl])
        #cas blanc
        if line[j] == 0:
            return T2(j-1, l, S,line[:-1])
        #cas non determiner
        #Quand on a pas de bloc forcement vrai.... du coup on peut toujours placer un bloc sur une case indeterminer
        if not(possible_block(j, sl, line)):
            return T2(j-1, l, S,line[:-1])
           
        b1 = T2(j-sl-1, l-1,S, line[:j-sl])
        b2 = T2(j-1, l, S,line[:-1])
        return b1 or b2
#        return b1 or b2


def color_case(i, S, vecteur):
    #a priori a chaque fois qu'on change de valeur on renvoi v qui a une nouvelle adresse memoire
    if vecteur[i] != -1:
        #cas ou la case est deja coloré
        return None, vecteur
    N = len(vecteur)
    vblack = list(vecteur)
    #black
    vblack[i] = 1
    black = T2(N-1,len(S)-1,S,vblack)
    #white
    vwhite = list(vecteur)
    vwhite[i] = 0
    print('vwhite :' ,vwhite)
    print('N -1 :' ,N-1)
    print('verif existance key : ')
    key = (i, id(S), id(vwhite))
    if key in memo.dico:
       print('la clef existe ') 
    b = id(vblack) == id(vwhite) == id(vecteur)
    white = T2(N-1,len(S)-1,S,vwhite)
    print('white : ', white)
    if not(black) and not(white):
        #la grille n'a pas de solution
        print('echec pour vecteur = {}, i = {}, S = {}'.format(vecteur, i, S))
        return False,vecteur
    if black and white:
        return None, vecteur
    if black:
        #on colorie le vecteur en noir
        return i,vblack
    return i,vwhite
    
@timer
def coloration(A, lines, col):
    N, M = A.nblines, A.nbcols
    L = set([i for i in range(N)])
    C = set([i for i in range(M)])
    cpt = 0
    while L != set() or C != set():
        for i in L:
            li = lines[i]
            for j in range(M):
                new, newline = color_case(j, li, A.lines[i])
                print('new :' ,new)
                A.lines[i] = newline
                if new is False:
                    return False
                if new is not None:
                    C.add(new)
        L = set()
        for j in C:
            cj = col[j]
            for i in range(N):
                new, newcol = color_case(i, cj, A.cols[j])
                A.cols[j] = newcol
                if new is False:
                    return False
                if new is not None:
                    L.add(new)
        print('A :' ,A)
        C = set()
            
        cpt += 1
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
            if not(b):
                l.append(split)
            else:
                col.append(split)
    f.close()
    d1 = len(l)
    d2 = len(col)
    #Mat = np.zeros((d1,d2)) - np.ones((d1,d2))
    lines = []
    cols = []
    for i in range(d1):
        L = [-1 for i in range(d2)]
        lines.append(L)
    for j in range(d2):
        c = [-1 for i in range(d1)]
        cols.append(c)
    Mat = Matrice(lines, cols)
    return l, col, Mat

def draw(Matrice):
    plt.imshow(Matrice, cmap='binary', interpolation='nearest')
    plt.colorbar()
    plt.show()
    

if __name__ == "__main__":
    S = [5,2]
    v = T(6, len(S)-1, S)
    lines, col ,Mat = read_file('instances/0.txt')
    print('taille lines :', len(lines))
    print('taille col : ', len(col))
    Mat.printLine()
    #print('Mat : ', Mat)
    A = coloration(Mat, lines, col)
    print('A final : ')
    A.printLine()
#    draw(A)
#plt.show()
