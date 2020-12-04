#Author: Dharun Anand
#Date: 7/25/20

import RPi.GPIO as GPIO                                           #import the RPi.GPIO module to allow us use the board GPIO pins.
import pyrebase                                                   #import the pyrebase module which allows us to communicate with the firebase servers.
import time                                                       #import the time modulde to allow us do the delay stuff.
import Adafruit_DHT

config = {                                                        #define a dictionary named config with several key-value pairs that configure the connection to the database.
        "apiKey": "AIzaSyChtlc3MSKgZQ9k2mEHsdPrKkS3gte8t4M",
        "authDomain": "iothomesystem1.firebaseapp.com",
        "databaseURL": "https://iothomesystem1.firebaseio.com/",
        "storageBucket": "iothomesystem1.appspot.com"
}

firebase = pyrebase.initialize_app(config)                        #initialize the communication with the "firebase" servers using the previous config data.

#GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Lights Setup
lights = 17
GPIO.setup(lights, GPIO.OUT)

#Temp & Humidity Sensory Setup
THsensor = Adafruit_DHT.DHT11
THpin = 27

#Motion Detector Setup
pir = 22
GPIO.setup(pir, GPIO.IN) #Setup GPIO pin PIR as input

def initialize():
    GPIO.output(lights, True)
    database = firebase.database()                                         #take an instance from the firebase database which is pointing to the root directory of your database.
    database.child("IoTHomeSystem1").child("System").set("OFF")
    database.child("IoTHomeSystem1").child("Lights").set("OFF")
    database.child("IoTHomeSystem1").child("TH").child("Disp").set("OFF")
    database.child("IoTHomeSystem1").child("TH").child("Temp").set("0.00")
    database.child("IoTHomeSystem1").child("TH").child("Humid").set("0.00")
    database.child("IoTHomeSystem1").child("Motion").set("OFF")
    
def lightFunc():
    database = firebase.database()                                         
    lightStatus = database.child("IoTHomeSystem1").child("Lights").get().val()
    if "off" in lightStatus.lower():                               #If value is off, turn LED off
        #print("light status is: " + str(lightStatus))
        GPIO.output(lights, True)
    else:                                                     #If value is not off(implies it's on), turn LED on
        #print("light status is: " + str(lightStatus))
        GPIO.output(lights, False)

def THFunc():
    database = firebase.database()
    humidity, temperature = Adafruit_DHT.read_retry(THsensor, THpin)
    if humidity is not None and temperature is not None:
        str_temp = ' {0:0.2f}'.format(temperature)
        str_humid  = ' {0:0.2f}'.format(humidity)
        database.child("IoTHomeSystem1").child("TH").child("Temp").set(str_temp)
        database.child("IoTHomeSystem1").child("TH").child("Humid").set(str_humid)
    else:
        #print('Failed to get reading. Try later!')

def pirFunc():
    if GPIO.input(pir) == True: #If PIR pin goes high, motion is detected
        database.child("IoTHomeSystem1").child("Motion").set("ON")
        #print("Motion Detected")
    else:
        database.child("IoTHomeSystem1").child("Motion").set("OFF")

try:
    initialize()
    database = firebase.database() 
    while(True):
        sysStatus = database.child("IoTHomeSystem1").child("System").get().val()
        if "on" in sysStatus.lower():
            lightFunc()
            THFunc()
            pirFunc()
        time.sleep(0.1)
    
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    initialize()
    GPIO.cleanup() # cleanup all GPIO