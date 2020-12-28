import _thread as thread
import time
import pygame
from pygame.locals import *
from socket import *

s = thread.allocate_lock()


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (133, 133, 224)

threadVelo = [0, 0]
global b
b =  [0, 0]

global SPEED
global velocidade

SPEED = [0.1, 0.1, 0.1, 0.1]
velocidade = [1, 1,1,1]

pygame.init()
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption('Trabalho 3 - Sistema de Trens')

skins = [0, 0, 0, 0]

skins[0] = pygame.Surface((10, 10))
skins[0].fill(GREEN)

skins[1] = pygame.Surface((10, 10))
skins[1].fill(BLUE)

skins[2] = pygame.Surface((10, 10))
skins[2].fill(RED)

skins[3] = pygame.Surface((10, 10))
skins[3].fill(WHITE)

serverName = ''
serverPort = 61000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind((serverName,serverPort))
serverSocket.listen(1)
print ('Servidor TCP esperando conexoes na porta %d ...' % (serverPort))



threads_wagons = [0, 0, 0, 0]
trains_wagons = [0, 0, 0, 0]
train_wagon_positions = [[
    (90, 190),  # L1
    (140, 140),  # L2
    (190, 190),  # L3
    (140, 240)  # L4
],
    [
        (240, 340),  # L13
        (90, 290),  # L11
        (140, 240),  # L4
        (240, 240),  # L6
        (340, 240),  # L10
        (390, 290)  # L12
    ],
    [
        (240, 140),  # L7
        (290, 190),  # L5
        (240, 240),  # L6
        (190, 190)  # L3
    ],
    [
        (340, 140),  # L8
        (390, 190),  # L9
        (340, 240),  # L10
        (290, 190)  # L5
    ]
]

next_wagons = [1, 1, 1, 1]

font = pygame.font.Font('freesansbold.ttf', 18)


def changeWagonInThread(next_wagon, thread_num):
    global threads_wagons
    global train_wagon_positions
    global trains_wagons
    global next_wagons



    if train_wagon_positions[thread_num][next_wagon] not in trains_wagons:
        wagons_copy = threads_wagons.copy()
        prev_wagon = wagons_copy[thread_num]
        wagons_copy[thread_num] = next_wagon

        trems1 = [wagons_copy[0], wagons_copy[1], wagons_copy[2]]
        trems2 = [wagons_copy[1], wagons_copy[2], wagons_copy[3]]
        if (trems1 == [2, 2, 2] or trems2 == [3, 1, 2] or trems1 + [wagons_copy[3]] == [2, 2, 1, 2]):
            threads_wagons[thread_num] = prev_wagon
        else:
            threads_wagons[thread_num] = next_wagon
            counter = next_wagons[thread_num] + 1
            next_wagons[thread_num] = counter % 4 if thread_num != 1 else counter % 6


def thread_green_train():
    while True:
        thread_num = 0
        print('Sou o trem verde e estou com a velocidade: %s' % (velocidade[0]))
        changeWagonInThread(next_wagons[thread_num], thread_num)
        time.sleep(SPEED[0])
        changeWagonInThread(next_wagons[thread_num], thread_num)
        time.sleep(SPEED[0])
        s.acquire()
        changeWagonInThread(next_wagons[thread_num], thread_num)
        time.sleep(SPEED[0])
        s.release()
        s.acquire()
        changeWagonInThread(next_wagons[thread_num], thread_num)
        time.sleep(SPEED[0])
        s.release()


def thread_blue_train():
    while True:
        print('Sou o trem blue e estou com a velocidade: %s' % (velocidade[3]))
        thread_num = 1
        changeWagonInThread(next_wagons[thread_num], thread_num)
        time.sleep(SPEED[3])
        changeWagonInThread(next_wagons[thread_num], thread_num)
        time.sleep(SPEED[3])
        s.acquire()
        changeWagonInThread(next_wagons[thread_num], thread_num)
        time.sleep(SPEED[3])
        s.release()
        s.acquire()
        changeWagonInThread(next_wagons[thread_num], thread_num)
        time.sleep(SPEED[3])
        s.release()
        s.acquire()
        changeWagonInThread(next_wagons[thread_num], thread_num)
        time.sleep(SPEED[3])
        s.release()
        changeWagonInThread(next_wagons[thread_num], thread_num)
        time.sleep(SPEED[3])


def thread_purple_train():
    while True:
        print('Sou o trem vermelho e estou com a velocidade: %s' % (velocidade[1]))
        thread_num = 2
        changeWagonInThread(next_wagons[thread_num], thread_num)
        time.sleep(SPEED[1])
        s.acquire()
        changeWagonInThread(next_wagons[thread_num], thread_num)
        time.sleep(SPEED[1])
        s.release()
        s.acquire()
        changeWagonInThread(next_wagons[thread_num], thread_num)
        time.sleep(SPEED[1])
        s.release()
        s.acquire()
        changeWagonInThread(next_wagons[thread_num], thread_num)
        time.sleep(SPEED[1])
        s.release()


def thread_red_train():
    while True:
        thread_num = 3
        print('Sou o trem white e estou com a velocidade: %s' % (velocidade[2]))
        changeWagonInThread(next_wagons[thread_num], thread_num)
        time.sleep(SPEED[2])
        changeWagonInThread(next_wagons[thread_num], thread_num)
        time.sleep(SPEED[2])
        s.acquire()
        changeWagonInThread(next_wagons[thread_num], thread_num)
        time.sleep(SPEED[2])
        s.release()
        s.acquire()
        changeWagonInThread(next_wagons[thread_num], thread_num)
        time.sleep(SPEED[2])
        s.release()

def thread_comunicacao():
    while True:
        connectionSocket, addr = serverSocket.accept()
        sentence = connectionSocket.recv(1024)
        sentence = sentence.decode('utf-8')
        capitalizedSentence = sentence.upper()
        threadVelo = capitalizedSentence
        global b
        global SPEED
        global velocidade
        b[0] = str(capitalizedSentence).split(' ')[0][0]
        b[1] = str(capitalizedSentence).split(' ')[1][0]
        if (b[0] == '0' and b[1] == '1' ):
            SPEED[0] = 0.1
            velocidade[0] = 1
        if (b[0] == '0' and b[1] == '2' ):
            SPEED[0] = 0.5
            velocidade[0] = 2
        if (b[0] == '0' and b[1] == '3' ):
            SPEED[0] = 1
            velocidade[0] = 3
        if (b[0] == '1' and b[1] == '1' ):
            SPEED[1] = 0.1
            velocidade[1] = 1
        if (b[0] == '1' and b[1] == '2' ):
            SPEED[1] = 0.5
            velocidade[1] = 2
        if (b[0] == '1' and b[1] == '3' ):
            SPEED[1] = 1
            velocidade[1] = 3
        if (b[0] == '2' and b[1] == '1' ):
            SPEED[2] = 0.1
            velocidade[2] = 1
        if (b[0] == '2' and b[1] == '2' ):
            SPEED[2] = 0.5
            velocidade[2] = 2
        if (b[0] == '2' and b[1] == '3' ):
            SPEED[2] = 1
            velocidade[2] = 3
        if (b[0] == '3' and b[1] == '1' ):
            SPEED[3] = 0.1
            velocidade[3] = 1
        if (b[0] == '3' and b[1] == '2' ):
            SPEED[3] = 0.5
            velocidade[3] = 2
        if (b[0] == '3' and b[1] == '3' ):
            SPEED[3] = 1
            velocidade[3] = 3


        print('Cliente %s enviou: %s, transformando em: %s' % (addr, sentence, capitalizedSentence))
        connectionSocket.send(capitalizedSentence.encode('utf-8'))
        connectionSocket.close()

thread.start_new_thread(thread_green_train, ())
thread.start_new_thread(thread_blue_train, ())
thread.start_new_thread(thread_purple_train, ())
thread.start_new_thread(thread_red_train, ())
thread.start_new_thread(thread_comunicacao, ())

end = False

while not end:


    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    for i in range(4):
        trains_wagons[i] = train_wagon_positions[i][threads_wagons[i]]

    screen.fill((0, 0, 0))

    # desenha o grid e os caminhos dos trens
    for x in range(0, 600, 10):
        pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, 600))
    for y in range(0, 600, 10):
        pygame.draw.line(screen, (40, 40, 40), (0, y), (600, y))
        pygame.draw.line(screen, GREEN, [100, 250], [100, 150], 2)
        pygame.draw.line(screen, GREEN, [100, 150], [200, 150], 2)
        pygame.draw.line(screen, GREEN, [200, 150], [200, 250], 2)
        pygame.draw.line(screen, GREEN, [200, 250], [100, 250], 2)
        pygame.draw.line(screen, RED, [200, 150], [300, 150], 2)
        pygame.draw.line(screen, RED, [300, 150], [300, 250], 2)
        pygame.draw.line(screen, RED, [300, 250], [200, 250], 2)
        pygame.draw.line(screen, WHITE, [300, 150], [400, 150], 2)
        pygame.draw.line(screen, WHITE, [400, 150], [400, 250], 2)
        pygame.draw.line(screen, WHITE, [400, 250], [300, 250], 2)
        pygame.draw.line(screen, BLUE, [100, 250], [100, 350], 2)
        pygame.draw.line(screen, BLUE, [100, 350], [400, 350], 2)
        pygame.draw.line(screen, BLUE, [400, 250], [400, 350], 2)

    for i in range(4):
        screen.blit(skins[i], trains_wagons[i])

    pygame.display.update()

while True:
    end_font = pygame.font.Font('freesansbold.ttf', 75)
    pygame.display.update()
    pygame.time.wait(500)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
