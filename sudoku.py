#!/usr/bin/python

# Copyright 2013, Gurobi Optimization, Inc.


from gurobipy import *
import numpy as np

def solve(a,b,c,dataType=GRB.CONTINUOUS,GRBobj=GRB.MAXIMIZE):
    nbcont = len(b)
    nbvar = len(c)

    lignes = range(nbcont)
    colonnes = range(nbvar)
    
    m = Model("mogplex") 
    
    # declaration variables de decision
    x = []
    for i in colonnes:
        x.append(m.addVar(vtype=dataType, lb=0, name="x%d" % (i+1)))
        
    # maj du modele pour integrer les nouvelles variables
    m.update()
        
    obj = LinExpr();
    obj =0
    for j in colonnes:
        obj += c[j] * x[j]
            
    # definition de l'objectif
    m.setObjective(obj,GRBobj)
            
    # Definition des contraintes
    if GRBobj == GRB.MAXIMIZE:
        for i in lignes:
            m.addConstr(quicksum(a[i][j]*x[j] for j in colonnes) <= b[i], "Contrainte%d" % i)
    else:
        for i in lignes:
            m.addConstr(quicksum(a[i][j]*x[j] for j in colonnes) >= b[i], "Contrainte%d" % i)
                
    # Resolution
    m.optimize()
                
                
    print ""                
    print 'Solution optimale:'
    for j in colonnes:
        print 'x%d'%(j+1), '=', x[j].x
    print ""
    print 'Valeur de la fonction objectif :', m.objVal


def dual(a,b,c):
    return (np.array(a).T).tolist(), c, b

def main():
    a = [[1,2,3],
         [3,1,1]]
    b = [8,5]
    c = [7,3,4]
    da, db, dc = dual(a,b,c)
    print(da)
    print(db)
    print(dc)
    solve(da,db,dc)

main()
