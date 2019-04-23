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
right_angle = 293
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
	  #scooch right
      for x in range (0,1):
        motor(RM,-70)
        motor(LM,-40)
    #if on white
    if analog(0) <= threshold:
      print("white")
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
  
  #drive towards pole
  off(TM)
  drive_forwards_fast(1850)
  off(RM)
  off(LM)
  msleep(500)
  
  #scooch back
  drive_backwards_slow(10)
  msleep(500)
      
  #turn adjustment
  pivot_right(49)
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
  for i in range(0,3000):
		print(i)
		motor(TM, -100)
  off(TM)
  msleep(5000)

  #-------------------------------------------------------------------------#
            
  #turn left 90 degrees
  pivot_left(right_angle)
      
  #scooch
  drive_backwards_slow(1400)
  
  #line follow backwards till button clicked
  print(digital(0))
  while digital(0) == 0:
    #line_follow_backwards(black_threshold, 50)
	drive_backwards_slow(50)
  print(digital(0))
  off(RM)
  off(LM)
  msleep(1000)
  
  drive_forwards_slow(130)
  off(RM)
  off(LM)
  msleep(1000)
        
  #pivot right towards blue poms
  pivot_right(right_angle - 120)
  off(RM)
  off(LM)
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



