#!/usr/bin/python
import os, sys
from wallaby import *

#70% battery????????

# -- function variables -- #
LM = 2
RM = 0
#TM clockwise = green
TM = 1 
down_position = 0
up_position = 0
open_position = 0
close_position = 0
HS = 100
NS = 80
TS = -10
PS = -100
right_angle = 250
black_threshold = 3750
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
    for x in range(0,3):
    motor(RM, -100)
        motor(LM, -40)
    if analog(0) >= threshold:
    for x in range(0,3):
    motor(LM,-100)
        motor(RM, -40)
 
def aosleep(ms):
  ao()
  msleep(ms)
      
def main():
  # -------------------------------------program start ------------------------------------- #
        
  #figure out how long to run motor till 
        
  #turn left 90 degrees
  pivot_left(right_angle)
      
  #scooch
  drive_backwards_slow(500)
  
  #line follow backwards
  line_follow_backwards(black_threshold, 500)
   
  #pivot right towards blue poms
  pivot_right(right_angle)
        
  #scooch towards blue tape
  drive_backwards_slow(20)
        
  #get that bao
  line_follow_backwards(blue_threshold, 3400)
        
  #lift things up and put things down
        
  # -------------------------------------program end ------------------------------------- #



if __name__== "__main__":
    sys.stdout = os.fdopen(sys.stdout.fileno(),"w",0)
    main();