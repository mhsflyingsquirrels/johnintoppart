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
HS = 90
NS = 60
TS = -10
PS = -90
right_angle = 250
black_threshold = 3900
blue_threshold = 3600
    
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
        motor(LM,90)
        motor(RM,65)
    if analog(0) >= threshold:
      for x in range (0,5):
        motor(RM,90)
        motor(LM,65)

def line_followR(threshold,time):
  for i in range(0,time):
    if analog(0) >= threshold:
      for x in range (0,5):
        motor(RM,90)
        motor(LM,10)
    if analog(0) <= threshold:
      for x in range (0,5):
        motor(LM,90)
        motor(RM,10)

#line follows on right
def line_follow_backwards(threshold,time):
  for i in range(0,time):
    if analog(0) <= threshold:
      for x in range (0,2):
        mav(LM,-1000)
        mav(RM,-700)
    if analog(0) >= threshold:
      for x in range (0,2):
        mav(RM,-1000)
        mav(LM,-500)
 
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
  
  #get firefighters out of pole
  for i in range(0,20000):
      print("dab")
      motor(TM, -100)
  off(TM)
  msleep(500)
      
            
  #--------figure out how long to run motor till --------**************
       
  #back up
  drive_backwards_fast(100)
  msleep(500)
            
  #turn left 90 degrees
  pivot_left(right_angle)
      
  #scooch
  drive_backwards_slow(700)
  
  #line follow backwards till button clicked
  print(digital(0))
  while digital(0) == 0:
    line_follow_backwards(black_threshold, 100)
  print(digital(0))
  msleep(1000)
        
  #pivot right towards blue poms
  pivot_right(right_angle)
  msleep(1000)
        
  #scooch towards blue tape
  drive_backwards_slow(300)
        
  #get that bao
  line_follow_backwards(blue_threshold, 3400)
        
  #lift things up and put things down
        
  # -------------------------------------program end ------------------------------------- #



if __name__== "__main__":
    sys.stdout = os.fdopen(sys.stdout.fileno(),"w",0)
    main();