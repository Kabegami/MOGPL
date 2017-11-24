# coding: utf-8

#variable global

from projet import *
from wrapper import *

debug = False

@silent
def sp():
    """ print pour les Assert , attention cpt est une liste ! """
    global cpt
    print('====================================================')
    print('                      TEST {}                       '.format(cpt))
    print('====================================================')
    cpt += 1
    

@silent
def test_T():
    assert(T(10, 1, [5,2]) == True)
    assert(T(7, 1, [5,2]) == True)
    assert(T(6, 1, [5,2]) == False)
    assert(T(3, 0, [4]) == True)

@silent
def test_T2():
    global cpt
    e1 = np.array([1,1,1,-1,-1])
    e2 = np.array([1,-1,-1,-1,-1])
    e3 = np.array([1,-1,0,-1,-1])
    e4 = np.array([1,0,-1,-1,0,-1])
    e5 = np.array([1,0,0,0,0,1])
    e6 = np.array([1,1,1,-1,-1,0])
    cpt = 0
    sp()
    assert(T2(4, 0, [3], e1) == True)
    sp()
    assert(T2(4, 0, [3], e2) == True)
    sp()
    assert(T2(4,0,[3],e3) == False)
    sp()
    assert(T2(4,0,[3],e4) == False)
    sp()
    assert(T2(5,1,[1,1],e5) == True)
    sp()
    assert(T2(5,0,[1],e5) == False)
    sp()
    assert(T2(5,0,[3],e6) == True)

@silent
def test_possible_block():
    a1 = [-1,-1,-1,-1,-1]
    sl1 = 5
    a2 = [-1, -1, 0, -1, -1]
    
    assert(possible_block(4,sl1, a1) == True)
    assert(possible_block(3, sl1, a1) == False)
    assert(possible_block(0, sl1, a1) == False)

    assert(possible_block(4,sl1, a2) == False)
    assert(possible_block(3, sl1, a2) == False)
    assert(possible_block(0, sl1, a2) == False)

def main():
    print("=====================================================")
    print("          JEU DE TEST")
    print("=====================================================")
    test_possible_block()
    test_T()
    test_T2()
    print("jeu de test effectué avec succès !")
    print("=====================================================")

main()
