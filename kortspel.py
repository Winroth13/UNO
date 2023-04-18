import pygame

def variables():
    global backgroundColour
    global windowWidth
    global windowHeight
    global windowName
    global playerHand

    backgroundColour = (200, 200, 200)
    windowWidth = 800
    windowHeight = 600
    windowName = 'UNO'
    playerHand = {
        [0, 'Green'],
        [2, 'Yellow'],
        [9, 'Blue']
        [8, 'Red']
    }

def displayCards():
    global playerHand

    for i in len(playerHand):
        pass
        #Dispaly card side by side with the number in the middle.

def start():
    variables()
    global backgroundColour
    global windowWidth
    global windowHeight
    global windowName

    screen = pygame.display.set_mode((windowWidth, windowHeight))
    pygame.display.set_caption(windowName)
    screen.fill(backgroundColour)

    pygame.display.flip()

    running = True

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

start()