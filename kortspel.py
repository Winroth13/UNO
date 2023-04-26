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
    global largeNumberFont
    global smallNumberFont
    global colours
    global buttonWidth
    global buttonHeight
    global largeTextFont
    global buttonColumnX
    global buttonDrawY
    global buttonUnoY
    global smallTextFont
    global coloursOnHand
    global opponentHand

    backgroundColour = (200, 200, 200)
    windowWidth = 800
    windowHeight = 600
    windowName = 'UNO'
    playerHand = []
    opponentHand = []
    cardWidth = 100
    cardHeight = 150
    largeNumberFont = pygame.font.SysFont('monoscape', 100)
    smallNumberFont = pygame.font.SysFont('monoscape', 25)
    
    buttonWidth = 100
    buttonHeight = 50
    largeTextFont = pygame.font.SysFont('monoscape', 50)
    smallTextFont = pygame.font.SysFont('monoscape', 40)
    buttonColumnX = windowWidth*0.75
    buttonDrawY  = windowHeight/2 - 30
    buttonUnoY = windowHeight/2 + 30
    
    coloursOnHand = {'Red': 0, 'Green': 0, 'Blue': 0, 'Yellow': 0}
    
    colours = {'Red': (255, 0, 0), 'Green': (0, 255, 0), 'Blue': (0, 0, 255), 'Yellow': (255, 255, 0)}

def displayCard(centerX, centerY, number, colour, cornerNumber = True):
    card = pygame.draw.rect(screen, colour, [centerX - cardWidth/2, centerY - cardHeight/2, cardWidth, cardHeight])
    pygame.draw.rect(screen, (0, 0, 0), [card.left, card.top, cardWidth, cardHeight], width=2)
    
    largeNumber = largeNumberFont.render(str(number), 1, (0, 0, 0))
    screen.blit(largeNumber, (centerX - 18, centerY - 25))
    
    if cornerNumber == True:
        smallNumber = smallNumberFont.render(str(number), 1, (0, 0, 0))
        screen.blit(smallNumber, (card.left + 2, card.top + 2))

def displayHand():
    global cardDisplayWidth
    cardShift = 0
    
    pygame.draw.rect(screen, backgroundColour, [0, windowHeight - cardHeight, windowWidth, cardHeight])

    if cardWidth*len(playerHand) > windowWidth:
        cardShift = (cardWidth*len(playerHand) - windowWidth)/len(playerHand)
    
    cardDisplayWidth = cardWidth - cardShift
    
    for i in range(len(playerHand)):
        displayCard(windowWidth/2 - 50*(len(playerHand) - 1) + cardShift/2*len(playerHand) + (100 - cardShift)*i, windowHeight - cardHeight/2,
                    str(playerHand[i][0]), colours[playerHand[i][1]])

def randomCard():
    number = random.randint(0, 9)
    colourNumber = random.randint(0, len(colours) - 1)
    colour = list(colours)[colourNumber]
    
    return(number, colour)

def displayMiddleCard(card):
    global middleCard
    
    displayCard(windowWidth/2, windowHeight/2, card[0], card[1])
    pygame.display.update()
    middleCard = card

def drawCard(hand):
    card = randomCard()
    
    cardsInFront = 0
    
    colourIndex = list(coloursOnHand).index(card[1])
    
    for i in range(colourIndex):
        cardsInFront += coloursOnHand[list(coloursOnHand)[i]]
    
    comparisonCards = coloursOnHand[card[1]]
    
    coloursOnHand[card[1]] += 1
    
    while True:
        if comparisonCards == 0:
            hand.insert(int(cardsInFront), card)
            return
        elif comparisonCards % 2 == 0:
            comparisonCardIndex = int(cardsInFront + comparisonCards/2)
            comparisonValue = (hand[comparisonCardIndex][0] + hand[comparisonCardIndex - 1][0])/2
        else:
            comparisonCardIndex = int(cardsInFront + math.floor(comparisonCards/2))
            comparisonValue = hand[comparisonCardIndex][0]
            comparisonCards -= 1
            if comparisonValue < card[0]:
                cardsInFront += 1
        
        if comparisonValue == card[0]:
            hand.insert(comparisonCardIndex, card)
            return
        elif comparisonValue > card[0]:
            comparisonCards = comparisonCards/2
        else:
            comparisonCards = comparisonCards/2
            cardsInFront += comparisonCards

def drawButton(text, centerY, colour = (255, 255, 255)):
    button = pygame.draw.rect(screen, colour, [ buttonColumnX - buttonWidth/2, 
                                               centerY - buttonHeight/2, buttonWidth, buttonHeight])
    pygame.draw.rect(screen, (0, 0, 0), [button.left, button.top, buttonWidth, buttonHeight], width=2)
    
    textString = largeTextFont.render(str(text), 1, (0, 0, 0))
    screen.blit(textString, (buttonColumnX - 40, centerY - 15))

def unoButton(pressed):
    global unoButtonPressed
    
    if len(playerHand) == 1:
        if pressed == True:
            drawButton('UNO', buttonUnoY, colours['Green'])
            unoButtonPressed = True
        else:
            drawButton('UNO', buttonUnoY, colours['Red'])
            unoButtonPressed = False
    else:
        drawButton('UNO', buttonUnoY)

def displayOpponentHand():
    displayCard(windowWidth/2, cardHeight/2, len(opponentHand), (255, 255, 255), False)
    
    # if len(opponentHand) > 1:
    #     displayCard(windowWidth/2, cardHeight/2, len(opponentHand), (255, 255, 255), False)
    # else:
    #     pass

def start():
    pygame.font.init()
    variables()
    global screen

    screen = pygame.display.set_mode((windowWidth, windowHeight))
    pygame.display.set_caption(windowName)
    screen.fill(backgroundColour)

    pygame.display.flip()

    running = True
    
    for i in range(1):
        drawCard(playerHand)
        opponentHand.append(randomCard())

    displayHand()
    
    displayMiddleCard(randomCard())
    
    drawButton('Draw', buttonDrawY)
    
    drawButton('UNO', buttonUnoY)

    displayOpponentHand()
    
    pygame.display.update()
    
    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
            
            if pygame.mouse.get_pressed() == (1,0,0):
                if pygame.mouse.get_pos()[1] >= windowHeight - cardHeight and pygame.mouse.get_pos()[0] >= (windowWidth - cardWidth*len(playerHand))/2 and pygame.mouse.get_pos()[0] <= (windowWidth + cardWidth*len(playerHand))/2:
                    if len(playerHand)*cardWidth > windowWidth:
                        index = math.floor(pygame.mouse.get_pos()[0]/cardDisplayWidth)
                    else:
                        index = math.floor((pygame.mouse.get_pos()[0] - 
                                            (windowWidth - cardWidth*len(playerHand))/2)/cardWidth)
                    
                    if middleCard[0] == playerHand[index][0] or middleCard[1] == playerHand[index][1]:    
                        displayMiddleCard(playerHand[index])
                        coloursOnHand[playerHand[index][1]] -= 1
                        playerHand.pop(index)
                        
                        if len(playerHand) == 0 and unoButtonPressed == False:
                            for i in range(3):
                                drawCard(playerHand)
                        else:
                            win = True
                        
                        displayHand()
                    else:
                        print('Nej')
                    
                    unoButton(False)

                if pygame.mouse.get_pos()[0] >= buttonColumnX - buttonWidth/2 and pygame.mouse.get_pos()[0] <= buttonColumnX + buttonWidth/2:
                    if pygame.mouse.get_pos()[1] >= buttonDrawY - buttonHeight/2 and pygame.mouse.get_pos()[1] <= buttonDrawY + buttonHeight/2:
                        drawCard(playerHand)
                        displayHand()
                        pygame.display.update()
                    elif pygame.mouse.get_pos()[1] >= buttonUnoY - buttonHeight/2 and pygame.mouse.get_pos()[1] <= buttonUnoY + buttonHeight/2:
                        unoButton(True)
                
                pygame.display.update()

start()