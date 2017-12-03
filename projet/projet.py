# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import profile
from wrapper import *
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

@memo_id
def T2(j, l, S, line):
    if j < 0 and l >= 0:
        return False
    if j < 0 and l < 0:
        return True   
    if l < 0:
        return not(check_color_in(j,line,1))
    sl = S[l]
    #il faut verifier qu'il n'y a aucune case blanche
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
           
        return T2(j-sl-1, l-1, S, line[:j-sl]) or T2(j-1, l, S,line[:-1])

def color_case(i, S, vecteur):
    """ on fait un copie du vecteur sous forme de tuple pour manipuler uniquement des tuples dans T2 """
    if vecteur[i] != -1:
        #cas ou la case est deja coloré
        return None
    #black
    vecteur[i] = 1
    blackTuple = tuple(vecteur)
    N = len(vecteur)
    black = T2(N-1,len(S)-1,tuple(S),blackTuple)
    #white
    vecteur[i] = 0
    whiteTuple = tuple(vecteur)
    #white = T2(N-1,len(S)-1,S,vecteur)
    white = T2(N-1, len(S)-1, tuple(S), whiteTuple)
    if not(black) and not(white):
        #la grille n'a pas de solution
        return False
    if black and white:
        vecteur[i] = -1
        return None
    if black:
        #on colorie le vecteur en noir
        vecteur[i] = 1
        return i
    vecteur[i] = 0
    return i

@timer
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
                    return False
                if new is not None:
                    L.add(new)
        C = set()
        #print('tour de boucle numero : ', cpt)
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
    Mat = np.zeros((d1,d2)) - np.ones((d1,d2))
    return l, col, Mat

def draw(Matrice):
    plt.imshow(Matrice, cmap='binary', interpolation='nearest')
    plt.colorbar()
    plt.show()
    

if __name__ == "__main__":
    lines, col ,Mat = read_file('instances/9.txt')
    A = coloration(Mat, lines, col)
    draw(A)
    print('temps de calcul des clefs : ', memo_id.keyTime)
#plt.show()
