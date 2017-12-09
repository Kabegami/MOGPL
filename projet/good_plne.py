#!/usr/bin/python
#-*- coding: utf-8 -*-
# Copyright 2013, Gurobi Optimization, Inc.

from gurobipy import *
from projet import *
from tools import *
import numpy as np

"""
def X_to_array(X, K):
    M = []
    L = []
    cpt = 0
    for xi in X:
        for i in xi:
            print('i : ', i)
            if cpt % K == 0 and cpt != 0:
                M.append(L)
                L = []
            L.append(i.x)
            cpt += 1
    M.append(L)
    return np.array(M)
"""

def to_array(X, N, M):
        """ X : dict """
        A = np.zeros((N,M))
        for keys in X.keys():
                v = int(X[keys].x)
                #print('V : ', v)
                i,j = keys
                A[i][j] = v
        return A

############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################

def variables(N, M, Sligne, Scolonne, model):
	X, Y, Z = {}, {}, {}
	for i in range(N):
			for j in range(M):
				X[i,j] = model.addVar(vtype=GRB.BINARY, lb=0, name= 'X{}{}'.format(i,j))
				for t in range(len(Sligne[i])):
				    Y[i,j,t] = model.addVar(vtype=GRB.BINARY, lb = 0, name = 'Y{}{}{}'.format(i,j,t))
				for t in range(len(Scolonne[j])):
					Z[i,j,t] =  model.addVar(vtype=GRB.BINARY, lb = 0, name = 'Z{}{}{}'.format(i,j,t))	
	
	model.update()
	return X, Y, Z
	
def contrainte(X, Y, Z, N, M, Sligne, Scolonne, model):
	for i in range(N):
		for t in range(len(Sligne[i])):
			CY = []
			coef = []	
			for j in range(M):
				CY .append(Y[i,j,t])
				coef.append(1)
			model.addConstr(LinExpr(coef, CY), '<=', 1, name = "Somme des y vaut 1")
			model.addConstr(LinExpr(coef, CY), '>=', 1, name = "Somme des y vaut 1")
			
	for j in range(M):
		for t in range(len(Scolonne[j])):
			CZ = []
			coef = []	
			for i in range(N):
				CZ .append(Z[i,j,t])
				coef.append(1)
			model.addConstr(LinExpr(coef, CZ), '<=', 1, name = "Somme des z vaut 1")
			model.addConstr(LinExpr(coef, CZ), '>=', 1, name = "Somme des z vaut 1")
		
	################################################################################
	################################################################################

        #Cette contrainte empeche le bloc t+1 d'etre place mais pas les autre (t+2 ect)
        #faire une contrainte qui empeche les bloc Yi,j t < Yi,j t + i pour tous i
#         for i in range(N):
#                 for t in range(0,len(Sligne[i])-1):
#                         for j in range(0, M):
#                                 #print('boucle des j')
#                                 CY = [Y[i,j,t]]
#                                 coef = [1]
#                                 for prime in range(t+1, len(Sligne[i])):
# #                                        CY = [Y[i,j,t]]
# #                                        coef = [1]
#                                         for k in range(j, min(j + Sligne[i][t]+1, M)):
#                                                    #print('j == k ', j == k)
#                                                    CY.append(Y[i,k, prime])
#                                                    coef.append(1)
#                                         model.addConstr(LinExpr(coef, CY), '<=', 1, name = "decalage necessaire y")

        for i in range(N):
                for t in range(0, len(Sligne[i])-1):
                        for j in range(M):
                               CY = [Y[i,j,t]]
                               coef = [1]
                               for k in range(0, min(j+Sligne[i][t]+1, M)):
                                       CY.append(Y[i,k,t+1])
                                       coef.append(1)
                               model.addConstr(LinExpr(coef, CY), '<=', 1, name='decalage nececessaire y')

        for j in range(M):
                for t in range(0, len(Scolonne[j])-1):
                        for i in range(N):
                                CZ = [Z[i,j,t]]
                                coef = [1]
                                for k in range(0, min(i + Scolonne[j][t]+1, N)):
                                        CZ.append(Z[k,j,t+1])
                                        coef.append(1)
                                model.addConstr(LinExpr(coef, CZ), '<=', 1, name='decalage nececessaire y')
                                
                        


                
#         for j in range(M):
#                 for t in range(len(Scolonne[j])-1):
#                         for i in range(N):
#                                 CY = [Z[i,j,t]]
#                                 coef = [1]
#                                 for prime in range(t+1, len(Scolonne[j])):
# #                                        CY = [Z[i,j,t]]
# #                                        coef = [1]
#                                         for k in range(i, min(i + Scolonne[j][t]+1, N)):
#                                                 CY.append(Z[k,j, t+1])
#                                                 coef.append(1)
#                                         print('CZ : ', CY)
#                                         print('coef : ', coef)
#                                         model.addConstr(LinExpr(coef, CZ), '<=', 1, name = "decalage necessaire z")

    
			
		 
	################################################################################
	################################################################################

        for i in range(N):
                CY = []
                coef = []
                b = sum(Sligne[i])
                for j in range(M):
                        CY.append(X[i,j])
                        coef.append(1)
                model.addConstr(LinExpr(coef, CY), '<=', b, name = "il ne peut pas avoir plus de case noires")

        for j in range(M):
                CZ = []
                coef = []
                b = sum(Scolonne[j])
                for i in range(N):
                        CZ.append(X[i,j])
                        coef.append(1)
                model.addConstr(LinExpr(coef, CZ), '<=', b, name = "il ne peut pas avoir plus de case noires")

	################################################################################
	################################################################################                
        
        for i in range(N):
                for j in range(M):
                        for t in range(len(Sligne[i])):
                                CY = [Y[i,j,t]]
                                coef = [1]
                                k = j + Sligne[i][t]
                                #print('k : ', k)
                                if k < M:
                                        CY.append(X[i,k])
                                        coef.append(1)
                                        model.addConstr(LinExpr(coef, CY), '<=', 1, name = "case blanche apres bloc y")

        for j in range(M):
                for t in range(len(Scolonne[j])):
                        for i in range(N):
                                #print('i : {}, j : {}'.format(i,j))
                                CY = [Z[i,j,t]]
                                coef = [1]
                                k = i + Scolonne[j][t], N-1
                                if k < N:                                        
                                        CY.append(X[k,j])
                                        coef.append(1)
                                        model.addConstr(LinExpr(coef, CY), '<=', 1, name = "case blanche apres bloc z")
                                
        
	################################################################################
	################################################################################
        
        for i in range(N):
                for t in range(len(Sligne[i])):
                        for j in range(0, M):
                                CY = []
                                coef = []
                                for k in range(j,  min(j+Sligne[i][t], M)):
                                        CY.append(X[i,k])
                                        coef.append(1)
                                CY.append(Y[i,j,t])
                                coef.append(-Sligne[i][t])
                                model.addConstr(LinExpr(coef, CY), '>=', 0, name = "cases noires y")

        for j in range(M):
                for t in range(len(Scolonne[j])):
                        for i in range(0, N):
                                CZ = []
                                coef = []
                                for k in range(i,  min(i+Scolonne[j][t], N)):
                                        CZ.append(X[k,j])
                                        coef.append(1)
                                CZ.append(Z[i,j,t])
                                coef.append(-Scolonne[j][t])
                                model.addConstr(LinExpr(coef, CZ), '>=', 0, name = "cases noires z")
                                
                                

        ################################################################################
	################################################################################



	model.update()



def solve(S, N, M, timeout = False):
    model = Model("mogpl")
    Sligne, Scolonne = S[:N], S[N:]
    X, Y, Z = variables(N, M, Sligne, Scolonne, model)
    
    obj = []
    coef = []
    for i in range(N):
        for j in range(M):
            obj.append(X[i,j])
            coef.append(1)
    model.setObjective(LinExpr(coef,obj), GRB.MINIMIZE)
    model.update()
    
    contrainte(X, Y, Z, N, M, Sligne, Scolonne, model)
    
    model.optimize()
    for yi in Y:
        print(Y[yi])
        
    for zi in Z:
        print(Z[zi])        
    A = to_array(X, N, M)
    return A, model.Runtime
    #print('A : ', A)
    #draw(A)

def compute_instance(start=11, end=16):
        for i in range(start, end+1):
                filename = 'instances/' + str(i) + '.txt' 
                dataName = 'plneData/' +'instance' + str(i)
                timeName = 'plneData/' + 'time' + str(i)
                S,N,M = lireFichier(filename)
                A,t = solve(S,N,M)
                save(A, dataName)
                save(t, timeName)
                
        
		
def main():
    compute_instance(11,15)
    #S, N, M = lireFichier('instances/13.txt')
    #L = solve(S,N,M)
    #print(L)


if __name__ == '__main__':
	main()

