#Author: Dharun Anand
#Date: 7/25/20

#import RPi.GPIO as GPIO                                           #import the RPi.GPIO module to allow us use the board GPIO pins.
import pyrebase                                                   #import the pyrebase module which allows us to communicate with the firebase servers.
import time                                                       #import the time modulde to allow us do the delay stuff.

config = {                                                        #define a dictionary named config with several key-value pairs that configure the connection to the database.
        "apiKey": "AIzaSyChtlc3MSKgZQ9k2mEHsdPrKkS3gte8t4M",
        "authDomain": "iothomesystem1.firebaseapp.com",
        "databaseURL": "https://iothomesystem1.firebaseio.com/",
        "storageBucket": "iothomesystem1.appspot.com"
}

firebase = pyrebase.initialize_app(config)                        #initialize the communication with the "firebase" servers using the previous config data.
db = firebase.database()

#GPIO Setup
#GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)

#Lights setup
lights = 17
#GPIO.setup(lights, GPIO.OUT)

def lightFunc():
    database = firebase.database()                                         #take an instance from the firebase database which is pointing to the root directory of your database.
    SmartHub = database.child("IoTHomeSystem1")                        #get the child "RGBControl" path in your database and store it inside the "RGBControlBucket" variable.
    lightStatus = SmartHub.child("Lights").get().val()  #read the light preset mode value from the tag "lightMode" which is a node inside the database then store that value inside the "lightPresetMode" variable.
    print("light status is: " + str(lightStatus))
    #if(lightStatus == "OFF"):                                  #If value is off, turn LED off
        #GPIO.output(lights, False)
    #else:                                                     #If value is not off(implies it's on), turn LED on
        #GPIO.output(lights, True)
        
while(True):
    lightFunc()
    time.sleep(0.1)
    
#except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    #GPIO.cleanup() # cleanup all GPIO