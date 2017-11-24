import re

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
    f = open(filename, 'a')
    f.write(s)
    f.close()

s = del_print('projet.py')
print(s)
save(s, 'no_print_projet.py')
