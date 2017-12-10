from projet import *
from good_plne import *

def main(methode='dynamique', filename='instances/8.txt'):
    if methode == 'plne':
        timeout = True
        S,N, M = lireFichier(filename)
        L = solve(S,N,M,timeout)
        draw(L)
        return L
    if methode == 'dynamique':
        lines, col, M = read_file(filename)
        A,t  = timeIt(coloration,M, col, lines)
        draw(A)
        print('t : ', t)
        return A
    if methode =='mix':
        timeout = True
        partialDir = 'dynamiqueData/'
        partialF = partialDir + 'instace' + str(i)
        S,N, M = lireFichier(filename)
        A = load(partialF)
        L = partial_solve(S,N,M,A,timeout)
        #draw(L)
        return L

A = main()
print('A')
        
        

