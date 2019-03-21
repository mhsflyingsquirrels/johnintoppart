#!/usr/bin/python
import os, sys
from wallaby import *

# -- function variables -- #
LM = 0
RM = 1
TM = 2 
HS = 100
NS = 80
TS = -10
PS = -100
right_angle = 250
line_follow_threshold = 50
    
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
  for i in range(9,time):
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
      
  #turn adjustment
  pivot_right(50)
  off(RM)
  off(LM)
  msleep(500)
      
  #scooch forward
  drive_forwards_fast(50) 
  off(RM)
  off(LM)
  msleep(500)
  
  #turn left adjustment again
  pivot_left(50)
  off(RM)
  off(LM)
  msleep(500)
      
  #get firefighters out of pole
  for i in range(0,20000):
    print("dab")
    motor(TM, -100)
        
  #back up    
  #turn 90 degrees left
  #scooch forwards (backwards)  
  #line follow backwards on black until hits wall
  #turn right (left) towards blue line
  #put down claw opened
  #line follow backwards on blue while scooping blue poms touch sensor activated
  #back up
  #lift up claw
  #turn left (right)
  #distribute poms
        
        
  
        
        
  # -------------------------------------program end ------------------------------------- #



if __name__== "__main__":
    sys.stdout = os.fdopen(sys.stdout.fileno(),"w",0)
    main();
