#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 13:28:31 2021

@author: pi
"""
aantal = 0          # begint met waarde 0 voor de schijven 1,2,3
lichtsluis1= 21
lichtsluis2= 20
motor1= 23
motor2= 22
roodknop= 27
roodlamp= 17
groenknop= 25
groenlamp= 24

import RPi.GPIO as GPIO
import time  
#import csv
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.IN)  #rechter lichtsluis  (2)
GPIO.setup(21, GPIO.IN)  # linker lichtsluis    (1)
GPIO.setup(22, GPIO.OUT)  # rechter draaischijg( met de buizen )    (2)
GPIO.setup(23, GPIO.OUT) # linker draaischijf( waar magneet ingaat)  (1)
GPIO.setup(17, GPIO.OUT) #lampje rood
GPIO.setup(27, GPIO.IN) #lampje roodknop
GPIO.setup(24, GPIO.OUT) #lampje groen
GPIO.setup(25, GPIO.IN) #lampje groenknop
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn







def Lichtsluis1():                      
    if GPIO.input(lichtsluis1):
        print (" lichtsluis 1")
        time.sleep(0.1)


def Lichtsluis2():
    if GPIO.input(lichtsluis1):
        print (" lichtsluis 1")
        time.sleep(0.1)



def nulpunt1():
    print('nulpunt zoeken1')
    for i in range(500):            #500 stappen maken 
        if GPIO.input(roodknop):
            print("stop")                   
            break                   #verbreekt definition als roodknop true is
        GPIO.output(motor1, True)
        time.sleep(0.0007)
        GPIO.output(motor1, False)
        time.sleep(0.0007) 

    while GPIO.input(lichtsluis1) == GPIO.LOW:#draait tot lichtsluis true wordt
        if GPIO.input(roodknop):
            print("stop")
            break
        GPIO.output(motor1, True)
        time.sleep(0.0006)
        GPIO.output(motor1, False)
        time.sleep(0.0006)
        
    for i in range(230):         #230 stappen erbij wanneer lichtsluis true is
        GPIO.output(motor1, True)
        time.sleep(0.0006)
        GPIO.output(motor1, False)
        time.sleep(0.0006) 
        
        
def nulpunt2():
    print('nulpunt zoeken2')
    for i in range(250):
        if GPIO.input(roodknop):
            print("stop2")
            break
        GPIO.output(motor2, True)
        time.sleep(0.0005)
        GPIO.output(motor2, False)
        time.sleep(0.0005) 

    while GPIO.input(lichtsluis2) == GPIO.LOW:
        if GPIO.input(roodknop):
            print("stop")
            break
        GPIO.output(motor2, True)
        time.sleep(0.0005)
        GPIO.output(motor2, False)
        time.sleep(0.0005)
        
    for i in range(230):
        if GPIO.input(roodknop):
            print("stop")
            break
        GPIO.output(motor2, True)
        time.sleep(0.0005)
        GPIO.output(motor2, False)
        time.sleep(0.0005) 

def nulpunt2schijf7():  #dit word gebruikt wanneer het na schijf 7 moet nullen
    while GPIO.input(lichtsluis2) == GPIO.LOW:
        if GPIO.input(roodknop):
            print("stop")
            break
        GPIO.output(motor2, True)
        time.sleep(0.0005)
        GPIO.output(motor2, False)
        time.sleep(0.0005)
        
    for i in range(230):
        if GPIO.input(roodknop):
            print("stop")
            break
        GPIO.output(motor2, True)
        time.sleep(0.0005)
        GPIO.output(motor2, False)
        time.sleep(0.0005)    
       
        
def draaivoorsensor():
    RotationPosition = 0 
    print("draaien naar de sensor toe")
    while RotationPosition < 2050 :         #3200 hele rondje
        if GPIO.input(roodknop):
            print("stop")
            break
        RotationPosition = RotationPosition + 1     
        GPIO.output(motor1, True)
        time.sleep(0.0002)
        GPIO.output(motor1, False)
        time.sleep(0.0002)
        


        
        
        
def magneeteruitsnel():
    RotationPosition = 0
    print("magneet gaat eruit en gaat naar nulpunt")
    while RotationPosition < 1000:      #maakt 1000 stappen om weer terug 
        if GPIO.input(roodknop):        #te gaan naar nulpunt 
            print("stop")
            break
        RotationPosition += 1 #betekent RotationPosition = RotationPosition + 1 
        GPIO.output(motor1, True)
        time.sleep(0.001)
        GPIO.output(motor1, False)
        time.sleep(0.001)
    


    
def sensormeting():             #meting hallsensor met ADC
    global aap
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1015(i2c)
    ads.gain = 1
    values=0
    chan = AnalogIn(ads, ADS.P0)
    values = chan.voltage,values
   # print(values) hoeft niet
    time.sleep(0.01)
    aap = values
    
        


def draaitotsensor():       #na elk stap word er een meting gedaan
    RotationPosition = 0
    LastMaxValue = 0
    while RotationPosition < 150:
        if GPIO.input(roodknop):
            print("stop")
            break
        RotationPosition = RotationPosition + 1
        GPIO.output(motor1, True)
        time.sleep(0.01)
        GPIO.output(motor1, False)
        time.sleep(0.01)
        sensormeting()
        if GPIO.input(roodknop):
            print("stop")
            break
        #print(aap)
        if max(aap) > LastMaxValue:         
            global MaxValue
            MaxValue = max(aap)
            LastMaxValue = MaxValue
    print("hierkomt de maxvalue")
    print(MaxValue)                 # max waarde in volt

def webers():
    global MaxValue
    x =  MaxValue - 0.2516
    y=x/0.0215
    print(round(y)) 
    return round(y)
    
    
        
def excel():
    global MaxValue
    global y
    global x
    f= open("hoi.csv", "a" ) 
    f.write(str(webers()) + "\n")

    f.close()

 
    
def schijf1():
    global aantal
    if aantal > 55:          # aanpassen naar aantal magnete in 1 buis tot schijf 3
        schijf2()
        return   
    RotationPosition = 0
    LastMaxValue = 130                  #aan te passen cijfer
    global MaxValue
    x =  MaxValue - 0.2516
    y=x/0.0215
    print(round(y))             # maxvalue in V omgezet in webers met afronding
    if y > LastMaxValue and y < 160:    #aan te passen cijfer
        print("goed1")
        aantal += 1
        while RotationPosition < 400:   #aantal stappen voor buis= 1/8 van 3200
            #print("bezig met schijf1")
            if GPIO.input(roodknop):
                print("stop")
                break
            RotationPosition = RotationPosition + 1
            GPIO.output(motor2, True)
            time.sleep(0.0005)
            GPIO.output(motor2, False)
            time.sleep(0.0005)   
      
 
def schijf2():
    global aantal
    if aantal > 110:
        schijf3()
        return
    RotationPosition = 0
    LastMaxValue = 130
    global MaxValue
    x =  MaxValue - 0.2516
    y=x/0.0215
    print(round(y)) 
    if y > LastMaxValue and y < 160:
        print("goed2")
        aantal +=1
        while RotationPosition < 800:
            if GPIO.input(roodknop):
                print("stop")
                break
            RotationPosition = RotationPosition + 1
            GPIO.output(motor2, True)
            time.sleep(0.0005)
            GPIO.output(motor2, False)
            time.sleep(0.0005)   
     
        
        
def schijf3():
    global aantal
    if aantal > 200:
        return 1
    RotationPosition = 0
    LastMaxValue = 130
    global MaxValue
    x =  MaxValue - 0.2516
    y=x/0.0215
    print(round(y)) 
    if y > LastMaxValue and y < 160:
        print("goed3")
        aantal +=1
        while RotationPosition < 1200:
            if GPIO.input(roodknop):
                print("stop")
                break
            RotationPosition = RotationPosition + 1
            GPIO.output(motor2, True)
            time.sleep(0.0005)
            GPIO.output(motor2, False)
            time.sleep(0.0005)   
    
def schijf4():
    RotationPosition = 0
    LastMaxValue = 120
    global MaxValue
    x =  MaxValue - 0.2516
    y=x/0.0215
    print(round(y)) 
    if y > LastMaxValue and y < 130:
        print("afkeur120 tot 130")
        while RotationPosition < 1600:
            if GPIO.input(roodknop):
                print("stop")
                break
            RotationPosition = RotationPosition + 1
            GPIO.output(motor2, True)
            time.sleep(0.0005)
            GPIO.output(motor2, False)
            time.sleep(0.0005)   
        
        
        
def schijf5():
    RotationPosition = 0
    LastMaxValue = 100
    global MaxValue
    x =  MaxValue - 0.2516
    y=x/0.0215
    print(round(y)) 
    if y > LastMaxValue and y < 120:
        print("afkeur100 tot 120")
        while RotationPosition < 2000:
            if GPIO.input(roodknop):
                print("stop")
                break
            RotationPosition = RotationPosition + 1
            GPIO.output(motor2, True)
            time.sleep(0.0005)
            GPIO.output(motor2, False)
            time.sleep(0.0005)   
     
        
def schijf6():
    RotationPosition = 0
    LastMaxValue = 60
    global MaxValue
    x =  MaxValue - 0.2516
    y=x/0.0215
    print(round(y)) 
    if y > LastMaxValue and y < 100:
        print("afkeur 60 tot 100")
        while RotationPosition < 2400:
            if GPIO.input(roodknop):
                print("stop")
                break
            RotationPosition = RotationPosition + 1
            GPIO.output(motor2, True)
            time.sleep(0.0005)
            GPIO.output(motor2, False)
            time.sleep(0.0005)   
        
        
        
        
def schijf7():
    RotationPosition = 0
    LastMaxValue = 0
    global MaxValue
    x =  MaxValue - 0.2516
    y=x/0.0215
    print(round(y)) 
    if y > LastMaxValue and y < 60:
        print("afkeur tot 60")
        while RotationPosition < 2800:
            if GPIO.input(roodknop):
                print("stop")
                break
            RotationPosition = RotationPosition + 1
            GPIO.output(motor2, True)
            time.sleep(0.0005)
            GPIO.output(motor2, False)
            time.sleep(0.0005)   
        magneeteruitsnel()
        nulpunt2schijf7()
        GPIO.output(groenlamp, True)
        GPIO.output(roodlamp, False)
        return True
    return False  


    
def werking():
    global aantal           #voor schijven 1,2,3
    while True:
        if GPIO.input(roodknop):
            print("stop")
            break
        draaivoorsensor()
        if GPIO.input(roodknop):
            print("stop")
            break
        print("meting sensor")
        if GPIO.input(roodknop):
            print("stop")
            break
        draaitotsensor()
        excel()
        if GPIO.input(roodknop):
            print("stop")
            break
        print("schijf 2 draait naar zn positie")
        if GPIO.input(roodknop):
            print("stop")
            break
        schijf1()
        if aantal > 200:          #dus als de 3 schijven vol zitten stop
            nulpunt2()
            nulpunt1()
            break
        if GPIO.input(roodknop):
            print("stop")
            break
        #schijf2()
        if GPIO.input(roodknop):
            print("stop")
            break
        #schijf3()
        if GPIO.input(roodknop):
            print("stop")
            break
        schijf4()
        if GPIO.input(roodknop):
            print("stop")
            break
        schijf5()
        if GPIO.input(roodknop):
            print("stop")
            break
        schijf6()
        if GPIO.input(roodknop):
            print("stop")
            break
        if schijf7():
            print(" stop en druk reset")
            break
        magneeteruitsnel()
        nulpunt2()
        

    


GPIO.output(groenlamp, False)
GPIO.output(roodlamp, True)
nulpunt2()
nulpunt2()
nulpunt1()
nulpunt1()
GPIO.output(groenlamp, True)
GPIO.output(roodlamp, False) #werking wanneer het programma start
while True:
    if GPIO.input(groenknop):       #startknop
        GPIO.output(groenlamp, False)
        GPIO.output(roodlamp, True)
        werking()
        
    if GPIO.input(roodknop):        #stopknop
        time.sleep(0.5)
        nulpunt2()
        nulpunt1()
        GPIO.output(groenlamp, True)
        GPIO.output(roodlamp, False)
       