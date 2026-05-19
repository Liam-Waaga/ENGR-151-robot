'''
Defines dances and a panic function
Includes:
    -panic()        *has optional parameters
    -dance_green()
    -dance_blue()   *has optional parameters
    -dance_red()    *has optional parameters
    -victory()      *has optional parameters
Also Includes (meant for keeping clutter clear): 
    -endprogram()
    -clean_and_close()  *has optional parameters
    
#TODO:
-verify everything works
-add descriptive comments

Could sensors.py be imported rather than leds.py? Both have show_flash() and the light shows from leds.py are adapted into this file
Should a motor stop all function be added to clean_and_close() and/or endprogram()
'''
#Imports
import machine
import motion
import time
import leds
from lcd1602 import LCD
from ws2812 import WS2812

#LED Strip Setup
ws = WS2812(machine.Pin(28), 8)

#lcd Screen
lcd = LCD()

def clean_and_close(color=None):
    ''' makes sure everything is off when returning / prints saying finished with section'''
    
    if color is not None: # if given a string, it prints it in a logging meassage
        print(f'finished {color} dance')
    ws.write_all([0, 0, 0]) # makes sure led is off
    lcd.clear() # makes sure lcd is off



def endprogram():
    ''' bot sleeps for 1 hour '''
    #This effectively turns the robot off
    
    while True:
        machine.lightsleep(3600000)



def panic(flashcount=3, shutdown=True):
    ''' sos mode '''
    #This function by default is a dead end
    
    #takes in flashcount:
    #    repeats that many times
    #    (Default) otherwise: repeats 3 times
    
    #takes in leave
    #    if set to False: leaves definition
    #    (Default) otherwise: terminates program
    
    #settings:
    color = [255,0,0]
    s = (color,3,60,60)
    o = (color,3,180,180)
    rest = 100 #milliseconds
    
    
    print('panic') #logs the start of panic
    lcd.write(0, 0, '!!!PANIC!!!')
    
    for _ in range(flashcount): # plays sos in morse code
        leds.show_flash(*s)
        time.sleep_ms(rest)
        leds.show_flash(*o)
        time.sleep_ms(rest)
        leds.show_flash(*s)
        time.sleep_ms(2 * rest)
    clean_and_close('panic') #logs the end of panic
    
    if shutdown is True: # shuts robot down if not set otherwise
        endprogram()
    
    

def dance_green():
    ''' Green Dance '''
    
    text = 'Found Green!'
    
    print(text) # logs the start of green dance
    for i in range(8):
        leds.show_flash([0,255,0],3,100,50) # 3 flash blue
        ws[i] = [0, 255, 0]
        ws.write() #write a single green led at index i
        
        if i % 3 == 1: #shows 'Found ' and every once in a while reveals 3 more characters
            lcd.clear()
            lcd.write(0, 0, text[:(i+5)])
        
        if i % 2 == 0: # drive back and forth
            motion.drive_mm(-5)
        else:
            motion.drive_mm(5)
        
        time.sleep_ms(50)
        leds.show_flash([0,255,0],2,50,50) #2 flash green
        time.sleep_ms(100)
    clean_and_close('green') # logs the end of green dance



def dance_blue(repeat=0):
    ''' Blue Dance '''
    
    #takes in repeat:
    #    repeats that many times
    #    (Default) otherwise: repeats 1 times
    
    text = 'Found Blue!'
    
    print(text) # log start of blue dance
    for i in range(repeat):
        ws.write_all([0, 0, 0])
        lcd.write(0, 0, text)
        
        for _ in range(5): # fades blue in and out 5 times
            for j in range(0,256,1):
                ws.write_all([0, 0, j])
                time.sleep_us(500)
            for j in range(255,-1,-1):
                ws.write_all([0, 0, j])
                time.sleep_us(500)
                
        lcd.clear()
        leds.show_flash([50,0,100],3,100,100) #should this be lavender?
        time.sleep_ms(100)
        
        motion.turn_deg(90)
        motion.turn_deg(-180)
        motion.turn_deg(90)
    clean_and_close('blue') # log end of blue dance


def dance_red(pivots=2):
    ''' Red Dance '''

    #takes in pivots:
    #    repeats section that many times
    #    (Default) otherwise: repeats 2 times
    
    text = 'Found Red!'
    motorstrength = 40
    
    print(text)
    lcd.write(0, 0, text)
    for i in range(8):
        ws.write_all([0, 0, 0])
        ws[i] = [255, 0, 0]
        time.sleep_ms(50)
        ws.write()
        time.sleep_ms(80)
    lcd.clear()
    motion.drive_mm(-50)
    
    lcd.write(0, 0, text)
    for i in range(8):
        ws.write_all([0, 0, 0])
        ws[i] = [255, 0, 0]
        time.sleep_ms(50)
        ws.write()
        time.sleep_ms(80)
    lcd.clear()
    motion.drive_mm(50)
    
    lcd.write(0, 0, text)
    motion.turn_deg(5, motorstrength)
    for _ in range(pivots):
        motion.turn_deg(-10, motorstrength)
        motion.turn_deg(10, motorstrength)
    motion.turn_deg(-5, motorstrength)
    
    leds.show_flash([255,0,0],1,100,0)
    clean_and_close('red')



def victory(endspincount=5,shutdown=False):
    ''' Victory Dance '''
    #This function can be a dead end
    
    #takes in endspincount
    #    spins that many times
    #    (Default) otherwise: spins 5 times
    
    #takes in end
    #    if set to true: terminates program
    #    (Default) otherwise: leaves definition (robot will be probably be in a random direction)
    
    
    #prep
    ws.write_all([0, 0, 0])
    lcd.clear()
    text = '    ' + 'Victory!' #second set should be 8 characters to look good
    endspincountdeg = endspincount * (-360)
    
    
    #the real stuff
    print('Victory Time!')
    lcd.write(0, 0, text)
    leds.show_flash([0,0,255],1,500,500)
    leds.show_flash([0,255,0],1,500,500)
    leds.show_flash([255,0,0],1,500,500)
    lcd.clear()
    
    for i in range(8):
        lcd.write(0, 0, text[:(i+5)])
        ws[i] = [0, 0, 255]
        time.sleep_ms(50)
        ws.write()
        time.sleep_ms(10)
        motion.turn_deg(5)
        lcd.clear()
        
    time.sleep_ms(10)
    
    for i in range(8):
        lcd.write(0, 0, (i+4)*' ' + text[(i+4):])
        ws[i] = [0, 255, 0]
        time.sleep_ms(50)
        ws.write()
        time.sleep_ms(10)
        motion.turn_deg(5)
        lcd.clear()
        
    time.sleep_ms(10)
    
    for i in range(8):
        lcd.write(0, 0, text[:(i+5)])
        ws[i] = [255, 0, 0]
        time.sleep_ms(50)
        ws.write()
        time.sleep_ms(10)
        motion.turn_deg(5)
        lcd.clear()
        
    time.sleep_ms(300)
    
    def flashtext(color):
        lcd.write(0, 0, text)
        leds.show_flash(color,1,250,0)
        lcd.clear()
        time.sleep_ms(250)
    
    flashtext([255,0,0])
    flashtext([0,255,0])
    flashtext([0,0,255])

    lcd.write(0, 0, text)
    leds.show_flash([255, 255, 255],3,200,200)
    motion.turn_deg(endspincountdeg)
    clean_and_close('victory')
    
    if shutdown is True:
        ws[0] = [255, 255, 255]  # White
        ws[1] = [255, 0, 0]      # Red
        ws[2] = [0, 255, 0]      # Green
        ws[3] = [0, 0, 255]      # Blue
        ws[4] = [255, 255, 0]    # Yellow
        ws[5] = [0, 255, 255]    # Cyan
        ws[6] = [255, 0, 255]    # Magenta
        ws[7] = [255, 255, 255]  # White
        
        print('Shutting Down')
        lcd.write(0, 0, 'ShuttingDown')
        ws.write()

        for i in range(-1,-9,-1):
            ws[i] = [0,0,0]
            time.sleep_ms(250)
            ws.write()
           
        clean_and_close('Victory Shutdown')
        endprogram()





'''
Credits:
Michael McKenzie
red, blue, green, and finale led shows adapted from shows listed in leds.py (written by Micah Patelli) to be able to have motor movements and lcd visuals inserted in the middle


AI use (Gemini):
    -to learn how to define functions in functions
    -to learn about how to effectively make the robot stop indefinitly using machine.lightsleep()
    -to troubleshoot code when writing code not at school

'''
