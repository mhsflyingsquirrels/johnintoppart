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
  # -- program start -- #


  #drive towards pole
  off(TM)
  drive_forwards_fast(2400) 
  off(RM)
  off(LM)
  msleep(200)
      
  #turn adjustment
  pivot_right(30)
  off(RM)
  off(LM)
  msleep(200)
  
  #scooch forwards a little
  drive_forwards_fast(5)
  off(RM)
  off(LM)
  msleep(200)
  
  #get firefighters out of pole
  i = 0
  while i<20000:
    i+=1
    motor(TM, 100)
  
        
        
  # -- program end -- #



if __name__== "__main__":
    sys.stdout = os.fdopen(sys.stdout.fileno(),"w",0)
    main();
