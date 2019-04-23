#!/usr/bin/python
import os, sys
from wallaby import *

# -- function variables -- #
LM = 2
RM = 0
#TM clockwise = green
TM = 1 
down_position = 0
up_position = 0
open_position = 0
close_position = 0
# high speed and low speed
HS = 90
NS = 60
# turn speed and pivot speed
TS = -10
PS = -90
right_angle = 280
black_threshold = 3980
blue_threshold = 3790
    
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
	#if on black
    if analog(0) >= threshold:
      print("black")
      print(analog(0))
	  #scooch right
      for x in range (0,1):
        motor(RM,-70)
        motor(LM,-40)
    #if on white
    if analog(0) <= threshold:
      print("white")
      print(analog(0))
	  #scooch left
      for x in range (0,1):
        motor(LM,-70)
        motor(RM,-40)

def line_follow_blue(threshold,time):
  for i in range(0,time):
	#if on blue
    if analog(0) >= threshold:
      print("blue")
	  #scooch right
      for x in range (0,1):
        mav(RM,-1000)
        mav(LM,-500)
    #if on white
    if analog(0) <= threshold:
      print("white")
	  #scooch left
      for x in range (0,1):
        mav(LM,-1000)
        mav(RM,-500)
            
def aosleep(ms):
  ao()
  msleep(ms)
      
def main():
  # -------------------------------------program start ------------------------------------- #
         
            
  #turn left 90 degrees
  pivot_left(right_angle)
      
  #scooch
  drive_backwards_slow(1400)
  
  #line follow backwards till button clicked
  print(digital(0))
  while digital(0) == 0:
    line_follow_backwards(black_threshold, 50)
  print(digital(0))
  msleep(1000)
        
  #pivot right towards blue poms
  pivot_right(right_angle)
  msleep(1000)
        
  #scooch towards blue tape
  drive_backwards_slow(100)
        
  #get that bao
  line_follow_blue(blue_threshold, 3400)
        
  #lift things up and put things down
    #move servo to move arm
        
  # -------------------------------------program end ------------------------------------- #



if __name__== "__main__":
    sys.stdout = os.fdopen(sys.stdout.fileno(),"w",0)
    main();