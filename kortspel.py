import pygame
import random
import math
import time

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
    global largeButtonWidth
    global buttonHeight
    global largeTextFont
    global buttonColumnX
    global buttonLeaderboardY
    global buttonRulesY
    global buttonDrawY
    global buttonUnoY
    global smallTextFont
    global coloursOnHand
    global opponentHand
    global opponentColourPreferences
    global opponentNumberPreferences
    global turnDisplayWidth
    global turnDisplayHeight
    global turnDisplayX
    global turnDisplayY

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
    largeButtonWidth = buttonWidth*2.5
    buttonHeight = 50
    largeTextFont = pygame.font.SysFont('monoscape', 50)
    smallTextFont = pygame.font.SysFont('monoscape', 40)
    buttonColumnX = windowWidth*0.75
    buttonLeaderboardY = windowHeight/2 - 90
    buttonRulesY = windowHeight/2 - 30
    buttonDrawY  = windowHeight/2 + 30
    buttonUnoY = windowHeight/2 + 90

    turnDisplayWidth = 300
    turnDisplayHeight = 50
    turnDisplayX = windowWidth/5
    turnDisplayY = windowHeight/2
    
    coloursOnHand = {'Red': 0, 'Green': 0, 'Blue': 0, 'Yellow': 0}
    
    colours = {'Red': (255, 0, 0), 'Green': (0, 255, 0), 'Blue': (0, 0, 255), 'Yellow': (255, 255, 0)}
    
    opponentColourPreferences = {'Red': 0, 'Green': 0, 'Blue': 0, 'Yellow': 0}
    opponentNumberPreferences = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}

def drawFrame(centerX, centerY, width, height, colour = (255, 255, 255)):
    frame = pygame.draw.rect(screen, colour, [centerX - width/2, centerY - height/2, width, height])
    pygame.draw.rect(screen, (0, 0, 0), [frame.left, frame.top, width, height], width=2)

def writeText(text, leftX, topY):
    textString = largeTextFont.render(str(text), 1, (0, 0, 0))
    screen.blit(textString, (leftX, topY))

def displayCard(centerX, centerY, number, colour, cornerNumber = True):
    drawFrame(centerX, centerY, cardWidth, cardHeight, colour)
    
    largeNumber = largeNumberFont.render(str(number), 1, (0, 0, 0))
    screen.blit(largeNumber, (centerX - 18, centerY - 25))
    
    if cornerNumber == True:
        smallNumber = smallNumberFont.render(str(number), 1, (0, 0, 0))
        screen.blit(smallNumber, (centerX - cardWidth/2 + 2, centerY - cardHeight/2 + 2))

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

def playerDrawCard():
    card = randomCard()
    
    cardsInFront = 0
    
    colourIndex = list(coloursOnHand).index(card[1])
    
    for i in range(colourIndex):
        cardsInFront += coloursOnHand[list(coloursOnHand)[i]]
    
    comparisonCards = coloursOnHand[card[1]]
    
    coloursOnHand[card[1]] += 1
    
    while True:
        if comparisonCards == 0:
            playerHand.insert(int(cardsInFront), card)
            return
        elif comparisonCards % 2 == 0:
            comparisonCardIndex = int(cardsInFront + comparisonCards/2)
            comparisonValue = (playerHand[comparisonCardIndex][0] + playerHand[comparisonCardIndex - 1][0])/2
        else:
            comparisonCardIndex = int(cardsInFront + math.floor(comparisonCards/2))
            comparisonValue = playerHand[comparisonCardIndex][0]
            comparisonCards -= 1
            if comparisonValue < card[0]:
                cardsInFront += 1
        
        if comparisonValue == card[0]:
            playerHand.insert(comparisonCardIndex, card)
            return
        elif comparisonValue > card[0]:
            comparisonCards = comparisonCards/2
        else:
            comparisonCards = comparisonCards/2
            cardsInFront += comparisonCards

def opponentDrawCard():
    card = randomCard()
    opponentHand.append(card)
    
    opponentColourPreferences[card[1]] += 1
    opponentNumberPreferences[card[0]] += 1

def drawSmallButton(text, centerY, colour = (255, 255, 255)):
    drawFrame(buttonColumnX, centerY, buttonWidth, buttonHeight, colour)

    writeText(text, buttonColumnX - 20 - 5.5*len(text), centerY - 15)

def drawLargeButton(text, centerY, colour = (255, 255, 255)):
    drawFrame(buttonColumnX, centerY, largeButtonWidth, buttonHeight, colour)

    writeText(text, buttonColumnX - 110, centerY - 15)

def unoButton(pressed):
    global unoButtonPressed
    
    if len(playerHand) == 1:
        if pressed == True:
            drawSmallButton('UNO', buttonUnoY, colours['Green'])
            unoButtonPressed = True
        else:
            drawSmallButton('UNO', buttonUnoY, colours['Red'])
            unoButtonPressed = False
    else:
        drawSmallButton('UNO', buttonUnoY, (125, 125, 125))

def displayOpponentHand():
    drawFrame(windowWidth/2, cardHeight/2, cardWidth, cardHeight)

    number = largeNumberFont.render(str(len(opponentHand)), 1, (0, 0, 0))

    if len(opponentHand) == 0:
        loss = True
    elif len(opponentHand) > 9:
        screen.blit(number, (windowWidth/2 - 38, cardHeight/2 - 25))
    else:
        if len(opponentHand) == 1:
            writeText('UNO!', windowWidth/2 - 44, cardHeight/2 - 10)
        
        else:
            screen.blit(number, (windowWidth/2 - 18, cardHeight/2 - 25))

def opponentTurn():
    isPlayerTurn(False)
    pygame.display.update()
    time.sleep(1)

    #print(opponentColourPreferences)
    #print(opponentNumberPreferences)
    #print('Opponent Turn')
    
    bestPlayIndex = None
    bestPlayValue = 0
    currentIndex = -1
    
    #print(middleCard)
    #print(opponentHand)
    for comparisonCard in opponentHand:
        #print(comparisonCard)
        currentIndex += 1
        if comparisonCard[0] == middleCard[0] or comparisonCard[1] == middleCard[1]:
            comparisonCardValue = opponentNumberPreferences[comparisonCard[0]] + opponentColourPreferences[comparisonCard[1]]
            
            #print('Jämförelse:')
            #print(comparisonCardValue)
            #print(bestPlayValue)
            if bestPlayIndex == None or comparisonCardValue > bestPlayValue:
                bestPlayIndex = currentIndex
                
                bestPlayValue = comparisonCardValue
                
                #print('Best card:')
                #print(comparisonCard)
    if bestPlayIndex != None:
        displayMiddleCard(opponentHand[bestPlayIndex])
        
        opponentNumberPreferences[opponentHand[bestPlayIndex][0]] -= 1
        opponentColourPreferences[opponentHand[bestPlayIndex][1]] -= 1
        
        opponentHand.pop(bestPlayIndex)
        
        #print(opponentColourPreferences)
        #print(opponentNumberPreferences)
        #print(opponentHand)
    else:
        #print('Draw')
        opponentDrawCard()
    
    displayOpponentHand()

    isPlayerTurn(True)

def isPlayerTurn(playerTurn):
    if playerTurn == True:
        drawFrame(turnDisplayX, turnDisplayY, turnDisplayWidth, turnDisplayHeight, colours['Green'])
        writeText('Your turn', turnDisplayX - 80, turnDisplayY - 15)
    else:
        drawFrame(turnDisplayX, turnDisplayY, turnDisplayWidth, turnDisplayHeight, colours['Red'])
        writeText("Opponent's turn", turnDisplayX - 135, turnDisplayY - 15)

def playArea():
    global opponentColourPreferences
    global opponentNumberPreferences
    global running

    screen.fill(backgroundColour)

    displayMiddleCard(middleCard)

    displayHand()

    drawLargeButton('Leaderboard', buttonLeaderboardY)
    drawSmallButton('Rules', buttonRulesY)
    drawSmallButton('Draw', buttonDrawY)
    unoButton(False)

    displayOpponentHand()

    isPlayerTurn(True)
    
    pygame.display.update()
    
    #opponentTurn()
    
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
                        
                        #Makes the opponent less likely to play cards that have a higher cahnce of being good for the player
                        opponentColourPreferences[playerHand[index][1]] -= 0.5
                        opponentNumberPreferences[playerHand[index][0]] -= 0.5
                        
                        playerHand.pop(index)
                        
                        if len(playerHand) == 0 and unoButtonPressed == False:
                            for i in range(3):
                                playerDrawCard()
                                
                                #Reset all preference scores, since the player gets a fresh hand
                                opponentColourPreferences = {'Red': 0, 'Green': 0, 'Blue': 0, 'Yellow': 0}
                                opponentNumberPreferences = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
                                
                                #They still need to account for their own cards on hand
                                for opponentCard in opponentHand:
                                    opponentColourPreferences[opponentCard[1]] += 1
                                    opponentNumberPreferences[opponentCard[0]] += 1
                        else:
                            win = True
                        
                        displayHand()
                        
                        opponentTurn()
                    else:
                        print('Nej')
                    
                    unoButton(False)

                if pygame.mouse.get_pos()[0] >= buttonColumnX - buttonWidth/2 and pygame.mouse.get_pos()[0] <= buttonColumnX + buttonWidth/2:
                    if pygame.mouse.get_pos()[1] >= buttonDrawY - buttonHeight/2 and pygame.mouse.get_pos()[1] <= buttonDrawY + buttonHeight/2:
                        playerDrawCard()
                        displayHand()
                        
                        #More likely to play cards the player cannot play on
                        opponentColourPreferences[middleCard[1]] += 1
                        opponentNumberPreferences[middleCard[0]] += 1
                        
                        opponentTurn()
                    elif pygame.mouse.get_pos()[1] >= buttonUnoY - buttonHeight/2 and pygame.mouse.get_pos()[1] <= buttonUnoY + buttonHeight/2:
                        unoButton(True)
                    
                    elif pygame.mouse.get_pos()[1] >= buttonRulesY - buttonHeight/2 and pygame.mouse.get_pos()[1] <= buttonRulesY + buttonHeight/2:
                        #displayRules()
                        print('Rules')
                
                if pygame.mouse.get_pos()[0] >= buttonColumnX - largeButtonWidth/2 and pygame.mouse.get_pos()[0] <= buttonColumnX + largeButtonWidth/2 and pygame.mouse.get_pos()[1] >= buttonLeaderboardY - buttonHeight/2 and pygame.mouse.get_pos()[1] <= buttonLeaderboardY + buttonHeight/2:
                    #displayLeaderboard()
                    print('Leaderboard')

                pygame.display.update()

def newGame():
    variables()
    global middleCard

    for i in range(3):
        playerDrawCard()
        opponentDrawCard()

    middleCard = randomCard()

    playArea()

def start():
    pygame.font.init()
    variables()
    global screen
    global running

    screen = pygame.display.set_mode((windowWidth, windowHeight))
    pygame.display.set_caption(windowName)
    screen.fill(backgroundColour)

    pygame.display.flip()

    running = True
    
    newGame()

start()