nbvar=2
nbcont=3

lignes = range(nbcont)
colonnes = range(nbvar)

a = [[1,2,3],
     [3,1,1]]

b = [8,5]
c = [8,5]

m = Model("mogplex") 

# declaration variables de decision
x = []
for i in colonnes:
    x.append(m.addVar(vtype=GRB.CONTINUOUS, lb=0, name="x%d" % (i+1)))

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


print ""                
print 'Solution optimale:'
for j in colonnes:
    print 'x%d'%(j+1), '=', x[j].x
print ""
print 'Valeur de la fonction objectif :', m.objVal
