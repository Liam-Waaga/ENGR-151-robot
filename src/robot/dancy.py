import motion
import time

def dance_red():
    motion.turn_deg(360)
    motion.turn_deg(-360)
    pass

def dance_green():
    for i in range(36):
        motion.drive_distance_mm(50, 200)
        motion.turn_deg(10, 200)
        motion.drive_distance_mm(50, 200, True)
    pass

def dance_blue():
    pass

dance_green()