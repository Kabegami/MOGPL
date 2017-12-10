# coding: utf-8

debug = False

import sys
import os
import time

def silent(function):
    """ fonction wraper qui empeche les functions avec @silent de print si la variable global debug est à False, si debug est à True les fonctions s'affichent normalement """
    def stop_print(*args):
        """ prevent a function to print """
        global debug
        if debug == True:
            #print('appel avec debuf == True')
            if not args:
                res = function()
            else:
                res = function(*args)
            return res
        else:
            #print('appel avec debug == False')
            old = sys.stdout
            sys.stdout = open(os.devnull, "w")
            if not args:
                res = function()
            else:
                res = function(*args)
            sys.stdout = old
            return res
    return stop_print

def timer(f):
    def helper(*args):
        t1 = time.time()
        res = f(*args)
        t2 = time.time()
        I =  t2 - t1
        print("temps d'execution de la fonction : {} secondes".format(I))
        return res
    return helper


def memo(f):
    memo.dico = dict()
    def helper(j,l,S,line):
        key = (j,l) + tuple(S) + tuple(line)
        if key not in memo.dico:
            memo.dico[key] = f(j,l,S,line)
        return memo.dico[key]
    return helper

def memo_id(f):
    memo_id.dico = dict()
    def helper(j, l, S, line):
        idS = id(S)
        key = (j,l) + S + line
        if key not in memo_id.dico:
            memo_id.dico[key] = f(j,l,S,line)
        return memo_id.dico[key]
    return helper

def memo_str(f):
    memo_str.dico = dict()
    def helper(j,l,S,line):
        key = str(j) + str(l) + str(S) + str(line)
        if key not in memo_str.dico:
            memo_str.dico[key] = f(j,l,S,line)
        return memo_str.dico[key]
    return helper


class Memo():
    def __init__(self, fn):
        self.fn = fn
        self.memo = dict()
    def __call__(self, j,l,S,line):
        key = (j,l, id(S)) + tuple(line)
        t2 = time.time()
        self.keyTime +=  t2 - t1
        print('key : ', key)
        if key not in self.memo:
            self.memo[key] = self.fn(j,l,S,line)
        else:
            print('appel de memoization numero : ', self.cpt)
            self.cpt += 1
        return self.memo[key]

    def time(self):
        return self.keyTime
        

def set_debug(b):
    global debug
    debug = b
