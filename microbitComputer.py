# #from microbit import *
# 
# DELAY_VALUE =100
# 
# while True:
#     x = accelerometer.get_x()
#     y = accelerometer.get_y()
#     z = accelerometer.get_z()
#     print("x, y, z:", x, y, z)
#     #display.show(Image.YES)
#     sleep(DELAY_VALUE)
#     #display.show(Image.NO)
#     #sleep(DELAY_VALUE)
import pygame
from Microbit import *
floapyImg = pygame.image.load("floapy.png")


class Floapy():
    '''
    A class to represent a ball rolling around the screen
    
    '''
    def __init__(self, posIn, sizeIn, colorIn):
        self.pos = [0,0] #starting pos
        self.speed = [0,0] #starting speed
        self.size = 10 #size of ball
        #self.color = [20, 20, 40] #color of ball
        
    def draw(self, surfaceIn):
        mainSurface.blit(floapyImg, self.pos)
        
    def update(self):
        
        
        if self.pos[0] < 10:
            self.pos[0] = 10
            self.speed[0] = 0
        elif self.pos[0] > 470:
            self.pos[0] = 470
            self.speed[0] = 0
            
        elif self.pos[1] < 10:
            self.pos[1] = 10
            self.speed[1] = 0
        elif self.pos[1] > 470:
            self.pos[1] = 470
            self.speed[1] = 0
        else:
            self.move(self.speed[0],self.speed[1])

    def move(self, xIn=0, yIn=0):
        self.pos[0] += xIn
        self.pos[1] += yIn
    
    def accelerate(self, xIn=0, yIn=0):
        self.speed[0] += xIn
        self.speed[1] += yIn


def normalizeGyroValue(gyroString, startingY, displayRect):
    '''
    This function normalizes the gyro values from ~ +/- 1050 to  ~ +/- 200 to fit on screen

    Parameters
    ----------
    gyroString - The gyro value as a string
    startingY - The initial y value to place the rect at
    displayRect - The rect value to be modified to create the bar

    Returns
    -------
    None - Values required are changed in displayRec as passed by value

    '''  
    gyroValue = int(gyroString)
    
    gyroValue = (gyroValue/1050)*200 #Reduce gyrovalue to only scale between approx -200 and 200

    if gyroValue < 0:
        displayRect[1] = startingY+gyroValue
        displayRect[3] = -gyroValue
    else:
        displayRect[1] = startingY
        displayRect[3] = gyroValue



def main():
    
    
    """ Set up the game and run the main game loop """
    pygame.init()      # Prepare the pygame module for use
    surfaceSize = 480   # Desired physical surface size, in pixels.
    
    clock = pygame.time.Clock()  #Force frame rate to be slower


    # Create surface of (width, height), and its window.
    mainSurface = pygame.display.set_mode((surfaceSize, surfaceSize))

    programState = "initialize"
    

    while True:
        ev = pygame.event.poll()    # Look for any event
        if ev.type == pygame.QUIT:  # Window close button clicked?
            break                   #   ... leave game loop

        if programState == "initialize":
            #TODO set up the intial data for my 3 bar graphs
            #TODO Draw a loading message
            startingY =240
            gyroXRectBase = [50,startingY,25,50]
            gyroYRectBase = [100,startingY,25,0]
            gyroZRectBase = [150,startingY,25,0]
            
            #Set up rolling ball
            floapy = Floapy( [220,220], 40, (50,50,50))
            
            programState = "set up microbit"
            
        elif programState == "set up microbit":
            
            mb = Microbit()

            if not mb.isReady():
                print('Error opening Microbit - Trying again in 5 seconds')    
                time.sleep(5)
            else:
                programState = "display"
            
        elif programState == "display":
            #Grab the data from the microbit
            line = mb.nonBlockingReadLine()
            if line:  # If it isn't a blank line
                #Update your data
                #print(line)
                data = line.split()
                #print(data)
                *label, gyroX, gyroY, gyroZ = data
                #print(f' ({gyroX}, {gyroY}, {gyroZ})')
                
                floapy.accelerate(int(gyroX)/1500,0)
                floapy.accelerate(0,int(gyroY)/1500)
                
                normalizeGyroValue(gyroX, startingY, gyroXRectBase)
                normalizeGyroValue(gyroY, startingY, gyroYRectBase)
                normalizeGyroValue(gyroZ, startingY, gyroZRectBase)
                #print(gyroXRectBase)
                
                
            mainSurface.fill((250, 223, 147))
            
            pygame.draw.rect(mainSurface, (255,0,0), gyroXRectBase)
            pygame.draw.rect(mainSurface, (0,255,0), gyroYRectBase)
#             pygame.draw.rect(mainSurface, (0,0,255), gyroZRectBase)
            
           

#             floapy.update()
            mainSurface.blit(floapyImg)
            #floapy.blit(mainSurface)
            #TODO Draw the bar graph
            
        
            
            
            

        pygame.display.flip() #Update the display
        clock.tick(60) #Force frame rate to be slower

    #-----------------END of main while True loop!------------------------------
        
    if microbit != None:
        microbit.close()  #Close the microbit serial connection
    
    pygame.quit()     # Once we leave the loop, close the window.
    

main()
