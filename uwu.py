#!/usr/bin/python
import os, sys
from wallaby import *

def main():
  # -- function variables -- #
  LM = 0
  RM = 1
  TM = 2 #turn motor
  HS = 100
  NS = 80
  TS = -10
  PS = -100
  right_angle = 250
  line_follow_threshold = 50

  # -- program start -- #
  
  i = 0
  while i<20000:
    i+=1
    motor(TM, 100)
  aosleep(10000)


# -- function definitions -- #
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
