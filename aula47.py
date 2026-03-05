"""
Faça um jogo para o usuário adivinhar qual
a palavra secreta.
- Você vai propor uma palavra secreta
qualquer e vai dar a possibilidade para
o usuário digitar apenas uma letra.
- Quando o usuário digitar uma letra, você 
vai conferir se a letra digitada está
na palavra secreta.
    - Se a letra digitada estiver na
    palavra secreta; exiba a letra;
    - Se a letra digitada não estiver
    na palavra secreta; exiba *.
Faça a contagem de tentativas do seu
usuário.
"""

palavra_secreta = 'dormir'
letras_acertadas = ' ' 
tentativas = 0

while True:
    letra_digitada = input("Digite a letra: ")
    tentativas += 1

    if letra_digitada in palavra_secreta:
        letras_acertadas += letra_digitada
        
    palavra_formada = ''

    for letra_secreta in palavra_secreta:
        if letra_secreta in letras_acertadas:
            palavra_formada += letra_secreta

        else: 
            palavra_formada += '*'

    print(f'Palavra formada: {palavra_formada}')

    if palavra_formada == palavra_secreta:
        print(f'Parabéns, você ganhou! A palavra era {palavra_secreta}.')
        print(f'Número de tentativas: {tentativas}')
        break
    else: 
        print('A palavra formada ainda não é a palavra secreta, tente novamente.')
        
