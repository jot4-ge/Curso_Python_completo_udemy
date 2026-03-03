"""
Fatiamento de strings
 012345678
 Olá mundo
-987654321
Fatiamento [i:f:p] [::]
Obs.: a função len retorna a qtd
de caracteres da str
"""
variavel = 'Olá mundo'
print(variavel[4:8]) #indice final não é incluido, no ex coloquei 8 mas ele vai até o 7
print(variavel[-8:-2])
print(len(variavel))
print(variavel[::-1])