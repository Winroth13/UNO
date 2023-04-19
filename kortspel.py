import pygame
import random

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
                    str(playerHand[i][0]), colours[playerHand[i][1]], )

def randomCard():
    number = random.randint(0, 9)
    colourNumber = random.randint(0, len(colours) - 1)
    colour = list(colours)[colourNumber]
    
    return(number, colour)

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
    
    middleCard = randomCard()
    displayCard(windowWidth/2, windowHeight/2, middleCard[0], middleCard[1])
    
    pygame.display.update()
    
    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

start()