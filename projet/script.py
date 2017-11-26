import re
import os

def del_print(filename):
    f = open(filename, 'r')
    s = ""
    for line in f:
        b = re.match('.*(print){1,}.*', line)
        if b is None:
            s += line
        #prinet('line : ', line)
    f.close()
    return s

def save(s, filename):
    b = False
    if os.path.exists(filename):
        while not(b):
            print("le fichier existe deja être vous sur de vouloir écraser l'ancienne version ?")
            answer = (str)(input())
            if answer.lower() in ['y','yes','o','oui']:
                b= True
            elif answer.lower() in ['n','non','no']:
                return None
            else:
                print(" le format n'est pas valide tapez y ou n ")
    f = open(filename, 'a')
    f.write(s)
    f.close()
            

s = del_print('projet.py')
print(s)
save(s, 'projetv2.py')
