# UNIVERSIDADE FEDERAL DO RIO GRANDE DO NORTE
# DEPARTAMENTO DE ENGENHARIA DE COMPUTACAO E AUTOMACAO
# DISCIPLINA REDES DE COMPUTADORES (DCA0113)
# AUTOR: PROF. CARLOS M D VIEGAS (viegas 'at' dca.ufrn.br)
#
# SCRIPT: Cliente de sockets TCP modificado para enviar texto minusculo ao servidor e aguardar resposta em maiuscula (python 3)
#

# importacao das bibliotecas
from socket import *

# definicao das variaveis
serverName = 'localhost' # ip do servidor
serverPort = 61000 # porta a se conectar

while 1:
    clientSocket = socket(AF_INET,SOCK_STREAM) # criacao do socket TCP


    clientSocket.connect((serverName, serverPort)) # conecta o socket ao servidor
    print ('Entradas aceitas:')
    print('Trem verde: 0 1; 0 2; 0 3')
    print('Trem vermelho: 1 1; 1 2; 1 3')
    print('Trem branco: 2 1; 2 2; 2 3')
    print('Trem azul: 3 1; 3 2; 3 3')
    sentence = input('Digite o primeiro argumento referente Thread e o segundo a velocidade, ex: 1 2: ')
    clientSocket.send(sentence.encode('utf-8')) # envia o texto para o servidor
    modifiedSentence = clientSocket.recv(1024) # recebe do servidor a resposta
    print ('O servidor (\'%s\', %d) respondeu com: %s' % (serverName, serverPort, modifiedSentence.decode('utf-8')))

