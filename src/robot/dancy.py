import motion
import time

def dance_red():
    motion.turn_deg(360, 100)
    motion.turn_deg(-360, 100)
    pass

def dance_green():
    for i in range(10):
        motion.drive_distance_mm(50, 200)
        motion.drive_distance_mm(50, 200, True)
    pass

def dance_blue():
    motion.turn_deg(360, 100)
    motion.turn_deg(360, 100)
    motion.turn_deg(360, 100)
    motion.turn_deg(360, 100)
    motion.turn_deg(360, 100)
    motion.turn_deg(360, 100)
    pass

dance_blue()