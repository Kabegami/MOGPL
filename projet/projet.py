# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt

#variable global
cpt = 0

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

def T2(j, l, S, line):
    if l == -1:
        return True
    sl = S[l]
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
        print('b1 : ', b1)
        return b1
#        b2 = T2(j-1, l, S,line)
#        print('b2 : ', b2)
#        return b1 or b2
            
    
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
                split = -1
            else:
                split = int(split[0])
            #print('split : ', split)
            if not(b):
                l.append(split)
            else:
                col.append(split)
    d1 = len(l)
    d2 = len(col)
    Mat = np.zeros((d1,d2)) - np.ones((d1,d2))
    return l, col, Mat

def sp():
    """ print pour les Assert , attention cpt est une liste ! """
    global cpt
    print('====================================================')
    print('                      TEST {}                       '.format(cpt))
    print('====================================================')
    cpt += 1
    

def test_T():
    assert(T(10, 1, [5,2]) == True)
    assert(T(7, 1, [5,2]) == True)
    assert(T(6, 1, [5,2]) == False)
    assert(T(3, 0, [4]) == True)

def test_T2():
    global cpt
    e1 = np.array([1,1,1,-1,-1])
    e2 = np.array([1,-1,-1,-1,-1])
    e3 = np.array([1,-1,0,-1,-1])
    e4 = np.array([1,0,-1,-1,0,-1])
    cpt = 0
    sp()
    assert(T2(4, 0, [3], e1) == True)
    sp()
    assert(T2(4, 0, [3], e2) == True)
    sp()
    assert(T2(4,0,[3],e3) == False)
    sp()
    assert(T2(4,0,[3],e4) == False)

def test_possible_block():
    a1 = [-1,-1,-1,-1,-1]
    sl1 = 5
    a2 = [-1, -1, 0, -1, -1]
    
    assert(possible_block(4,sl1, a1) == True)
    assert(possible_block(3, sl1, a1) == False)
    assert(possible_block(0, sl1, a1) == False)

    assert(possible_block(4,sl1, a2) == False)
    assert(possible_block(3, sl1, a2) == False)
    assert(possible_block(0, sl1, a2) == False)
    

def draw(Matrice):
    plt.imshow(Matrice, cmap='binary', interpolation='nearest')
    plt.colorbar()
    plt.show()
    


S = [5,2]
v = T(6, len(S)-1, S)
test_possible_block()
test_T()
test_T2()
print('v : ', v)
lines, col, Mat = read_file('Instances/test1')
print('lines :', lines)
print('cols : ', col)
print('Mat : ', Mat)
test = np.zeros((5,6))
test[0][0] = 1
test[2][2] = -1

draw(test)
#plt.show()
