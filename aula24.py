# Operadores in e not in
# Strings sãp iteráveis
#  0 1 2 3
#  J o ã o
# -6-5-4-3

#nome = 'João'
#print(nome[2])
#print(nome[-4])
#print('ão' in nome)
#print('os' in nome)
#print(10 * '-')
#print('ão' not in nome)
#print('os' not in nome)

nome = input('Digite seu nome: ')
encontrar = input('Digite o que deseja encontrar: ')

if encontrar in nome:
    print(f'{encontrar} está em {nome}')
else: 
    print(f'{encontrar} não está em {nome}')
 