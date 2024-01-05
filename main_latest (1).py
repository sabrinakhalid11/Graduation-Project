'''
The is the main function that will be called to operate the whole project
The project is about green houses and how to automates it monitoring system
'''

#Importong GPIO, time, DHT, and Adafruit IO REST client libraries
import RPi.GPIO as GPIO
import time
import Adafruit_DHT
from Adafruit_IO import Client, Feed, RequestError
import requests
import threading
import pyrebase
# import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008


config = {     
  "apiKey": "AIzaSyAc5CIZFiVapWG7b35DRgAJTyIJNwiExzw",
  "authDomain": "iot-greenhouse-9343a.firebaseapp.com",
  "databaseURL": "https://iot-greenhouse-9343a-default-rtdb.firebaseio.com",
  "storageBucket": "iot-greenhouse-9343a.appspot.com"
}


# Software SPI configuration:
CLK  = 18
MISO = 23
MOSI = 24
CS   = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

#initialize firebase API
firebase = pyrebase.initialize_app(config)
database = firebase.database()


# Set to the Adafruit IO key.
ADAFRUIT_IO_KEY = 'aio_cfkp16ctP5tGmpp6IxQr1HZvC86C'

# Set to the Adafruit IO username.
ADAFRUIT_IO_USERNAME = 'ehelsayed'

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)


#set the GPIO modes and neglect warnings
#GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

try: # if we have a 'temperature' feed
    temperature = aio.feeds('temperature')  #Sending the reading of the temperature to the feed
except RequestError: # create a temperature feed
    feed = Feed(name="temperature")
    temperature = aio.create_feed(feed)
    # the created feed will be empty, so with no value aio.receive(temperature.key) will result in 404 error
    # after creating the feed, send an intial value
    aio.send(temperature.key, 0)


try: # if we have a 'humidity' feed
    
    #Sending the reading of the humidity to the feed
    humidity = aio.feeds('humidity')
    
except RequestError: # create a humidity feed
    feed = Feed(name="humidity")
    humidity = aio.create_feed(feed)
    # the created feed will be empty, so with no value aio.receive(humidity.key) will result in 404 error
    # after creating the feed, send an intial value
    aio.send(humidity.key, 0)

    
try: # if we have a 'gas' feed
    #Sending the reading of the gas sensor to the feed
    gas = aio.feeds('gas')
    
except RequestError: # create a gas feed
    feed = Feed(name="gas")
    gas = aio.create_feed(feed)
    # the created feed will be empty, so with no value aio.receive(gas.key) will result in 404 error
    # after creating the feed, send an intial value
    aio.send(gas.key, 0)

try: # if we have a 'Moisture' feed
    #Sending the reading of the soil moisture sensor to the feed
    moisture = aio.feeds('moisture')        
except RequestError: # create a humidity feed
    feed = Feed(name="moisture")
    moisture = aio.create_feed(feed)
    # the created feed will be empty, so with no value aio.receive(humidity.key) will result in 404 error
    # after creating the feed, send an intial value
    aio.send(moisture.key, 0)


#Declare the pins of each I/O
fanIO = 15
pumpIO = 19
dhtIO = 17

# sensor signal pin connected to adc #0
gas = 0
moist=1

#Create DHT11 object
DHT_SENSOR = Adafruit_DHT.DHT11

#Declare sesnor variables
humidityv = 0
temperaturev = 0
gasv = 0
moisturev = 0

#Declare Blynk token
BLYNK_AUTH_TOKEN = "yu9LfsKQ5yZnwQjGqCK0OXrOXsX8Hn-i"

#Declare last time read for sesnors
lastRead = 0


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


def init():
    '''
        This function initial the pins and the objects needed
        inside the project
    '''
    #set gas sesnor and moisture sensor to input
    #GPIO.setup(gas,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
    #GPIO.setup(moist,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)


    #set Fan relay and lamp relay to output
    GPIO.setup(fanIO,GPIO.OUT,initial = GPIO.LOW)
    GPIO.setup(pumpIO,GPIO.OUT,initial = GPIO.LOW)

def readDHT(dhtIO):

    '''
        This function uses adafuit library for the DHT11
        to read the data from the sensor. Then the readings
        will be sent to Adafruit and Blynk
    '''
    global humidityv
    global temperaturev
    humidityv , temperaturev = Adafruit_DHT.read(DHT_SENSOR,dhtIO)
    if humidityv is None and temperaturev is None :
        print("Sensor Failure");
        humidityv = temperaturev = 0
        #return 0,0

    #Sending the reading to Adafruit
    #aio.send(humidity.key, humidityv)
    #aio.send(temperature.key, temperaturev)

    #Sending the reading to FireBase
    WriteBase(['humidity',humidityv])
    WriteBase(['temperature',temperaturev])
    
    #Sending the reading to Blynk
    write(BLYNK_AUTH_TOKEN, 'v0', str(temperaturev)) 
    write(BLYNK_AUTH_TOKEN, 'v1', str(humidityv))
    print("Temp ={0:0.1f}C humditiy={1:0.1f}%".format(temperaturev, humidityv))
    #return humidityv , temperaturev

def pump(state):
    '''
        This function control the pump
    '''
    
    if(state):
        GPIO.output(pumpIO, GPIO.HIGH)
    else:
        GPIO.output(pumpIO, GPIO.LOW)

def fan(state):
    '''
        This function control the fan
    '''
    
    if(state):
        GPIO.output(fanIO, GPIO.HIGH)
    else:
        GPIO.output(fanIO, GPIO.LOW)


def readGas(gasIO):
    '''
        This function read from the gas sensor pin and send the reading
        to the Adafruit and Blynk clouds
    '''
    global gasv
    #Defining the values that will be sent to the platforms
    gasv= mcp.read_adc(gas)
    print("gas level:"+str("%.1f"%(gasv))+"\n")

    
    if(gasv < 160):
        #gasv = 1
        gass = "Normal"
        WriteBase(['gasrisk',0])
    else:
        #gasv = 0
        gass = "Bad Gases"
        WriteBase(['gasrisk',1])
        
    #Send the reading to Adafruit, Firebase, and Blynk
    WriteBase(['gas',gasv])
    #aio.send(gas.key, gasv) 
    write(BLYNK_AUTH_TOKEN, 'v3',gass)
    write(BLYNK_AUTH_TOKEN, 'v7',str(gasv))
    #print("Gas (in PPM) =",gasv)
    #return gasv


def readMoist(moistIO):
    '''
        This function read from the Moisture sensor pin and send
        the reading to the Adafruit and Blynk clouds
    '''
    global moisturev
    #Defining the values that will be sent to the platforms
    moisturev= mcp.read_adc(moist)
    moisturev = 100 - moisturev*100/1024
    print("Moisture level:"+str("%.1f"%(moisturev))+"%\n")
    if(moisturev < 20):
        #moisturev = 1
        moistures = "Dry Soil"
        WriteBase(['moistrisk',1])
    else:
        #moisturev = 0
        moistures = "Hydrated Soil"
        WriteBase(['moistrisk',0])
        
    #Send the reading to Adafruit, Firebase, and Blynk
    WriteBase(['moist',moisturev])
    #aio.send(moisture.key, moisturev)
    write(BLYNK_AUTH_TOKEN, 'v4', moistures)
    write(BLYNK_AUTH_TOKEN, 'v8', str(moisturev))
    #print("Moist (%) = ", moisturev)
    #return moisturev


def Threading():
    '''
        This function is responsible for start the threading rotine
        for sensor reading 
    '''

    #Create Sensor reading threads
    gasThread = threading.Thread(target=readGas, args=(gas,))
    DHTThread = threading.Thread(target=readDHT, args=(dhtIO,))
    MoistThread = threading.Thread(target=readMoist, args=(moist,))
    
    #Start the threads of Gas, DHT11 ,and Moisture sensor
    gasThread.start()
    DHTThread.start()
    MoistThread.start()

    #Wait the thread till they are done 
    gasThread.join()
    DHTThread.join()
    MoistThread.join()



if __name__ == "__main__":

    try:
        #call init() function to initialize all the pins as I/O
        init()
    
        while(True):
            
            #time interval condition to read sensors each 30 seconds 
            if(time.time() - lastRead > 5):
                
                #call the function to check sensors using threads
                Threading()
                
                #save the last time the sensors was read
                lastRead = time.time()
                
            #Retrieve the values of switches from Blynk (Auto, Fan, and Pump) respectively
            Auto = read(BLYNK_AUTH_TOKEN,'v2')
            Fanstat =read(BLYNK_AUTH_TOKEN,'v5')
            Pumpstat = read(BLYNK_AUTH_TOKEN,'v6')
            Auto = ReadBase('auto') if Auto == '1' else Auto
            Fanstat =ReadBase('fan') if Fanstat == '0' else Fanstat
            Pumpstat = ReadBase('pump') if Pumpstat == '0'  else Pumpstat
            
            #Debug the values of switches
            print("Auto = ", Auto)
            print("Fan = ", Fanstat)
            print("Pump = ", Pumpstat)

            #Check if the system in Blynk is Automated
            if(Auto =='1'):
                
                #Apply the condition to control fan
                #(humidityv > 60 or temperaturev >30 or gas read a problem)
                fan(True if humidityv > 60 or temperaturev >30 or gasv >= 160 else False )

                #give the pump function reads of moisture sensor to control it
                pump(moisturev<20)

            #otherwise (manual), control the system based on the switches from Blynk
            else:

                #control fan based on fanstat value
                fan(True if Fanstat =='1' else False)

                #control pump based on pumpstat value
                pump(True if Pumpstat =='1' else False)
    finally:
        GPIO.cleanup()
