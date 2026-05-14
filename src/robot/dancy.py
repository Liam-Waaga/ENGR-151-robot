#import motion
import time
import sensors&leds as sleds

def PANIC():
    '''sos dance'''
    #lcd.write('!!!PANIC!!!')
    for i in range(1):
        color = [255,0,0]
        s = (color,3,60,60)
        o = (color,3,180,180)
        rest = (100) #milliseconds
        
        show_found_red()
        
        sleds.show_flash(*s)
        time.sleep_ms(rest)
        
        sleds.show_flash(*o)
        time.sleep_ms(rest)
        
        sleds.show_flash(*s)
        time.sleep_ms(rest)
        
        time.sleep_ms(rest)

        sleds.show_flash(*s)
        time.sleep_ms(rest)
        
        sleds.show_flash(*o)
        time.sleep_ms(rest)
        
        sleds.show_flash(*s)
        time.sleep_ms(rest)
    pass

def dance_green():
    for i in range(10):
        motion.drive_distance_mm(50, 200)
        motion.drive_distance_mm(50, 200)
    pass

def dance_blue():
    motion.turn_deg(360, 100)
    motion.turn_deg(360, 100)
    motion.turn_deg(360, 100)
    motion.turn_deg(360, 100)
    motion.turn_deg(360, 100)
    motion.turn_deg(360, 100)
    pass

def dance_red():
    motion.turn_deg(360, 200)
    sleds.show_found_red
    motion.turn_deg(-360, 200)
    sleds.show_found_red
    
PANIC()
