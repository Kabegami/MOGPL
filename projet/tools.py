# coding: utf-8

import matplotlib.pyplot as plt
import numpy as np
try:
    from scipy import stats
    noLib = False
except:
    noLib = True

import math
import pickle

def toLatexTab(dico, listKey=None,n=None,start=0):
    if listKey is None:
        listKey = dico.keys()
    listKey = list(listKey)
    if n is None:
        n = len(dico[listKey[0]])
    nkey = len(listKey)
    allignement = '|c|'* (nkey + 1)
    s = '\\begin{tabular}{' + allignement + '}\n'
    s += '\\hline\n'
    #Header
    line = 'instances & '
    for key in listKey:
        line += str(key) + ' & '
    line = line[:-2] + "\\\ " + '\n'
    s += line
    s += '\\hline\n'
    for i in range(n):
        line = str(start + i) + ' & '
        for key in listKey:
            data = dico[key]
            #print('data : ', data)
            line += str(data[i]) + ' & '
        line = line[:-2] + "\\\ "
        s += line + '\n'
        s += '\\hline\n'
    s +=  '\\end{tabular}'
    return s
#    for i in range(n):
        

def draw_graphe(L1, L2, xlabel="Nombre de cases a coloriees", ylabel="Temps de calcul"):
    plt.plot(L1, L2)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def multiple_draw_graphe(M, Ltime, xlabel="Nombre de cases a coloriees", ylabel="Temps de calcul", L_label=[]):
    i = 0
    if L_label == []:
        #on remplit de fot label
        while len(L_label) < len(M):
            L_label.append('')
        for L1 in M:
            plt.plot(Ltime, L1,label=L_label[i])
            i += 1
    else:
        for L1 in M:
            plt.plot(Ltime, L1,label=L_label[i])
            i += 1
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()

def verifComplexite(L1, L2):
    """ Si nos données ont une complexitée polynomiale alors on a une fonction de la forme f(x) = a*x^K donc log(f(x)) = log(a) + k * log(b) donc si on trace la courbe au log la pente correspond à K , c'est à dire la complexité """
    global noLib
    if noLib:
        print("La bibliotheque scipy.stats n'est pas présente sur la machine, donc la fonction verifComplexite ne marche pas")
        return None
    t1 = list(map(math.log, L1))
    t2 = list(map(math.log, L2))
    x = np.array(t1)
    y = np.array(t2)
    slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
    return slope

def build_plne_images(start=11, stop=16,dataDir='plneData'):
    for i in range(start, stop+1):
        fname = dataDir + '/' + 'instance'+str(16)

def lireFichier(nom, separation_char='#\n'):
	S = []
	i = 0
	l = 0
	fichier = open(nom, "r")
	for ligne in fichier:
		if ligne != separation_char:
			S.append(list(map(int, ligne.split())))
			i += 1
		else:
			l = i
	fichier.close()

	# Liste de toutes les sequences, nbr de ligne, nbr de colonne
	return S, l, len(S)-l
