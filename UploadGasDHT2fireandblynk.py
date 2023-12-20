import RPi.GPIO as GPIO
import time
import requests
import pyrebase
import Adafruit_DHT
import requests
''' This Code takes readings from sensors and sent it to firebase and blynk dashboard and mobile app '''
config = {     
  "apiKey": "AIzaSyBD_tIuFSnDGcCCwv0iDqw7B-Fo-yt_o_U",
  "authDomain": "upgrow-b9789.firebaseapp.com",
  "databaseURL": "https://upgrow-b9789-default-rtdb.firebaseio.com",
  "storageBucket": "upgrow-b9789.appspot.com"
}

#initialize firebase API
firebase = pyrebase.initialize_app(config)
database = firebase.database()

#PIN Selection
mq5_pin = 4
dht_pin = 17

# Create DHT11 Object
sensor_dht = Adafruit_DHT.DHT11 

# Setup pins for MQ5 Sensor
GPIO.setmode(GPIO.BCM)
GPIO.setup(mq5_pin,GPIO.IN)

#Declare Blynk token
BLYNK_TEMPLATE_ID = "TMPL2YTgY2665"
BLYNK_TEMPLATE_NAME = "Quickstart Template"
token="_hI1wtLUhYmyiAKrvv8kb7yNiXc_p_NR"

def WriteBase(data):
    """
        This function push the values of sensors and the system state to firebase
        to make the system send a message in case of any abnormality
    """
    database.child("Monitor").child(data[0]).set(data[1])
    database.child("Store").child(data[0]).push(data[1])

def ReadBase(data):
    """
        This function get the values of control methods from firebase
        to make the system get a message in case of any abnormality
    """
    x=database.child("Monitor").child(data).get()
    return x.val()

''' Blynk Send and Update Data Functions '''
def write(token,pin,value):
        api_url = "https://blynk.cloud/external/api/update?token="+token+"&"+pin+"="+value
        response = requests.get(api_url)
        if "200" in str(response):
                print("Value successfully updated")
        else:
                print("Could not find the device token or wrong pin format")
                
def read(token,pin):
        api_url = "https://blynk.cloud/external/api/get?token="+token+"&"+pin
        response = requests.get(api_url)
        return response.content.decode()

""" Sensors Functions """
def ReadGas():
	mq5_digital_output = GPIO.input(mq5_pin)
	print(f'mq5 digital output: {mq5_digital_output}')
	if(mq5_digital_output == 1):
		print("Good")
		WriteBase(['gas',mq5_digital_output])
		WriteBase(['gasrisk','No Risk'])
		write(token,"v0",f"{mq5_digital_output}")
	else:
		print("Bad")
		WriteBase(['gas',mq5_digital_output])
		WriteBase(['gasrisk','Risk'])
		write(token,"v0",f"{mq5_digital_output}")
		
def ReadDHT():
	    humidity , temperature = Adafruit_DHT.read_retry(sensor_dht,dht_pin)
	    if humidity is not None and temperature is not None:
		    print('Temp={0}*C Humidity ={1}%'.format(temperature,humidity))
		    WriteBase(['humidity',humidity])
		    WriteBase(['temperature',temperature])
		    write(token,"v1",f"{temperature}")
		    write(token,"v2",f"{humidity}")
	    else:
		    print("DHT 11 is not Working")
		    
""" Main Loop to Work """
while True:
	ReadGas()
	ReadDHT()
	time.sleep(1)
