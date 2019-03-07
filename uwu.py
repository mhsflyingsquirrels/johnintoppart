#!/usr/bin/python
import os, sys
from wallaby import *

def main():
  #FUNCTION VARIABLES
  LM = 0
  RM = 1
  TM = 2 #turn motor
  HS = 100
  NS = 80
  TS = -10
  PS = -100
  right_angle = 250
  line_follow_threshold = 50
  
  #PROGRAM START
  #move towards firemen
  drive_forwards_fast(100) #adjust this so the wallaby gets to the point where it can start turning the motor
  off(8) #turns motors off for 5 seconds *i think*

  #move firemen out of pole
  for f in range (5): #for each of the 5 firemen in the pole
    for i in range (0,6): #turn motor then stop 6 times to knock each block out (play with the number of times the effector turns/stops and the power)
      motor(TM,50)
      off(5)
    motor(TM,80) #swing effector back around for the next block



#FUNCTION DEFINITIONS 
def drive_forwards_fast(time):
  i = 0
  while i <= time:
    motor(LM, HS)
    motor(RM,HS)

def drive_forwards_slow(time):
  i = 0
  while i <= time:
    motor(LM,NS)
    motor(RM,NS)

def drive_backwards_fast(time):
  i = 0
  while i <= time:
    motor(LM,-HS)
    motor(RM,-HS)
    
def drive_backwards_slow(time):
  i = 0
  while i <= time:
    motor(LM,-NS)
    motor(RM,-NS)
    
def pivot_left(time):
  i = 0
  while i <= time:
    motor(LM,PS)
    motor(RM,HS)
    
def pivot_right(time):
  i = 0
  while i <= time:
    motor(LM,HS)
    motor(RM,PS)
    
def line_followL(threshold,time):
  i = 0
  while i <= time:
    if analog(0) <= threshold:
      for x in range (0,5):
        motor(LM,100)
        motor(RM,65)
    if analog(0) >= threshold:
      for x in range (0,5):
        motor(RM,100)
        motor(LM,65)
        
def line_followR(threshold,time):
  i = 0
  while i <= time:
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
        
if __name__== "__main__":
    sys.stdout = os.fdopen(sys.stdout.fileno(),"w",0)
    main();