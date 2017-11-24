# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
import os
import sys
from wrapper import *
#import test

#variable global
cpt = 0

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
        print('sl = 0')
        b =  check_color_in(j, line, 1)
        print('y a t-il un noir dans la ligne : ', b)
        print('la fonction retourne ', not(b))
        print('ligne : ', line)
        return not(b)
    #il faut verifier que chaque case n'est pas noir
    if (j == sl - 1):
        #print('cas j = sl - 1')
        print('j : ', j)
        print('l : ', l)
        if l == 0 and not(check_color_in(j, line, 0)):
            return True
        #print('cas j = sl-1 false')
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
        b2 = T2(j-1, l, S,line)
        return b1 or b2
#        print('b2 : ', b2)
#        return b1 or b2

@silent
def color_case(i, S, vecteur):
    print('vecteur : ', vecteur)
    print('i : ', i)
    if vecteur[i] != -1:
        #cas ou la case est deja coloré
        return None
    v = np.copy(vecteur)
    #black
    v[i] = 1
    print('S : ', S)
    black = T2(len(v)-1,len(S)-1,S,v)
    #white
    v[i] = 0
    white = T2(len(v)-1,len(S)-1,S,v)
    print('black : ', black)
    print('white : ', white)
    if not(black) and not(white):
        #la grille n'a pas de solution
        print("La grille n'est pas faisable")
        print("arguments de T2 : j = {}, l = {}, S = {}, v = {}".format(len(v)-1, len(S) -1, S, v))
        return False
    if black and white:
        return None
    if black:
        #on colorie le vecteur en noir
        print('la couleur affecté est noir')
        vecteur[i] = 1
        return i
    print('la couleur affecté est blanche')
    vecteur[i] = 0
    print('i : ', i)
    return i
    
    
def coloration(A, lines, col):
    N, M = A.shape
    L = set([i for i in range(N)])
    C = set([i for i in range(M)])
    print('taille : {},{}'.format(N,M))
    cpt = 0
    while L != set() or C != set():
        for i in L:
            li = lines[i]
            linecolor = A[i]
            for j in range(M):
                print('j : ', j)
                new = color_case(j, li, linecolor)
                print('valeur de new : ', new)
                if new is False:
                    return False
                if new is not None:
                    C.add(new)
        L = set()
        for j in C:
            #print('col :', col)
            #print('j :', j)
            cj = col[j]
            colcolor = A[:,j]
            #print('colcolor ', colcolor)
            for i in range(N):
                new = color_case(i, cj, colcolor)
                if new is False:
                    return False
                if new is not None:
                    L.add(new)
        C = set()
        print('A la fin de la boucle : {}'.format(cpt))
        print('L : {}'.format(L))
        print('C : {}'.format(C))
        print('A : ', A)
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
    lines, col ,Mat = read_file('instances/1.txt')
    print('lines :', lines)
    print('cols : ', col)
    print('Mat : ', Mat)
    A = coloration(Mat, lines, col)
    print('A : ', A)
    draw(A)
#plt.show()
