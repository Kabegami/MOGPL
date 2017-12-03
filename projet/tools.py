import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import math

def draw_graphe(L1, L2, xlabel="Nombre de cases à coloriées", ylabel="Temps de calcul"):
    plt.plot(L1, L2)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def multiple_draw_graphe(M, Ltime, xlabel="Nombre de cases à coloriées", ylabel="Temps de calcul", L_label=[]):
    i = 0
    if L_label != []:
        while len(L_label) < len(M):
            L_label.append('')
        for L1 in M:
            plt.plot(L1, Ltime,label=L_label[i])
            i += 1
    else:
        for L1 in M:
            plt.plot(L1, Ltime,label=L_label[i])
            i += 1
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()

def verifComplexite(L1, L2):
    """ Si nos données ont une complexitée polynomiale alors on a une fonction de la forme f(x) = a*x^K donc log(f(x)) = log(a) + k * log(b) donc si on trace la courbe au log la pente correspond à K , c'est à dire la complexité """
    t1 = list(map(math.log, L1))
    t2 = list(map(math.log, L2))
    x = np.array(t1)
    y = np.array(t2)
    slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
    return slope
