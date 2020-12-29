#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 13:46:37 2020

@author: pi
"""

import RPi.GPIO as GPIO
import time
down = False
while 1 == 1:
      GPIO.setmode(GPIO.BOARD)

      PIN_TRIGGER = 22 #25
      PIN_ECHO = 37 #26
#      17,16,13,12
      pin_Red = 12 #18
      pin_Blue = 35 #19
      pin_Green = 38 #20
      #set initial color to magenta\
      GPIO.setup(pin_Red, GPIO.OUT)
      GPIO.setup(pin_Green, GPIO.OUT)
      GPIO.setup(pin_Blue, GPIO.OUT)
      
#      GPIO.output(pin_Red, GPIO.HIGH)
#      GPIO.output(pin_Blue, GPIO.HIGH)
#      GPIO.output(pin_Green, GPIO.LOW)
      
      
      
      ControlPin = [11,36,33,32] 
      
      ##setup pins for motor
      for pin in ControlPin:
          GPIO.setup(pin, GPIO.OUT)
          GPIO.output(pin,0)
          
          
      seq = [[1,0,0,0],
             [1,1,0,0],
             [0,1,0,0],
             [0,1,1,0],
             [0,0,1,0],
             [0,0,1,1],
             [0,0,0,1],
             [1,0,0,1]]      
      reverse_seq = [
              [1,0,0,0],
              [1,0,0,1],
              [0,0,0,1],
              [0,0,1,1],
              [0,0,1,0],
              [0,1,1,0],
              [0,1,0,0],
              [1,1,0,0],                       
              ]
      #pin setup for distance censor
      GPIO.setup(PIN_TRIGGER, GPIO.OUT)
      GPIO.setup(PIN_ECHO, GPIO.IN)

      GPIO.output(PIN_TRIGGER, GPIO.LOW)

      print "Waiting for sensor to settle"

      time.sleep(1.5)

      print "Calculating distance"

      GPIO.output(PIN_TRIGGER, GPIO.HIGH)

      time.sleep(0.00001)

      GPIO.output(PIN_TRIGGER, GPIO.LOW)

      while GPIO.input(PIN_ECHO)==0:
            pulse_start_time = time.time()
      while GPIO.input(PIN_ECHO)==1:
            pulse_end_time = time.time()

      pulse_duration = pulse_end_time - pulse_start_time
      distance = round(pulse_duration * 17150, 2)
      print "Distance:",distance,"cm"
#      
      
      #down
      if ((not down) and distance < 30):
          #set color to magenta 
          GPIO.output(pin_Blue, GPIO.LOW)
          GPIO.output(pin_Red, GPIO.LOW)
          GPIO.output(pin_Green, 1)
          down = True
          for i in range(512) :
              for halfstep in range(8):
                  for pin in range(4):
                      GPIO.output(ControlPin[pin], reverse_seq[halfstep][pin])
                  time.sleep(0.001)
          down = True 
          
          
      #up           
      elif (distance >= 75 and down):
          #set color to cyan 
          GPIO.output(pin_Green, GPIO.LOW)
          GPIO.output(pin_Blue, GPIO.LOW)
          GPIO.output(pin_Red, 1)  
          down = False
          for i in range(512) :
              for halfstep in range(8):
                  for pin in range(4):
                      GPIO.output(ControlPin[pin], seq[halfstep][pin])
                  time.sleep(0.001)
          down = False
                 

      GPIO.cleanup()
 

def turnOff(pin):
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, GPIO.LOW)

