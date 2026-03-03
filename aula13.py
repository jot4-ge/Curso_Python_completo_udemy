nome = 'Jota'
altura = 1.70
peso = 78
imc = peso / (altura * altura) #IMC = peso / (altura x altura)

"f-strings"
linha_1 = f'{nome} tem {altura:.2f} de altura,'#formatação que usa duas casas decimais 
linha_2 = f'pesa {peso} quilos e seu imc é'
linha_3 = f'{imc:.2f}'#formatação que usa duas casas decimais 

#É possível fazer dentro do print tbm, as de baixo são um exemplo de uso:
print(linha_1)
print(linha_2)
print(linha_3)