import pygame
import random
import math

def variables():
    global backgroundColour
    global windowWidth
    global windowHeight
    global windowName
    global playerHand
    global cardWidth
    global cardHeight
    global textFont
    global smallTextFont
    global colours

    backgroundColour = (200, 200, 200)
    windowWidth = 800
    windowHeight = 600
    windowName = 'UNO'
    playerHand = [(0, 'Green'), (2, 'Yellow'), (9, 'Blue'), (8, 'Red')]
    cardWidth = 100
    cardHeight = 150
    textFont = pygame.font.SysFont('monoscape', 100)
    smallTextFont = pygame.font.SysFont('monoscape', 25)
    
    colours = {'Red': (255, 0, 0), 'Green': (0, 255, 0), 'Blue': (0, 0, 255), 'Yellow': (255, 255, 0)}

def displayCard(centerX, centerY, number, colour):
    card = pygame.draw.rect(screen, colour, [centerX - cardWidth/2, centerY - cardHeight/2, cardWidth, cardHeight], width=0)
    pygame.draw.rect(screen, (0, 0, 0), [card.left, card.top, cardWidth, cardHeight], width=2)
    
    largeNumber = textFont.render(str(number), 1, (0, 0, 0))
    screen.blit(largeNumber, (card.centerx - 18, card.centery - 25))
    
    smallNumber = smallTextFont.render(str(number), 1, (0, 0, 0))
    screen.blit(smallNumber, (card.left + 2, card.top + 2))

def displayHand():
    for i in range(len(playerHand)):
        displayCard(windowWidth/2 - 50*(len(playerHand) - 1) + 100*i, windowHeight - cardHeight/2,
                    str(playerHand[i][0]), colours[playerHand[i][1]])

def randomCard():
    number = random.randint(0, 9)
    colourNumber = random.randint(0, len(colours) - 1)
    colour = list(colours)[colourNumber]
    
    return(number, colour)

def middleCard(card):
    displayCard(windowWidth/2, windowHeight/2, card[0], card[1])
    pygame.display.update()

def start():
    pygame.font.init()
    variables()
    global screen

    screen = pygame.display.set_mode((windowWidth, windowHeight))
    pygame.display.set_caption(windowName)
    screen.fill(backgroundColour)

    pygame.display.flip()

    running = True
    
    displayHand()
    
    middleCard1 = randomCard()
    displayCard(windowWidth/2, windowHeight/2, middleCard1[0], middleCard1[1])
    
    pygame.display.update()
    
    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
            
            if pygame.mouse.get_pressed() == (1,0,0):
                if pygame.mouse.get_pos()[1] >= windowHeight - cardHeight and pygame.mouse.get_pos()[0] >= (windowWidth - cardWidth*len(playerHand))/2 and pygame.mouse.get_pos()[0] <= (windowWidth + cardWidth*len(playerHand))/2:
                    index = math.floor((pygame.mouse.get_pos()[0] - (windowWidth - cardWidth*len(playerHand))/2)/100)
                    middleCard1 = playerHand[index]
                    displayCard(windowWidth/2, windowHeight/2, middleCard1[0], middleCard1[1])
                    playerHand.pop(index)
                    displayHand()
                    pygame.display.update()

start()