# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt

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
            #il faut verifier qu'il n'a pas de voisin et que la serie fait la bonne taille et finie pas un blanc ou non colorié
            for i in range(1,l):
                if line[j-i] == 0:
                    return False
            #dernier car
            print('derniere case apres le bloc : ', i)
            if line[j - i - 1] != 1:
                return False
            return T2(j-sl-1, l-1,S, line)
        #cas blanc
        if line[j] == 0:
            return T2(j-1, l, S,line)
        #cas non determiner
        print('non determiner')
        b1 = T2(j-sl-1, l-1,S, line)
        print('b1 : ', b1)
        b2 = T2(j-1, l, S,line)
        print('b2 : ', b2)
        return b1 or b2
            
    
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

def test_T():
    assert(T(10, 1, [5,2]) == True)
    assert(T(7, 1, [5,2]) == True)
    assert(T(6, 1, [5,2]) == False)
    assert(T(3, 0, [4]) == True)

def test_T2():
    e1 = np.array([1,1,1,-1,-1])
    e2 = np.array([1,-1,-1,-1,-1])
    e3 = np.array([1,-1,0,-1,-1])
    e4 = np.array([1,0,-1,-1,0,-1])
    print('Example 1')
    assert(T2(4, 0, [3], e1) == True)
    print('Example 2')
    assert(T2(4, 0, [3], e2) == True)
    print('Example 3')
    assert(T2(4,0,[3],e3) == False)
    print('Example 4')
    assert(T2(4,0,[3],e4) == False)
    
    

def draw(Matrice):
    plt.imshow(Matrice, cmap='binary', interpolation=None)
    plt.colorbar()
    plt.show()
    


S = [5,2]
v = T(6, len(S)-1, S)
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
