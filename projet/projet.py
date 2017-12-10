# coding: utf-8

import pickle
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import profile
import tools
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
    if line[j - (l - 1) - 1] == 1:
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
    if sl == 0:
        return not(check_color_in(j,line,1))
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
                
#=========================================================================================================
#                                             TOOLS
#=========================================================================================================

def save(data, fichier):
    pickle.dump(data, open(fichier, 'wb'), protocol=2)
    print('Données sauvegardées avec succès !')

def load(fichier):
    data = pickle.load(open(fichier, 'rb'))
    return data
    

def timeIt(f , *args):
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

def build_images(start=0, end=10, dirname='instances', dirSave='images', fname='dynamique'):
    for i in range(start, end+1):
        filename= dirname + '/'+str(i)+'.txt'
        lines, col, Mat = read_file(filename)
        A = coloration(Mat, lines, col)
        plt.figure()
        plt.imshow(A, cmap='binary', interpolation='nearest')
        #plt.colorbar()
        if not os.path.exists(dirSave):
            os.mkdir(dirSave)
        name = dirSave + '/' + fname + '_instance' + str(i)
        plt.savefig(name)
        
def build_plne_images(start=11, stop=16, dataDir='plneData', dirSave='images', prefix='plne'):
    for i in range(start, stop+1):
        fname = dataDir + '/' + 'instance'+str(i)
        A = load(fname)
        plt.figure()
        plt.imshow(A, cmap='binary', interpolation='nearest')
        if not os.path.exists(dirSave):
            os.mkdir(dirSave)
        name = dirSave + '/' + prefix + '_instance' + str(i)
        plt.savefig(name)

def load_time(start=11, end=16, dataDir='plneData'):
    L = []
    for i in range(start, end+1):
        name = dataDir + '/' + 'time' + str(i)
        if os.path.exists(name):
            t = load(name)
            L.append(t)
    return L

def robust_load_time(start=0, end=16, dataDir='plneData', default='timeout'):
    L = []
    for i in range(start, end+1):
        name = dataDir + '/' + 'time' + str(i)
        if os.path.exists(name):
            t = load(name)
            L.append(t)
        else:
            L.append(default)
    return L

def robust_time_list(L,start=1,end=16, default='timeout'):
    R = []
    for i in range(start, end+1):
        try:
            elem = L[i]
            R.append(elem)
        except IndexError:
            R.append(default)
    return R

def get_nbCases(start=0, end=16, dirname='instances/'):
    L = []
    for i in range(start, end+1):
        fname = dirname + str(i) + '.txt'
        lines, col, Mat = read_file(fname)
        N,M = Mat.shape
        L.append(N*M)
    return L
        

def save_grid(start=0, end=10, dirname='instances/', objDir='dynamiqueData/', name='instance'):
    if not os.path.exists(objDir):
        os.mkdir(objDir)
    for i in range(start, end+1):
        fname = dirname + str(i)+'.txt'
        lines, col, Mat = read_file(fname)
        A,t  = timeIt(coloration,Mat, lines, col)
        saveFname = objDir + name + str(i)
        timeName = objDir + 'time' + str(i)
        save(A, saveFname)
        save(t, timeName)
    print('Sauvegarde des grilles effectué avec succès !')
        
    
def stat(start=0, end=10, dirname='instances', saveData=False, fichier='data'):
    dico_stat = dict()
    for i in range(start,end+1):
        filename= dirname + '/'+str(i)+'.txt'
        lines, col, Mat = read_file(filename)
        N, K = Mat.shape
        nbCases = N * K
        dico_stat.setdefault('nbCases',[]).append(nbCases)
        nb_cLines = 0
        for c_line in lines:
            nb_cLines += len(c_line)
        dico_stat.setdefault('nb_cLines',[]).append(nb_cLines)
        nb_cCol = 0
        for c_col in col:
            nb_cCol += len(c_col)
        dico_stat.setdefault('nb_cCol',[]).append(nb_cCol)
        
        A, time = timeIt(coloration, Mat,lines, col)
        dico_stat.setdefault('time',[]).append(time)
        print("fin de l'iteration ", i)
    if saveData:
        save(dico_stat, fichier)
    return dico_stat
        
        
    
#=========================================================================================================
#                                             MAIN
#=========================================================================================================

if __name__ == "__main__":
    #build_plne_images(16,16,dataDir='mixData', dirSave='mixImages', prefix='mix')
    d = dict()
    #save_grid()
    d['plne_time'] = robust_load_time()
    d['dynamique_time'] = load_time(0,16, dataDir='dynamiqueData')
    d['nombre de cases'] = get_nbCases()
    L1 =  d['plne_time']
    L2 = d['dynamique_time']
    L3 = d['nombre de cases']
    print('l1 : ', len(L1))
    print('l2 : ', len(L2))
    print('l3 : ', len(L3))
    print('d :', d)
    s = tools.toLatexTab(d,start=0,listKey=['dynamique_time','plne_time','nombre de cases'])
    print(s)
    #d['mix_time'] = load_time(11,16,dataDir='mixData')
    #L = load_time(11,16,dataDir='dynamiqueData')
    #for i in range(len(L)):
    #    d['mix_time'][i] += L[i]
    #d['nombre de cases'] = get_nbCases(11,16)
    # s = tools.toLatexTab(d,start=11,listKey=['plne_time','mix_time','nombre de cases'])
    # L1 = d['plne_time']
    # L1[-1] = max(d['nombre de cases'])
    # tools.multiple_draw_graphe([L1, d['mix_time']],d['nombre de cases'], L_label=['PLNE','mix_time'])
    # print(s)
    #lines, col ,Mat = read_file('instances/8.txt')
    #print('lines', lines)
    #build_images(15,16)
    #build_plne_images(11,15,dataDir='mixData', dirSave='mixImages', prefix='mix')
    #save_grid(11,16)
    #L = load_time(0,8)
    #d = {'time': L}
    #s= tools.toLatexTab(d,start=11)
    #print('S : ', s)
    #print('L : ', L)
    #L = robust_time_list(L,0,10,1000)
#    d = {'plne-time' : L}
    #A = coloration(Mat, lines, col)
    #print('A : ', A)
    #draw(A)
    #dico = stat(0,10,saveData=False)
    #dico = load('data')
    #print('dico : ', dico)
    #L1 = dico['nbCases']
    #L2 = dico['time']
    #d['dynamique-time'] = L2

    #s = tools.toLatexTab(d,start=0)
    #print(s)
    #tools.multiple_draw_graphe([L,L2[:9]],L1[:9], L_label=['PLNE','programation dynamique'])
    #tools.draw_graphe(L1,L2)
    #q = tools.verifComplexite(L1,L2)
    #print('complexité : ', q)
    
#plt.show()
