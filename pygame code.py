import pygame


def main():
    
    
    """ Set up the game and run the main game loop """
    pygame.init()      # Prepare the pygame module for use
    surfaceSize = 500   # Desired physical surface size, in pixels.
    
    clock = pygame.time.Clock()  #Force frame rate to be slower
    font = pygame.font.SysFont("Courier New", 40)
    words = "START"  #words to put on screen
    renderedText = font.render(words, 1, pygame.Color("black")) #during game text
    gyroA = "False"
    gyroB = "False"
    aPoint = [50, 150] #point
    bPoint = [50, 200] #point
    rectColor = (172, 195, 232) #color    
    rectDim = [150, 100]  #dimensions
    startImg = pygame.image.load("floapyStart.png")
    pointImg = pygame.image.load("floapyPoint.png") 

    circlePos = [50,100]  #X and Y Positions
    circleDim = [10, 25]  #dimensions
    circleSpeed = [0,0]  #X and Y Speeds
    circleColor = (255, 0, 0)        # A color is a mix of (Red, Green, Blue)

    # Create surface of (width, height), and its window.
    mainSurface = pygame.display.set_mode((surfaceSize, surfaceSize))

    programState = "start"

    while True:
        ev = pygame.event.poll()    # Look for any event
        if ev.type == pygame.QUIT:  # Window close button clicked?
            break                   #   ... leave game loop
        if ev.type == pygame.KEYDOWN:  #KEYDOWN has the attributes: key, mod, unicode, scancode
            print('A Key was pressed down.  ', end='')

        #start screen + help screen with buttons
        if programState == "start":
            if gyroA == "True": #mouse pressed                             
                    programState = "game" #change screen
            elif gyroB == "True": #help button
                    programState = "help"
        if programState == "help":
            print ('help') #make an instructions screen
        
        #game screen
        if programState == "game":
            if gyroA == "True":
                print('Move Up')
                circleSpeed[1] -= 0.05
            if gyroB == "True":
                circleSpeed[0] -= 0.05

        #ALL LOGICS
        circlePos[0] += circleSpeed[0]
        circlePos[1] += circleSpeed[1]
            
        
        
        #ALL DRAWS
        if programState == "start": #Draw for the start screen
            mainSurface.blit(startImg, (0,0))
            mainSurface.blit(pointImg, (250, 175))
            pygame.draw.rect(mainSurface, rectColor, (aPoint, rectDim))
            pygame.draw.rect(mainSurface, rectColor, (bPoint, rectDim))            
            mainSurface.blit(renderedText, (65, 200))
            pygame.display.flip() #display
        if programState == "game":
            mainSurface.fill((0, 200, 255))
            pygame.draw.rect(mainSurface, circleColor, (circlePos, circleDim))            
            pygame.display.flip() #display

        pygame.display.flip() #Update the display
        clock.tick(60) #Force frame rate to be slower

    #-----------------END of main while True loop!------------------------------
        
    if mb != None:
        mb.close()  #Close the microbit serial connection
    
    pygame.quit()     # Once we leave the loop, close the window.
    

main()