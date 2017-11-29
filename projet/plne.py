#!/usr/bin/python

# Copyright 2013, Gurobi Optimization, Inc.


from gurobipy import *
from projetv2 import read_file
import numpy as np

def solve(a,b,c):
    """ a, b, c des matrices numpy"""
    nbcont = len(b)
    nbvar = len(c)

    lignes = range(nbcont)
    colonnes = range(nbvar)
    
    m = Model("mogplex") 
    
    # declaration variables de decision
    x = []
    for i in colonnes:
        x.append(m.addVar(vtype=GRB.INTEGER, lb=0, name="x%d" % (i+1)))
        
    # maj du modele pour integrer les nouvelles variables
    m.update()
        
    obj = LinExpr();
    obj =0
    for j in colonnes:
        obj += c[j] * x[j]
            
    # definition de l'objectif
    m.setObjective(obj,GRB.MAXIMIZE)
            
    # Definition des contraintes
    for i in lignes:
        m.addConstr(quicksum(a[i][j]*x[j] for j in colonnes) <= b[i], "Contrainte%d" % i)
                
    # Resolution
    m.optimize()
                
                
    print(""                )
    print('Solution optimale:')
    for j in colonnes:
        print ('x%d'%(j+1), '=', x[j].x)
    print ("")
    print ('Valeur de la fonction objectif :', m.objVal)


def dual(a,b,c):
    return a.T, c, b

def solve_pb(Mat, lines, col):
    

def main():
    #lines, col, Mat = read_file('instances/11.txt')
    #================================
    #      TEST
    Mat = np.array([[-1,-1,-1],[-1,-1,-1]])
    lines = np.array([[2],[1]])
    col = np.array([[1],[1],[1]])
    N, K = Mat.shape
    #creation du vecteur obj c
    c = np.ones((N,K))
    Y = []
    for contrainte in lines:
        #contraintes sur les lignes
        L = []
        for t in contrainte:
            L.append([0 for i in range(K)])
        Y.append(L)
    Y = np.array(Y)
    print('Y : ', Y)
    print('c : ', c)
    #creation de la matrices des contraintes

main()
