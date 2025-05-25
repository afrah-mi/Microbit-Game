#-----------------------------------------------------------------------------
# Name:        Floapy Fly
# Purpose:     Detects/reads microbit data and moves character, shoots, and changes size of balloon accordingly
#
# Author:      Afrah Iqbal
# Created:     14-November-2022
# Updated:     23-November-2022
#-----------------------------------------------------------------------------

''' 
from microbit import *

DELAY_VALUE = 50

while True:
    x = accelerometer.get_x()
    y = accelerometer.get_y()
    a = button_b.is_pressed() 
    b = button_a.is_pressed()
    g = accelerometer.was_gesture("shake")
    print("x, y, a, b, g:", x, y, a, b, g)
    sleep(DELAY_VALUE)    
    
'''
#-----------------------------------------------------------------------------

import pygame
import random
import math

from Microbit import *


def distFromPoints(point1, point2):
    """
    Calculates distance between two points
    """
    distance = math.sqrt(((point2[0]-point1[0])**2)+((point2[1]-point1[1])**2))
    
    return distance
      

def main():
    
    
    """ Set up the game and run the main game loop """
    pygame.init()       # Prepare the pygame module for use
    surfaceSize = 500   # Desired physical surface size, in pixels.
    
    clock = pygame.time.Clock()                                        #Force frame rate to be slower
    font = pygame.font.SysFont("Courier New", 40)                      #set font
    mainSurface = pygame.display.set_mode((surfaceSize, surfaceSize))  #surface

    #LOADING IMAGES
    floapyImg = pygame.image.load("floapy.png")    #Controled Character
    cloudImg = pygame.image.load("angrycloud.png") #Evil cloud
    windImg = pygame.image.load("wind.png")        #Good cloud
    startImg = pygame.image.load("floapyStartN.png")
    pointImg = pygame.image.load("floapyPoint.png")
    rulesImg = pygame.image.load("rules.png")
    
    #CHARACTER RELATED VARIABLES
    floapyPos = [220,220]                             #Character position point
    floapySpeed = [0,0]                               #Character speed of movement
    balloonRadius = 10                                #initial radius of character balloon
    circlePoint = [floapyPos[0]+60, floapyPos[1]-30]  #Balloon Point
    
    #WORDS
    words = "START"                                               #words to put on start screen
    renderedText = font.render(words, 1, pygame.Color("black"))   #text
    font = pygame.font.SysFont("Courier New", 30)                 #change font to be smaller for other words
    
    #INITIALIZING GYRO VALUES
    gyroA = "False" 
    gyroB = "False" 
    gyroX = 0       
    gyroY = 0
    
    #SHAPES
    aPoint = [50, 150]           #point
    bPoint = [0, 200]           #point
    rectColor = (172, 195, 232)  #color    
    rectDim = [150, 100]         #dimensions

    #SHOT VARIABLES
    shotPos = [floapyPos[0]-20, floapyPos[0]+20]   #X and Y Point of Shot
    shotDim = [10, 25]                             #dimensions
    shotSpeed = [0,0]                              #X and Y Speeds
    shotColor = (0, 0, 0)                          #color
    shot = "unreleased"                            #status
    
    #CLOUD VARIABLES
    cloudPosList = []
    numCloud = 3                                   #number of clouds
    cloudX = int(random.randrange(surfaceSize-67)) #X range
    cloudY = int(random.randint(-500, -50))        #Y range
    
    for count in range(numCloud):
        cloudPosList.append([cloudX, cloudY])
        cloudX = int(random.randrange(surfaceSize-67)) #reset
        cloudY = int(random.randint(-500, 0))

    windX = int(random.randrange(surfaceSize-67))  #good clouds varaibles
    windY = int(random.randint(-500, -50))
    windPos = [windX, windY]

    #SCORE RELATED VARIABLES
    score = 0
    scoreNew = 0
    gameTimer = 0
    
    #Screen Organization
    programState = "set up microbit"
        
    while True:
        ev = pygame.event.poll()    # Look for any event
        if ev.type == pygame.QUIT:  # Window close button clicked?
            break                   #   ... leave game loop
            
        if programState == "set up microbit":
            
            mb = Microbit()

            if not mb.isReady():
                print('Error opening Microbit - Trying again in 5 seconds')    
                time.sleep(5)
            else:
                programState = "start"
                           
        elif programState == "start": #start screen
            #Grab data from the microbit
            line = mb.nonBlockingReadLine()
            if line:                         
                data = line.split(' ')
                *label, gyroX, gyroY, gyroA, gyroB, gyroG = data
                print(f' ({label} {gyroX}, {gyroY}, {gyroA}, {gyroB}, {gyroG})')

            
                floapySpeed[0] += (int(gyroX)/2500) #shlows down movement to imitate a balloon
                floapySpeed[1] += (int(gyroY)/2500)

                
                if gyroA == "True":                              
                    programState = "game"  #change screen
                elif gyroB == "True":      #help button
                    programState = "game"
                    

        if programState == "game": #game screen 
            gyroA = "False" 
            for count in range(numCloud):          #moves cloud down the screen by increasing y value
                cloudPosList[count][1] += 0.5 
                if cloudPosList[count][1] > 600:   #resets clouds once theyve passed the window length
                    cloudPosList[count][1] = random.randint(-200, 0)
                    cloudPosList[count][0] = random.randrange(surfaceSize-46)
                    
            windPos[1] += 0.5 
            if windPos[1] > 600:
                    windPos[1] = random.randint(-200, 0)
                    windPos[0] = random.randrange(surfaceSize-46)            

            line = mb.nonBlockingReadLine()
            if line:  # If it isn't a blank line
                      #Update your data
                data = line.split(' ')
                *label, gyroX, gyroY, gyroA, gyroB, gyroG = data  
                print(f' ({label} {gyroX}, {gyroY}, {gyroA}, {gyroB}, {gyroG})') #prints values

                floapySpeed[0] += (int(gyroX)/9500) #movement of charater
                floapySpeed[1] += (int(gyroY)/9500) #movement of character
                gameTimer += 0.5                    #timer
                
                #collision detection with walls
                if floapyPos[0] < 0:
                    floapyPos[0] = 0
                    floapySpeed[0] = 0
                elif floapyPos[0] > 430:
                    floapyPos[0] = 430
                    floapySpeed[0] = 0
                    
                elif floapyPos[1] < 0:
                    floapyPos[1] = 0
                    floapySpeed[1] = 0
                elif floapyPos[1] > 410:
                    floapyPos[1] = 410
                    floapySpeed[1] = 0
                    
                #move character
                else:
                    floapyPos[0] += floapySpeed[0]
                    floapyPos[1] += floapySpeed[1]
                    
                #if button pressed release shot
                if gyroA == "True":
                    shotSpeed[1] -= 0.5
                    shot = "released"

                    

        #LOGIC
                    
        #if shot unreleased keep it connected with the character
        if shot == "unreleased":
            shotPos[0] = floapyPos[0]
            shotPos[1] = floapyPos[1]
        #if shot released move up the screen
        if shot == "released":
            shotPos[1] += shotSpeed[1]
            if shotPos[1] < -25:
                shot = "unreleased"
                
        circlePoint = [floapyPos[0]+60, floapyPos[1]-30]
        
        #collision detection with cloud and shot
        for count in range(numCloud): 
            if shotPos[0] >= cloudPosList[count][0] and shotPos[0]+10 <= cloudPosList[count][0]+70: 
                if shotPos[1] <= cloudPosList[count][1]+50 and shotPos[1] >= cloudPosList[count][1]:
                    cloudPosList[count][1] = -100
                    score = score + 1
        
        #collision detection with cloud and balloon           
            if distFromPoints(circlePoint, (cloudPosList[count][0]+33, cloudPosList[count][1]+23)) < (40): 
                    cloudPosList[count][1] = -100
                    balloonRadius = balloonRadius - 5

        #collision detection with other cloud and balloon
        if distFromPoints(circlePoint, (windPos[0]+33, windPos[1]+23)) < (40):
                windPos[1] = -100
                balloonRadius = balloonRadius + 5
                
        #move to endgame if user lost main game
        if balloonRadius < 5:
            programState = "endgame"
        
        #endgame stage
        if programState == "endgame":
            line = mb.nonBlockingReadLine()
            if line:                        # If it isn't a blank line
                data = line.split(' ')
                *label, gyroX, gyroY, gyroA, gyroB, gyroG = data
                print(f' ({label} {gyroX}, {gyroY}, {gyroA}, {gyroB}, {gyroG})')
                
                gameTimer = gameTimer - 1 #use the time collected from before, and decrease it until 0
                
                if gameTimer > 0:         #if time remains and microbit is being shook, balloon gets biggger
                    if gyroG == "True":
                        balloonRadius += 5
                elif gameTimer <= 0:     #if time is up, end screen
                    gameTimer = 0
                    programState = "end"
                    
        #calculate final score           
        if programState == "end":
            scoreNew = score + int(balloonRadius/5)
            
   
        #ALL TEXT/WORDS
        words = "Score:" f'{score}'
        wordsTwo = "Time:" f'{int(gameTimer)}'
        wordsFinal = "Shake!!"
        wordsAir = "+ " f'{int(balloonRadius/5)}' " endgame points!"
        wordsFinalScore = "Final Score:" f'{scoreNew}'
        renderedTextTwo = font.render(words, 1, pygame.Color("red"))       
        renderedTextThree = font.render(wordsTwo, 1, pygame.Color("red")) 
        renderTextFinal = font.render(wordsFinal, 1, pygame.Color("white"))
        renderTextAir = font.render(wordsAir, 1, pygame.Color("white"))
        renderTextNew = font.render(wordsFinalScore, 1, pygame.Color("white"))
        
        
        #DRAWING FOR EACH PROGRAMSTATE
        if programState == "start": #start screen
            mainSurface.blit(startImg, (0,0))
            mainSurface.blit(pointImg, (250, 175))
            mainSurface.blit(rulesImg, bPoint)
            pygame.draw.rect(mainSurface, rectColor, (aPoint, rectDim)) #start button
            mainSurface.blit(renderedText, (65, 175))
            pygame.display.flip() 
            
        if programState == "game": #game screen
            mainSurface.fill((250, 223, 147))
            pygame.draw.rect(mainSurface, shotColor, (shotPos, shotDim))
            mainSurface.blit(floapyImg, floapyPos)
            pygame.draw.line(mainSurface, (0, 0, 0), [floapyPos[0]+60, floapyPos[1]-30], [floapyPos[0]+60, floapyPos[1]+60])
            pygame.draw.circle(mainSurface, (255, 0, 0), [floapyPos[0]+60, floapyPos[1]-30], balloonRadius)
            for count in range(numCloud):
                mainSurface.blit(cloudImg, cloudPosList[count])
            mainSurface.blit(windImg, windPos)
            mainSurface.blit(renderedTextThree, (20, 20))
            mainSurface.blit(renderedTextTwo, (20, 50))
            pygame.display.flip() 
            
        if programState == "endgame": #endgame screen
            mainSurface.fill((0, 0, 0))
            mainSurface.blit(renderedTextThree, (20, 20))
            mainSurface.blit(renderedTextTwo, (20, 50))
            mainSurface.blit(renderTextFinal, (200, 80))
            pygame.draw.circle(mainSurface, (255, 0, 0), [250, 250], balloonRadius)

        if programState == "end": #end screen
            mainSurface.fill((0, 0, 0))
            mainSurface.blit(renderedTextTwo, (200, 50))
            mainSurface.blit(renderTextAir, (90, 80))
            mainSurface.blit(renderTextNew, (140, 120))
            pygame.draw.circle(mainSurface, (200, 0, 0), [250, 250], balloonRadius)


        pygame.display.flip() #Update the display
        clock.tick(60) #Force frame rate to be slower

    #-----------------END of main while True loop!------------------------------
        
    if mb != None:
        mb.close()  #Close the microbit serial connection
    
    pygame.quit()     # Once we leave the loop, close the window.
    

main()
