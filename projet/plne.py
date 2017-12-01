#!/usr/bin/python
# coding: utf-8
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
    m.setObjective(obj,GRB.MINIMIZE)
            
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

def create_variable(Mat, lines, col):
    N, K = Mat.shape
    C = np.ones((N,K))
    m = Model("mogplex")
    X = []
    T1 = len(lines)
    T2 = len(col)
    Y = dict()
    Z = dict()
    for i in range(N):
        b = True
        T = []
        for j in range(K):
            T.append(m.addVar(vtype=GRB.BINARY, lb=0, name='X'+str(i)+str(j)))
            for t1 in range(len(lines)):
                M = Y.get(t1, [[0 for o in range(K)] for p in range(N)])
                print(' M : ', M)
                print('i : {}, j : {}'.format(i,j))
                M[i][j] = (m.addVar(vtype=GRB.BINARY, lb=0, name='Y[{}]{}{}'.format(t1, i, j)))
                Y[t1] = M
            for t2 in range(len(col)):
                M = Z.get(t2, [[0 for q in range(N)] for z in range(K)])
                M[j][i] = (m.addVar(vtype=GRB.BINARY, lb=0, name='Z[{}]{}{}'.format(t2, i, j)))
                Z[t2] = M
        X.append(T)
        
    m.update()
    obj = LinExpr();
    obj = 0
    for i in range(N):
        for j in range(K):
            obj += 1 * X[i][j]
    m.setObjective(obj, GRB.MINIMIZE)

    s = 0
#    print('Y : ', Y)
    #contrainte sur les j
    for i in range(N):
        for t in Y.keys():
            s = 0
            yt= Y[t]
            #print('yt :' , yt)
            for j in range(K):
                s += yt[i][j]
            m.addConstr(s <= 1,'contrainte unicité > y ' + str(t))
            m.addConstr(s >= 1,'contrainte unicité < y ' + str(t))

    for j in range(K):
        for t in Y.keys():
            s = 0
            zt= Z[t]
            for i in range(N):
                s += zt[j][i]
            m.addConstr(s <= 1,'contrainte unicité > z ' + str(t))
            m.addConstr(s >= 1,'contrainte unicité < z ' + str(t))

    #print('M')
    #print(Y[0])
    print('Z')
    print(Z[0])
    #contraintes sur le pose bloc ligne
    for i in range(0, N):
        for t in range(0,len(Y.keys())):
            for j in range(0, K - lines[t]):
                yt = Y[t]
                s = yt[i][j]
                for k in range(j,j+lines[t]):
                    for prime in range(t+1, T1):
                        s += (Y[prime])[i][k]
                m.addConstr(s <= 1, 'contrainte pose bloc lignes Y[{}]{}{}'.format(t,i,j))
    
    #contraintes sur le pose bloc ligne
    for j in range(0, K):
        for t in range(0,len(Z.keys())):
            for i in range(0, N - col[t]):
                zt = Z[t]
                s = zt[j][i]
                for k in range(i,i+col[t]):
                    for prime in range(t+1, T1):
                        s += (Z[prime])[j][k]
                m.addConstr(s <= 1, 'contrainte pose bloc lignes Z[{}]{}{}'.format(t,i,j))
    
    

    print('X')
    for xi in X:
        print(xi)      


def solve_pb(Mat, lines, col):
    pass

def main():
    #lines, col, Mat = read_file('instances/11.txt')
    #================================
    #      TEST
    Mat = np.array([[-1,-1,-1],[-1,-1,-1]])
    lines = np.array([[2],[1]])
    col = np.array([[1],[1],[1]])
    N, K = Mat.shape
    create_variable(Mat, lines, col)
    #creation du vecteur obj c
    #c = np.ones((N,K))
    #Y = []
    #for contrainte in lines:
    #    #contraintes sur les lignes
    #    L = []
    #    for t in contrainte:
    #        L.append([0 for i in range(K)])
    #    Y.append(L)
    #Y = np.array(Y)
    #print('Y : ', Y)
    #print('c : ', c)
    #creation de la matrices des contraintes

main()
