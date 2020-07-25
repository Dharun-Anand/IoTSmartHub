#Author: Dharun Anand
#Date: 7/25/20

import RPi.GPIO as GPIO                                           #import the RPi.GPIO module to allow us use the board GPIO pins.
import pyrebase                                                   #import the pyrebase module which allows us to communicate with the firebase servers.
import time                                                       #import the time modulde to allow us do the delay stuff.

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

#Lights setup
lights = 17
GPIO.setup(lights, GPIO.OUT)

def initialize():
    GPIO.output(lights, True)
    database = firebase.database()                                         #take an instance from the firebase database which is pointing to the root directory of your database.
    database.child("IoTHomeSystem1").child("Lights").set("OFF")
        
def lightFunc():
    database = firebase.database()                                         #take an instance from the firebase database which is pointing to the root directory of your database.
    lightStatus = database.child("IoTHomeSystem1").child("Lights").get().val()
    if "off" in lightStatus.lower():                               #If value is off, turn LED off
        print("light status is: " + str(lightStatus))
        GPIO.output(lights, True)
    else:                                                     #If value is not off(implies it's on), turn LED on
        print("light status is: " + str(lightStatus))
        GPIO.output(lights, False)

try:
    initialize()
    while(True):
        lightFunc()
        time.sleep(0.1)
    
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    initialize()
    GPIO.cleanup() # cleanup all GPIO
