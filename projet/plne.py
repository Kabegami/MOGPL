#!/usr/bin/python
#-*- coding: utf-8 -*-
# Copyright 2013, Gurobi Optimization, Inc.


from gurobipy import *
from projet import *
import numpy as np

def get_list(L, index, default=None):
    try:
        return L[index]
    except IndexError:
        return default

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

def test_simple1():
    Mat = np.array([-1,-1,-1])
    Mat = np.reshape(Mat, (1,len(Mat)))
    print('Mat : ,', Mat)
    lines = np.array([[2]])
    col = np.array([[1],[1],[0]])
    A = solve(Mat, lines, col)
    draw(A)

def test_simple2():
    Mat = np.array([[-1],[-1],[-1]])
    Mat = np.reshape(Mat, (len(Mat),1))
    print('Mat : ,', Mat)
    lines = np.array([[1],[1],[0]])
    col = np.array([[2]])
    A = solve(Mat, lines, col)
    draw(A)

def test_simple3():
    Mat = np.array([[-1,-1,-1,-1,-1]])
    Mat = np.reshape(Mat, (1,len(Mat[0])))
    print('Mat : ', Mat)
    lines = np.array([[2,2]])
    col = np.array([[1],[1],[0],[1],[1]])
    A = solve(Mat, lines, col)
    draw(A)

def test_simple4():
    Mat = np.array([[-1,-1,-1,-1,-1],
                    [-1,-1,-1,-1,-1]])
    #Mat = np.reshape(Mat, (1,len(Mat[0])))
    print('Mat : ', Mat)
    lines = np.array([[3,1],[3]])
    col = np.array([[1],[1],[2],[1],[2]])
    A = solve(Mat, lines, col)
    draw(A)
                 

def test_overlap():
    Mat = np.array([[-1,-1,-1,-1],[-1,-1,-1,-1]])
    lines = np.array([[2,1],[1]])
    col = np.array([[1],[1],[1],[1]])
    A = solve(Mat, lines, col)
    draw(A)


def solve(Mat, lines, col):
    N, K = Mat.shape
    C = np.ones((N,K))
    m = Model("mogplex")
    X = []
    T1 = len(lines)
    T2 = len(col)
    Y = dict()
    Z = dict()
    listContraintes = []
    
    #on verra apres
    #startLine = []
#    for i in range(len(lines)):
#        Lcontrainte = lines[i]
#        taille = len(lines[i])
#        line = []
#        for j in range(1,taille):
#            line.append(Lcontrainte[j] + 1)
#        startLine.append(line)

    #stopLine = []
    #for i in range(len(lines)):
    #    Lcontrainte = lines[i]
    #    taille = len(lines[i])
    #    line = []
    #    for l in range(0,taille):
    #        s = N - lines[l]
    #       for n in range(l+1, taille):
    #            s = -lines[n] - 1
    #        print('s : ',s)
    #        line.append(s)
    #    stopLine.append(line)
#    print('startLine :')
#    print(startLine)
#    print('stop line')
#    print(stopLine)


    Y2 = dict()
    for i in range(0, N):
        M2 = Y2.get(i, [[0 for j in range(0,K)] for t in range(0,len(lines[i]))])
        for t1 in range(0, len(lines[i])):
            for j in range(0, K):
                M2[t1][j] = (m.addVar(vtype=GRB.BINARY, lb=0, name='Y[{}]{}{}'.format(t1, i, j)))
        Y2[i] = M2

    Z2 = dict()
    for j in range(0, K):
        M2 = Z2.get(j, [[0 for i in range(0,N)] for t in range(0,len(col[j]))])
        for t2 in range(0, len(col[j])):
            for i in range(0, N):
                M2[t2][i]  = (m.addVar(vtype=GRB.BINARY, lb=0, name='Z[{}]{}{}'.format(t2, i, j)))
        Z2[j] = M2
    #print('Y2 : ', Y2)

    for i in range(0,N):
        T = []
        for j in range(0,K):
            T.append((m.addVar(vtype=GRB.BINARY, lb=0, name='X'+str(i)+str(j))))
        X.append(T)
    
            
    
    #for i in range(N):
#        b = True
#        T = []
#        for j in range(K):
#            T.append(m.addVar(vtype=GRB.BINARY, lb=0, name='X'+str(i)+str(j)))
#            for t1 in range(0,len(lines[i])):
#                print('t1', t1)
#                M2 = Y2.get(i, [[0 for j in range(0,K)] for t in range(0,len(lines[i]))])
#                #print('M2 : ', M2)
#                M = Y.get(t1, [[0 for o in range(K)] for p in range(N)])
#                M[i][j] = (m.addVar(vtype=GRB.BINARY, lb=0, name='Y[{}]{}{}'.format(t1, i, j)))
#                M2[t1][j] = (m.addVar(vtype=GRB.BINARY, lb=0, name='Y[{}]{}{}'.format(t1, i, j)))
#                #print('i : {},j : {},t : {}'.format(i,j,t1))
#                #print('M : ', M)
#                Y[t1] = M
#                Y2[i] = M2
#            for t2 in range(0,len(col[j])):
#                M = Z.get(t2, [[0 for q in range(N)] for z in range(K)])
#                M[j][i] = (m.addVar(vtype=GRB.BINARY, lb=0, name='Z[{}]{}{}'.format(t2, i, j)))
#                Z[t2] = M
#        X.append(T)
        
    m.update()
    print('X : ', X)
    print('Y2 : ', Y2)
    print('Z2 : ', Z2)
    obj = LinExpr();
    obj = 0
    for i in range(0,N):
        for j in range(0,K):
            obj += 1 * X[i][j]
    m.setObjective(obj, GRB.MINIMIZE)

    s = 0
#    print('Y : ', Y)
    #contrainte sur les j
    for i in range(0,N):
        Yi = Y2[i]
        for t in range(len(lines[i])):
            s = 0
            yt= Yi[t]
            #print('yt :' , yt)
            for j in range(0,K):
                s += yt[j]
            v = m.addConstr(s <= 1,'contrainte unicité > y ' + str(t))
            m.addConstr(s >= 1,'contrainte unicité < y ' + str(t))

    for j in range(0,K):
        Zj = Z2[j]
        for t in range(0, len(col[j])):
            s = 0
            zt= Zj[t]
            for i in range(0,N):
                s += zt[i]
            print('unicité s : ', s)
            m.addConstr(s <= 1,'contrainte unicité > z ' + str(t))
            m.addConstr(s >= 1,'contrainte unicité < z ' + str(t))

    #contraintes sur le pose bloc ligne
    for i in range(0, N):
        Yi = Y2[i]
        lc = lines[i]
        for t in range(0,len(lines[i])):
            yt = Yi[t]
            st = lc[t]
            start = sum([lc[p] + 1 for p in range(0, t)])
            end = K - st - sum([lc[q] + 1 for q in range(t + 1, len(lc))])
            #normalement N = 1 pour le test2 par 3 ...
            print('N : ', N)
            print('K : ', K)
            print('start : ', start)
            print('end :', end)
            print('taille ligne : ', len(lines[i]))
            for j in range(start, end):
                print('j : ', j)
                print('Yt : ', yt)
                s = yt[j]
                for k in range(j, j + st):
                    for prime in range(t+1, len(lines[i])):
                        s += (Y2[i][prime][j])
                print('s : ' ,s)
                #j'ai une contrainte pour chaque i et chaque j
                m.addConstr(s <= 1, 'contrainte pose bloc lignes Y[{}]{}{}'.format(t,i,j))
                #reset s
                s = 0
    
    #contraintes sur le pose bloc ligne
    for j in range(0, K):
        Zj = Z2[j]
        cc = col[j]
        for t in range(0,len(col[j])):
            st = cc[t]
            zt = Zj[t]
            start = sum([cc[p] +1 for p in range(0, t)])
            end = N - st - sum([lc[q] + 1 for q in range(t + 1, len(cc))])
            for i in range(0, N):
                s = zt[i]
                for k in range(i,i+col[j]):
                    for prime in range(t+1, len(col[j])):
                        s += (Z2[j][prime][i])
                m.addConstr(s <= 1, 'contrainte pose bloc lignes Z[{}]{}{}'.format(t,i,j))
                #reset s
                s = 0
                

    #Actuellement, le prg pose tous les bloc sur la meme case !
    #C'est cette contrainte qui provoque le bug
    for i in range(0, N):
        lc = lines[i]
        Yi = Y2[i]
        for t in range(0, len(lc)):
            yt = Yi[t]
            ytPlus = get_list(Yi, t+1)
            #ytPlus = Yi.get(t+1, None)      
            st = lc[t]
            s = 0
            #start = sum([lc[p] + 1 for p in range(0, t)])
            #end = N - st - sum([lc[q] + 1 for q in range(t + 1, len(lc))])
            for j in range(0, K):
                s += yt[j]
                if ytPlus is not None:
                    for k in range(j, min(j + st+1,K-1)):
                        print(' k ' , k)
                        s += ytPlus[k]
                print('s overlap : ', s)
                m.addConstr(s <= 1 , 'contrainte taille bloc Y')
                #reset s
                s = 0

    #C'est cette contrainte qui provoque le bug
    for j in range(0, K):
        cc = col[j]
        Zj = Z2[j]
        for t in range(0, len(cc)):
            zt = Zj[t]
            ztPlus = get_list(Zj, t+1)
            st = col[j][t]
            s = 0
            for i in range(0, N):
                s += zt[i]
                if ztPlus is not None:
                    #normalement on peut enlever le min quand la contrainte debut/fin bloc implémenté
                    for k in range(i, min(i + st+1,N-1)):
                        s += ztPlus[i][k]
                m.addConstr(s <= 1 , 'contrainte taille bloc Z')

    for i in range(0,N):
        lc = lines[i]
        Yi = Y2[i]
        for t in range(0, len(lc)):
            s = 0
            #t eme bloc
            st = lc[t]
            print('st : ' ,st)
            yt = Yi[t]
            for j in range(0, K):
                for k in range(j, st):
                    s += X[i][k]
                s -= (yt[j] * st)
                print('s : ', s)
                m.addConstr(s >= 0, 'nb case bloc Y')
                #reset de s
                s = 0

    for j in range(0,K):
        cc = col[j]
        Zj = Z2[j]
        for t in range(0, len(cc)):
            s = 0
            st = cc[t]
            zt = Zj[t]
            print('st : ', st)
            print('col : ', col)
            for i in range(0, N):
                for k in range(i, st):
                    s += X[k][j]
                s -= (zt[i] * st)
                print('contrainte z : ', s)
                m.addConstr(s >= 0, 'nb case bloc Z')
                #reset s
                s = 0
                
    #contrainte start
    for i in range(0,N):
        lc = lines[i]
        Yi = Y2[i]
        for t in range(0, len(lc)):
            yt = Yi[t]
            st = lc[t]
            start = sum([lc[p] + 1 for p in range(0, t)])
            end = K - st - sum([lc[q] + 1 for q in range(t + 1, len(lc))])
            for j in range(0, start):
                m.addConstr(yt[j] < 1, 'Y cc start')
            for j in range(K, end,-1):
                m.addConstr(yt[j] < 1, 'Y cc stop')

    #contrainte start
    for j in range(0,K):
        cc = col[j]
        Zj = Z2[j]
        for t in range(0, len(lc)):
            st = cc[t]
            start = sum([cc[p] + 1 for p in range(0, t)])
            end = N - st - sum([lc[q] + 1 for q in range(t + 1, len(cc))])
            zt = Zj[t]
            for i in range(0, start):
                m.addConstr(zt[i] < 1, 'Z cc start')
            for i in range(K, end,-1):
                m.addConstr(zt[i] < 1, 'Z cc stop')
    

#    for i in range(0,N):
#        lc = lines[i]
#        for t in range(0, len(lc)):
#            phi = sum([lc[k] for k in range(0, t)])
            
    
    m.optimize()            
    print('X')
    for xi in X:
        print(xi)

    print('Y')
    print(Y2)

    print('Z')
    print(Z2)

    A = X_to_array(X,K)
    print('A : ', A)
    return A
    

def main():
    #lines, col, Mat = read_file('instances/11.txt')
    #================================
    #      TEST
    Mat = np.array([[-1,-1,-1],[-1,-1,-1]])
    lines = np.array([[2],[1]])
    col = np.array([[1],[1],[1]])
    N, K = Mat.shape
    #solve(Mat, lines, col)
    test_simple4()

main()
