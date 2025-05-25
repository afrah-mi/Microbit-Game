#-----------------------------------------------------------------------------
# Name:        Using microbit class (using microbit class.py)
# Purpose:     This program is an example to demonstrate how to use the Microbit class to interface
#              with a microbit that is running serial output.
#
# Author:      Mr. Brooks-Prenger
# Created:     10-March-2021
# Updated:     3-June-2022
#-----------------------------------------------------------------------------
#--------------------------EXAMPLE CODE TO RUN ON MICROBIT -------------------
# from microbit import *
# import utime
# 
# while True:
#     
#     display.show(Image.HEART)
#     print('heart ', utime.ticks_ms())
#     utime.sleep_ms(15)
# 
#-----------------------------------------------------------------------------
# 
from Microbit import *


mb = Microbit()

while mb.isReady():
    
    line = mb.nonBlockingReadLine()
    if line != None:
        print(line)
        
    
    #time.sleep(1)
try:
    mb.closeConnection()
except AttributeError as e:
    print(f'Error - Connection could not be closed.  ({e})')
    
