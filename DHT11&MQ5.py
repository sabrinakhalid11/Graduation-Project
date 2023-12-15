'''
The is the main function that will be called to operate the whole project
The project is about green houses and how to automates it monitoring system
'''
import Adafruit_DHT
import RPi.GPIO as GPIO
import requests
import pyrebase
import time

config = {     
  "apiKey": "AIzaSyBD_tIuFSnDGcCCwv0iDqw7B-Fo-yt_o_U",
  "authDomain": "upgrow-b9789.firebaseapp.com",
  "databaseURL": "https://upgrow-b9789-default-rtdb.firebaseio.com",
  "storageBucket": "upgrow-b9789.appspot.com"
}

#initialize firebase API
firebase = pyrebase.initialize_app(config)
database = firebase.database()

#Declare Blynk token
BLYNK_AUTH_TOKEN = "yu9LfsKQ5yZnwQjGqCK0OXrOXsX8Hn-i"

#Declare last time read for sesnors
#lastRead = 0
dht_pin = 17
mq5_pin = 2
sensor_dht = Adafruit_DHT.DHT11 
GPIO.setmode(GPIO.BCM)
GPIO.setup(mq5_pin,GPIO.IN)
'''------------------------------------------------------------------'''
def WriteBase(data):
    """
        This function push the values of sensors and the system state to firebase
        to make the system send a message in case of any abnormality
    """
    database.child("EHAB").child(data[0]).set(data[1])
    database.child("Store").child(data[0]).push(data[1])

def ReadBase(data):
    """
        This function get the values of control methods from firebase
        to make the system get a message in case of any abnormality
    """
    x=database.child("Monitor").child(data).get()
    return x.val() 

    
def write(token,pin,value):
    '''
        This function updates the data sent to the feed of Blynk
        to show it on the app and website
    '''
    api_url = "https://blynk.cloud/external/api/update?token="+token+"&"+pin+"="+value
    response = requests.get(api_url)
    if "200" in str(response):
	    print("Value successfully updated")
    else:
	    print("Could not find the device token or wrong pin format")

def read(token,pin):
    ''' This function gets data from the Blynk app or website
        to control the system
    '''
    api_url = "https://blynk.cloud/external/api/get?token="+token+"&"+pin
    response = requests.get(api_url)
    return response.content.decode()
'''------------------------------------------------------------------'''
try:
    while True:
	    humidity , temperature = Adafruit_DHT.read_retry(sensor_dht,dht_pin)	
	    mq5_digital_output = GPIO.input(mq5_pin)
	    print(f'mq5 digital output: {mq5_digital_output}')
	    WriteBase(['gas',mq5_digital_output])
	    if humidity is not None and temperature is not None:
		    print('Temp={0}*C Humidity ={1}%'.format(temperature,humidity))
		    WriteBase(['humidity',humidity])
		    WriteBase(['temperature',temperature])
	    else:
		    print("try again")
	    time.sleep(1)
except KeyboardInterrupt:
	print('program end')
'''
if __name__ == "__main__":
   	WriteBase(['gas',mq5_digital_output])
'''
