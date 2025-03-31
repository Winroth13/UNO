import pygame
import random
import math
import time
import pickle

def variables():
    #All variables
    global backgroundColour
    global windowWidth
    global windowHeight
    global windowName
    global playerHand
    global cardWidth
    global cardHeight
    global largeNumberFont
    global smallNumberFont
    global cardColours
    global smallButtonWidth
    global largeButtonWidth
    global buttonHeight
    global largeTextFont
    global buttonColumnX
    global buttonLeaderboardY
    global buttonRulesY
    global buttonDrawY
    global buttonUnoY
    global buttonReturnY
    global smallTextFont
    global coloursOnHand
    global opponentHand
    global opponentColourPreferences
    global opponentNumberPreferences
    global turnDisplayWidth
    global turnDisplayHeight
    global turnDisplayX
    global turnDisplayY
    global turnCounter
    global playerRanking
    global playerScore

    #Main window
    backgroundColour = (200, 200, 200)
    windowWidth = 800
    windowHeight = 600
    windowName = 'UNO'
    
    #Display of cards
    cardWidth = 100
    cardHeight = 150
    
    #The hands of the players
    playerHand = []
    opponentHand = []
    
    #Number sizes and fonts
    largeNumberFont = pygame.font.SysFont('monoscape', 100)
    smallNumberFont = pygame.font.SysFont('monoscape', 25)
    
    #Text sizes and fonts 
    largeTextFont = pygame.font.SysFont('monoscape', 50)
    smallTextFont = pygame.font.SysFont('monoscape', 30)
    
    #Buttons
    smallButtonWidth = 125
    largeButtonWidth = smallButtonWidth*2
    buttonHeight = 50
    buttonColumnX = windowWidth*0.75
    buttonLeaderboardY = windowHeight/2 - 90
    buttonRulesY = windowHeight/2 - 30
    buttonDrawY  = windowHeight/2 + 30
    buttonUnoY = windowHeight/2 + 90
    buttonReturnY = windowHeight*0.75

    #The turn display
    turnDisplayWidth = 300
    turnDisplayHeight = 50
    turnDisplayX = windowWidth/5
    turnDisplayY = windowHeight/2
    
    #The colours on the player's hand
    coloursOnHand = {'Red': 0, 'Green': 0, 'Blue': 0, 'Yellow': 0}
    
    #The colours of the cards
    cardColours = {'Red': (255, 0, 0), 'Green': (0, 255, 0), 'Blue': (0, 0, 255), 'Yellow': (255, 255, 0)}
    
    #Varibales for what the opponenet pårefers to play
    opponentColourPreferences = {'Red': 0, 'Green': 0, 'Blue': 0, 'Yellow': 0}
    opponentNumberPreferences = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
    
    #The turn counter
    turnCounter = 0
    
    #The leaderboard information about the current game
    playerRanking = "-"
    playerScore = "--"

def objectInserter(object, list, comparisonObjects, isLeaderboard, objectsInFront = 0):
    #Inserts an opject into a list
    #Lower numbers are inserted earlier in the list
    while True:
        #If these are no objects to sompare it with
        if comparisonObjects == 0:
            #Inserts object into it's index based on number of objects determined to be in front of it
            list.insert(int(objectsInFront), object)
            
            #The objects index is returned in case it is to be used when displaying the leaderboard
            return(objectsInFront)
        
        #If the number of objects to compare with are even
        elif comparisonObjects % 2 == 0:
            #Compares with the two middle objects in the pool of objects it is coampared to
            comparisonObjectIndex = int(objectsInFront + comparisonObjects/2)
            comparisonValue = (list[comparisonObjectIndex][0] + list[comparisonObjectIndex - 1][0])/2
            
        #If the number of objects to compare with are uneven
        else:
            #Compares with the object in the middle of the pool of objects to be compared with
            comparisonObjectIndex = int(objectsInFront + math.floor(comparisonObjects/2))
            comparisonValue = list[comparisonObjectIndex][0]
            
            #The object is removed from the comparison pool
            comparisonObjects -= 1
            
            #If the object is added to to number of cards in front if it's value is less than
            # the cvalue of the object to be inserted
            #This is done on top of what the following if-statement will do
            if comparisonValue < object[0]:
                objectsInFront += 1
        
        #Comparing the new object to the previously established values to compare to
        
        #If the Object has the same value as the comaprison value
        if comparisonValue == object[0]:
            #Needs to put the object behind all objects of the same value if it is the leaderboard
            if isLeaderboard == True:
                #Moves the object one step back if the objectr behind it has the same value
                #This step is done one object at a time since it is faster due to the fact that there
                #   will only be a few entires that fulfill the requirement
                while list[comparisonObjectIndex][0] == object[0]:
                    comparisonObjectIndex += 1
            
            #This will insert the object after the one it was comapred to
            list.insert(comparisonObjectIndex, object)

            #The objects index is returned in case it is to be used when displaying the leaderboard
            return(comparisonObjectIndex)
        
        #If the object has a lover value than the one it aws compared to
        elif comparisonValue > object[0]:
            #All objects with the compared value or higher is removed from the objects to comapre with
            comparisonObjects = comparisonObjects/2
        
        #If the object has a higher value than the one it was comapred to
        else:
            #All objects with the compared value or lower is remoed from the comaprison and added to 
            # the objects to be in front of the object to be inserted
            comparisonObjects = comparisonObjects/2
            objectsInFront += comparisonObjects

def drawFrame(centerX, centerY, width, height, colour = (255, 255, 255)):
    #Draws a rectagnle with specified dimentions and colour (or white) in the speficied location
    frame = pygame.draw.rect(screen, colour, [centerX - width/2, centerY - height/2, width, height])
    
    #Draws a black outline around the rectangle
    pygame.draw.rect(screen, (0, 0, 0), [frame.left, frame.top, width, height], width=2)

def writeText(text, leftX, topY, smallFont = False):
    #Checks if the text should be generated with a smaller font
    if smallFont == False:
        #Renders a large text
        textString = largeTextFont.render(str(text), 1, (0, 0, 0))
    else:
        #Renders a small text
        textString = smallTextFont.render(str(text), 1, (0, 0, 0))
    
    #Blits the text to it's desired location
    screen.blit(textString, (leftX, topY))

def displayCard(centerX, centerY, number, colour):
    #Draws the farme of the card
    drawFrame(centerX, centerY, cardWidth, cardHeight, colour)
    
    #Draws the large number on the card
    largeNumber = largeNumberFont.render(str(number), 1, (0, 0, 0))
    screen.blit(largeNumber, (centerX - 18, centerY - 25))
    
    #Draws the samll number in the corner of the card
    smallNumber = smallNumberFont.render(str(number), 1, (0, 0, 0))
    screen.blit(smallNumber, (centerX - cardWidth/2 + 2, centerY - cardHeight/2 + 2))

def displayHand():
    global cardDisplayWidth
    cardShift = 0
    
    #Covers up the old hand
    pygame.draw.rect(screen, backgroundColour, [0, windowHeight - cardHeight, windowWidth, cardHeight])
    
    #Covers the messsage stating that a clicked card cannot be played
    pygame.draw.rect(screen, backgroundColour, [windowWidth/2 - 80, windowHeight - cardHeight - 40, windowWidth/2 + 80,
                                                windowHeight/2 - cardHeight])

    #Draws the cards slightly on top of each other if they don't all fit on screeen
    if cardWidth*len(playerHand) > windowWidth:
        #This varibale determines exactly how much the cards are drawn on top of each other
        cardShift = (cardWidth*len(playerHand) - windowWidth)/len(playerHand)
    
    cardDisplayWidth = cardWidth - cardShift
    
    #All cards on the player's hand are displayed
    for i in range(len(playerHand)):
        displayCard(windowWidth/2 - 50*(len(playerHand) - 1) + cardShift/2*len(playerHand) + (100 - cardShift)*i, windowHeight - cardHeight/2,
                    str(playerHand[i][0]), cardColours[playerHand[i][1]])

def randomCard():
    #A card with a random number and colour is generated
    number = random.randint(0, 9)
    colourNumber = random.randint(0, len(cardColours) - 1)
    colour = list(cardColours)[colourNumber]
    
    #The newly generated card is returned
    return(number, colour)

def displayMiddleCard(card):
    global middleCard
    
    #The card in the middle is updated
    displayCard(windowWidth/2, windowHeight/2, card[0], card[1])
    pygame.display.update()
    
    #The new middle card is set for all future comparsions with the middle card
    middleCard = card

def playerDrawCard():
    #A radnom card is generated
    card = randomCard()
    
    cardsInFront = 0
    
    #The index of the new card's colour
    colourIndex = list(coloursOnHand).index(card[1])
    
    #All cards of colours that are in front of the new card's colour are added together
    #This is to make sure that the new card is compared with cards of the same colour
    for i in range(colourIndex):
        cardsInFront += coloursOnHand[list(coloursOnHand)[i]]
    
    #The new card is compared with cards of the same colour
    comparisonCards = coloursOnHand[card[1]]
    
    #The number of cards of the new card's colour is updated
    coloursOnHand[card[1]] += 1
    
    #The card is inserted into the right index in the player's hand
    objectInserter(card, playerHand, comparisonCards, False, cardsInFront)

def opponentDrawCard():
    #The opponent is given a random card
    #It doesn't have to be sorted sicne all card are always checked wether they can be played or not
    card = randomCard()
    opponentHand.append(card)
    
    #It's preferences are updated to make it prefer to play card that can lead to this one
    opponentColourPreferences[card[1]] += 1
    opponentNumberPreferences[card[0]] += 1

def drawSmallButton(text, centerX, centerY, colour = (255, 255, 255)):
    #A normal button is drawn
    drawFrame(centerX, centerY, smallButtonWidth, buttonHeight, colour)

    #Text is written inside the button
    writeText(text, centerX - 20 - 5.5*len(text), centerY - 15)

def drawLargeButton(text, centerY, colour = (255, 255, 255)):
    #A wider button is drawn
    drawFrame(buttonColumnX, centerY, largeButtonWidth, buttonHeight, colour)

    #Thge text is written in the larger button
    writeText(text, buttonColumnX - 110, centerY - 15)

def unoButton(pressed):
    global unoButtonPressed
    
    #If the button is active
    if len(playerHand) == 1:
        #If the button has been pressed
        if pressed == True:
            drawSmallButton('UNO', buttonColumnX, buttonUnoY, cardColours['Green'])
            
            #This variable is checked when the player plays their last card
            unoButtonPressed = True
        #If the button hasn't been pressed
        else:
            drawSmallButton('UNO', buttonColumnX, buttonUnoY, cardColours['Red'])
            
            #This variable is checked when the player plays their last card
            unoButtonPressed = False
    #If the button is inactive
    else:
        drawSmallButton('UNO', buttonColumnX, buttonUnoY, (125, 125, 125))

def displayOpponentHand():
    #Draws the opponent's hand, displayed as a white card with their number of cards as it's number
    drawFrame(windowWidth/2, cardHeight/2, cardWidth, cardHeight)

    number = largeNumberFont.render(str(len(opponentHand)), 1, (0, 0, 0))
    
    #If more then one digit is used to display the number
    if len(opponentHand) > 9:
        screen.blit(number, (windowWidth/2 - 38, cardHeight/2 - 25))
    #If they only have one card left
    elif len(opponentHand) == 1:
        writeText('UNO!', windowWidth/2 - 44, cardHeight/2 - 10)
    #If one digit is used and they ahev more than one card left
    else:
        screen.blit(number, (windowWidth/2 - 18, cardHeight/2 - 25))

def isPlayerTurn(playerTurn):
    global turnCounter
    #If it's the player's turn
    if playerTurn == True:
        drawFrame(turnDisplayX, turnDisplayY, turnDisplayWidth, turnDisplayHeight, cardColours['Green'])
        writeText('Your turn', turnDisplayX - 80, turnDisplayY - 15)
        
    #If it's the oppoenent's turn
    else:
        drawFrame(turnDisplayX, turnDisplayY, turnDisplayWidth, turnDisplayHeight, cardColours['Red'])
        writeText("Opponent's turn", turnDisplayX - 135, turnDisplayY - 15)
        
        #Advances the turn by one
        #It is placed here, since playerTurn == True is also called upon refreshing the play area
        turnCounter += 1

def opponentTurn():
    #The turn display is updated
    isPlayerTurn(False)
    pygame.display.update()
    
    #The opponent waits
    time.sleep(1)
    
    bestPlayIndex = None
    bestPlayValue = 0
    currentIndex = -1
    
    #All cards in the opponent's ahnd are checked
    for comparisonCard in opponentHand:
        currentIndex += 1
        
        #If the card can be played
        if comparisonCard[0] == middleCard[0] or comparisonCard[1] == middleCard[1]:
            #Gives the card a value based of the opponent's preferences
            comparisonCardValue = opponentNumberPreferences[comparisonCard[0]] + opponentColourPreferences[comparisonCard[1]]
            
            #Sets the card as the best option if there either isn't a different playable card yet or the new card is prefered
            if bestPlayIndex == None or comparisonCardValue > bestPlayValue:
                bestPlayIndex = currentIndex
                
                bestPlayValue = comparisonCardValue
    #If there is a card that can be played
    if bestPlayIndex != None:
        #The best card is played
        displayMiddleCard(opponentHand[bestPlayIndex])
        
        #Said card's effect on the opponent's prefered play is removed
        opponentNumberPreferences[opponentHand[bestPlayIndex][0]] -= 1
        opponentColourPreferences[opponentHand[bestPlayIndex][1]] -= 1
        
        #The card is removed from the opponent's hand
        opponentHand.pop(bestPlayIndex)
    #If no card can be plated
    else:
        #Opponent draws a card
        opponentDrawCard()
    
    #Opponent's ahnd is updated
    displayOpponentHand()

    #Opponenet wins fi they have no cars left
    if len(opponentHand) == 0:
        endOfGame("Loss")
    
    #Game continues
    else:
        isPlayerTurn(True)

def leaderboardEntry(ranking, name, score, topY):
    #How entries in the leaderboard are displayed
    writeText(ranking, windowWidth/2 - 80, topY, True)
    writeText(name, windowWidth/2 - 50, topY, True)
    writeText(score, windowWidth/2 + 60, topY, True)

def displayLeaderboard():
    #Shows a fitting header
    writeText("Leaderboard", windowWidth/2 - 110, windowHeight/6)
    
    #Shows the five top entires on the leaderboard
    for i in range(5):
        leaderboardEntry(i + 1, leaderboard[i][1], leaderboard[i][0], windowHeight/3 + 30*(i - 1))
    
    #Shows your position on the leaderboard
    writeText("Your score:", windowWidth*0.5 - 55, windowHeight*0.6 - 30, True)
    leaderboardEntry(playerRanking, playerName, playerScore, windowHeight*0.6)

def infoWindow(windowName):
    global currentWindow
    
    #Affects what buttons you can push
    currentWindow = "infoWindow"
    
    screen.fill(backgroundColour)
    
    #If the "rules"-button was pressed
    if windowName == "Rules":
        writeText("Rules", windowWidth/2 - 60, windowHeight/6)
        
        paragraphText = ("Each player starts with three cards.",
                        "On your turn, you can either play a card which matches",
                        "the colour or number of the card in the middle or draw a card.",
                        "If you don't say UNO before playing your last card,",
                        "you draw three new cards.",
                        "The first player to play all their cards, win.")
        
        row = 0
        
        #Writes the previous text as seperate lines
        for i in paragraphText:
            writeText(i, windowWidth/6, windowHeight/3 + 25*row, True)
            row += 1
    #If the "leaderboard"-button was pressed
    else:
        displayLeaderboard()
    
    #The "Back"-button that returns you to the play area
    drawSmallButton("Back", windowWidth/2, buttonReturnY)

def endOfGame(outcome):
    #The game end window
    global currentWindow
    global playerScore
    global playerRanking
    
    #Affects what buttons you can push
    currentWindow = "endOfGame"
    
    screen.fill(backgroundColour)
    
    #Gives you a score and leaderboard position if you win
    if outcome == "Win":
        writeText("You won", windowWidth/2 - 70, windowHeight/12)
        
        playerScore = turnCounter - len(opponentHand) - 3 #The -3 is for the three starting cards
        player = (playerScore, playerName)
        playerRanking = int(objectInserter(player, leaderboard, len(leaderboard), True) + 1)
        
        #The new leaderboard is saved to the "leaderboard"-file
        with open("leaderboard.pkl", "wb") as filehandle:
            pickle.dump(leaderboard, filehandle)
    #Doesn't give you a score if you lose
    else:
        writeText("You lost", windowWidth/2 - 70, windowHeight/12)
    
    #Shows the leaderboard
    displayLeaderboard()
    
    #Button to restart
    drawSmallButton("Restart", windowWidth/2, buttonReturnY)

def playAreaInteractions():
    #All interaction in the play area
    global opponentColourPreferences
    global opponentNumberPreferences
    
    #Clicked in player hand area
    if pygame.mouse.get_pos()[1] >= windowHeight - cardHeight and pygame.mouse.get_pos()[0] >= (windowWidth - cardWidth*len(playerHand))/2 and pygame.mouse.get_pos()[0] <= (windowWidth + cardWidth*len(playerHand))/2:
        #Checks if a card was clickerd on
        #If the cards are compressed on screen
        if len(playerHand)*cardWidth > windowWidth:
            index = math.floor(pygame.mouse.get_pos()[0]/cardDisplayWidth)
        #If the cards aren't compressed on screen
        #This takes mouseX, subtracts the area to the left of the cards (so you get the mouseX relative to 
        # the left side of the leftmost card) and divides the result by the width of the cards
        else:
            index = math.floor((pygame.mouse.get_pos()[0] - 
                                (windowWidth - cardWidth*len(playerHand))/2)/cardWidth)
        
        #Clicked on unplayable card
        if middleCard[0] != playerHand[index][0] and middleCard[1] != playerHand[index][1]:
            #Tells the player that the card is unplayable
            writeText("Unplayable card", windowWidth/2 - 80, windowHeight - cardHeight - 40, True)
            
            #Interaction ends immediately
            return
        
        #Sets the middle card to the newly played card
        displayMiddleCard(playerHand[index])
        
        #Removes the played card from the number of cards of each colour
        coloursOnHand[playerHand[index][1]] -= 1
        
        #Makes the opponent less likely to play cards that have a higher cahnce of being good for the player
        opponentColourPreferences[playerHand[index][1]] -= 0.5
        opponentNumberPreferences[playerHand[index][0]] -= 0.5
        
        #Remove card from player hand
        playerHand.pop(index)
        
        #Played last card
        if len(playerHand) == 0:
            #UNO button not pressed
            if unoButtonPressed == True:
                #Victory screen is drawn
                endOfGame("Win")
                
                #Interaction ends immediately
                return
            
            #The player draws three cards
            for i in range(3):
                playerDrawCard()
                
            #Reset all preference scores, since the player gets a fresh hand
            opponentColourPreferences = {'Red': 0, 'Green': 0, 'Blue': 0, 'Yellow': 0}
            opponentNumberPreferences = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
            
            #They still need to account for their own cards on hand
            for opponentCard in opponentHand:
                opponentColourPreferences[opponentCard[1]] += 1
                opponentNumberPreferences[opponentCard[0]] += 1
        
        #The new player hand is drawn
        displayHand()
        
        #Resets the UNO button
        unoButton(False)
        
        #Opponent's turn
        opponentTurn()

    #Button column in playArea
    if pygame.mouse.get_pos()[0] >= buttonColumnX - smallButtonWidth/2 and pygame.mouse.get_pos()[0] <= buttonColumnX + smallButtonWidth/2:
        #Draw card button
        if pygame.mouse.get_pos()[1] >= buttonDrawY - buttonHeight/2 and pygame.mouse.get_pos()[1] <= buttonDrawY + buttonHeight/2:
            #Player draws a card and tehir new hand is drawn
            playerDrawCard()
            displayHand()
            
            #More likely to play cards the player cannot play on
            opponentColourPreferences[middleCard[1]] += 1
            opponentNumberPreferences[middleCard[0]] += 1
            
            #Resets the UNO button
            unoButton(False)
            
            #Opponent's turn
            opponentTurn()
        
        #UNO button
        elif pygame.mouse.get_pos()[1] >= buttonUnoY - buttonHeight/2 and pygame.mouse.get_pos()[1] <= buttonUnoY + buttonHeight/2:
            #The UNO button is triggered
            unoButton(True)
        
        #Rules gutton
        elif pygame.mouse.get_pos()[1] >= buttonRulesY - buttonHeight/2 and pygame.mouse.get_pos()[1] <= buttonRulesY + buttonHeight/2:
            #Shows the rules window
            infoWindow("Rules")
    
    #Leaderboard button
    if pygame.mouse.get_pos()[0] >= buttonColumnX - largeButtonWidth/2 and pygame.mouse.get_pos()[0] <= buttonColumnX + largeButtonWidth/2 and pygame.mouse.get_pos()[1] >= buttonLeaderboardY - buttonHeight/2 and pygame.mouse.get_pos()[1] <= buttonLeaderboardY + buttonHeight/2:
        #Shows the leaderboard window
        infoWindow("Leaderboard")

def interactions():
    #Everything that can be intereacted with in the game
    global running
    global currentWindow
    
    while running:

        for event in pygame.event.get():

            #If the application is closed
            if event.type == pygame.QUIT:
                running = False
            
            if pygame.mouse.get_pressed() == (1,0,0):
                #All interactions in the main play area
                if currentWindow == "playArea":
                    playAreaInteractions()
                
                #Back button in infoWindow
                elif currentWindow == "infoWindow":
                    if pygame.mouse.get_pos()[0] >= windowWidth/2 - smallButtonWidth/2 and pygame.mouse.get_pos()[0] <= windowWidth/2 + smallButtonWidth/2 and pygame.mouse.get_pos()[1] >= buttonReturnY - buttonHeight/2 and pygame.mouse.get_pos()[1] <= buttonReturnY + buttonHeight/2:
                        #Returns to play area
                        playArea()
                
                #Restart button in endOfGame window
                else:
                    if pygame.mouse.get_pos()[0] >= windowWidth/2 - smallButtonWidth/2 and pygame.mouse.get_pos()[0] <= windowWidth/2 + smallButtonWidth/2 and pygame.mouse.get_pos()[1] >= buttonReturnY - buttonHeight/2 and pygame.mouse.get_pos()[1] <= buttonReturnY + buttonHeight/2:
                        #Starts a new game
                        newGame()

                pygame.display.update()

def playArea():
    #The play area is deawn
    global opponentColourPreferences
    global opponentNumberPreferences
    global running
    global currentWindow

    screen.fill(backgroundColour)

    #All cards are displayed
    displayMiddleCard(middleCard)
    displayHand()
    displayOpponentHand()

    #All buttons are displayed
    drawLargeButton('Leaderboard', buttonLeaderboardY)
    drawSmallButton('Rules', buttonColumnX, buttonRulesY)
    drawSmallButton('Draw', buttonColumnX, buttonDrawY)
    unoButton(False)

    #The player starts
    isPlayerTurn(True)
    
    pygame.display.update()
    
    currentWindow = "playArea"
    
    interactions()

def newGame():
    #A new game is started and all variables are reset
    variables()
    global middleCard

    #Each player gets a new hand with three cards
    for i in range(3):
        playerDrawCard()
        opponentDrawCard()

    #A random card is put in the middle
    middleCard = randomCard()

    playArea()

def start():
    #When the game first starts
    pygame.font.init()
    variables()
    global screen
    global running
    global playerName
    global leaderboard
    
    #The saved leaderboard is loaded in from the "leaderboard"-file
    with open("leaderboard.pkl", "rb") as filehandle:
        leaderboard = pickle.load(filehandle)

    #This can be used to check the leaderboard
    # print(leaderboard)
    
    #Asks for the player's name
    print("##########################")
    print("# Please enter your name #")
    print("##########################")
    print()
    playerName = input()
    
    #Creates the game window
    screen = pygame.display.set_mode((windowWidth, windowHeight))
    pygame.display.set_caption(windowName)
    screen.fill(backgroundColour)

    pygame.display.flip()

    running = True
    
    newGame()

start()