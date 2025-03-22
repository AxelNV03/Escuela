def neuronaNot(x):
    w=-1
    theta=-0.5
    #Funcion de activacion
    fx=x*w
    if fx>theta:
        return 1
    else:
        return 0
    
def neuronaAnd(x1,x2):
    w1=1
    w2=1
    theta=1.5
    #Funcion de activacion
    fx=x1*w1+x2*w2
    if fx>theta:
        return 1
    else:
        return 0
    
def neuronaOr(x1,x2):
    w1=1,w2=1
    theta=0.9
    #Funcion de activacion
    fx=x1*w1+x2*w2
    if fx>theta:
        return 1
    else:
        return 0



'''
x=int(input("Ingrese un valor para x:"))
salida=neuronaNot(x)

print("La salida de la neurona es:", salida)
'''

x1=int(input("Ingrese un valor para x1:"))
x2=int(input("Ingrese un valor para x2:"))
salida=neuronaAnd(x1,x2)

print("La salida de la neurona AND es:", salida)

salida=neuronaOr(x1,x2)
print("La salida de la neurona OR es:", salida)


