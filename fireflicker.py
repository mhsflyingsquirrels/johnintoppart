#!/usr/bin/python
import os, sys
from wallaby import *

#70% battery????????

# -- function variables -- #
<<<<<<< HEAD
LM = 2
RM = 0
#TM clockwise = green
TM = 1 
down_position = 0
up_position = 0
open_position = 0
close_position = 0
=======
LM = 0 
RM = 1
TM = 2 
up_down_SVO = 0
open_close_SVO = 1
down_position = 0 #temporary variable
up_position = 0 #temporary variable
open_position = 0 #temporary variable
close_position = 0 #temporary variable
>>>>>>> e4ad0e86377cc6341f18ec893262cab937188aa9
HS = 100
NS = 80
TS = -10
PS = -100
right_angle = 250
black_threshold = 50
blue_threshold = 30
    
# -- function definitions -- #
def drive_forwards_fast(time):
  for i in range(0,time):
    motor(LM, HS)
    motor(RM,HS)

def drive_forwards_slow(time):
  for i in range(0,time):
    motor(LM,NS)
    motor(RM,NS)

def drive_backwards_fast(time):
  for i in range(0,time):
    motor(LM,-HS)
    motor(RM,-HS)

def drive_backwards_slow(time):
  for i in range(0,time):
    motor(LM,-NS)
    motor(RM,-NS)

def pivot_left(time):
  for i in range(0,time):
    motor(LM,PS)
    motor(RM,HS)

def pivot_right(time):
  for i in range(0,time):
    motor(LM,HS)
    motor(RM,PS)

def line_followL(threshold,time):
  for i in range(0,time):
    if analog(0) <= threshold:
      for x in range (0,5):
        motor(LM,100)
        motor(RM,65)
    if analog(0) >= threshold:
      for x in range (0,5):
        motor(RM,100)
        motor(LM,65)

def line_followR(threshold,time):
  for i in range(0,time):
    if analog(0) <= threshold:
      for x in range (0,5):
        motor(RM,100)
        motor(LM,65)
    if analog(0) >= threshold:
      for x in range (0,5):
        motor(LM,100)
        motor(RM,65)
            
def line_follow_backwards(threshold,time):
  for i in range(0,time):
    if analog(0) <=threshold:
      for x in range(0,5):
        motor(RM, -100)
        motor(LM, -65)
    if analog(0) >= threshold:
      for x in range(0,5):
        motor(LM,-100)
        motor(RM, -65)
 
def aosleep(ms):
  ao()
  msleep(ms)
      
def main():
  # -------------------------------------program start ------------------------------------- #
  
  #drive towards pole
  off(TM)
  drive_forwards_fast(1700) 
  off(RM)
  off(LM)
  msleep(500)
  
  #scooch back
  drive_backwards_slow(10)
  msleep(500)
      
  #turn adjustment
  pivot_right(50)
  off(RM)
  off(LM)
  msleep(500)
      
  #scooch forward
  drive_forwards_fast(200) 
  off(RM)
  off(LM)
  msleep(500)
  
  #turn left adjustment again
  pivot_left(50)
  off(RM)
  off(LM)
  msleep(500)
      
<<<<<<< HEAD
  #scooch a teeny tiny bit forwards -> inconsistent 
  #drive_forwards_fast(5)
      
  #get firefighters out of pole
  for i in range(0,20000):
    print(i)
    motor(TM, -100)
  off(TM)
=======
    #get firefighters out of pole
    for i in range(0,20000):
        print("dab")
        motor(TM, 100)
    off(TM)
        
    #back up
    drive_backwards_fast(100)
    msleep(500)
        
    #turn 90 degrees right (left)
    pivot_left(right_angle)
    msleep(500)

    #scooch forwards (backwards) 
    drive_backwards_fast(100)
    msleep(500)

    #line follow backwards on black until hits wall
    while digital(0) == 0 and digital(1) == 0:
    line_follow_backwards(black_threshold, 5)
    msleep(500)

    #turn right (left) towards blue line
    pivot_left(right_angle)
    msleep(500)
        
    #back up (drive forwards) until hits bulting
    while digital(2) == 0 and digital(3) == 0:
    drive_fowards_slow(5)

    #put down claw opened
    set_servo_position(up_down_SVO, down_position)
    set_servo_position(open_close_SVO, open_position)

    #line follow backwards on blue while scooping blue poms 
    line_follow_backwards(blue_threshold, ARBITRARY)
    msleep(500)
        
    #lift up claw
    set_servo_position(open_close, close_position)
    set_servo_position(up_down_SVO, up_position)

    #turn left (right)
    pivot_right(right_angle/2)
>>>>>>> e4ad0e86377cc6341f18ec893262cab937188aa9
        
  # -------------------------------------program end ------------------------------------- #



if __name__== "__main__":
    sys.stdout = os.fdopen(sys.stdout.fileno(),"w",0)
    main();