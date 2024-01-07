import RPi.GPIO as GPIO
import time
import requests
import threading

#Declare Blynk token
BLYNK_TEMPLATE_ID = "TMPL2inU0PIlo"
BLYNK_TEMPLATE_NAME = "Quickstart Template"
token="GWzg7MKv0UDEAqbQgYLVQsY9DJKzWP0B"

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
''' GPIO Pins ''' 
limit_switch1 = 17
limit_switch2 = 27
limit_switch3 = 5
limit_switch4 = 6
buzz = 23
led1 = 24
led2 = 14
ir1 = 22
ir2 = 26
ir3 = 16 
servo = 25 
sda = 2 
scl = 3


''' Servo Motor Function 
def move_servo(): # Servo Motor Parameters 
    if GPIO.setup(servo,GPIO.OUT) and GPIO.input (limit_switch1) == GPIO.LOW:
	    DUTY_CYCLE_MIN = 1
	    DUTY_CYCLE_MAX = 2
	    p=GPIO.PWM(servo,50) # 50hz frequency
	    p.start(2.5) # starting duty cycle ( it set the servo to 0 degree )
	    p.ChangeDutyCycle(DUTY_CYCLE_MAX)
	    p.ChangeDutyCycle(DUTY_CYCLE_MIN)
	    print("Motor is Running")
    else:
	    print ('NO TRAIN')
'''
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
  

''' Actuators Functions '''
def led_1(state):
    '''
        This function control the red led
    '''    
    if(state):
        GPIO.output(led1, GPIO.HIGH)
    else:
        GPIO.output(led1, GPIO.LOW)

def led_2(state):
    '''
        This function control the green led
    '''    
    if(state):
        GPIO.output(led2, GPIO.HIGH)
    else:
        GPIO.output(led2, GPIO.LOW)

def buzzer(state):
    '''
        This function control the buzzer
    '''
    if(state):
        GPIO.output(buzz, GPIO.HIGH)
    else:
        GPIO.output(buzz, GPIO.LOW)

def init():
    '''
        This function initial the pins and the objects needed
        inside the project
    '''
    #set alarm  and led  to output
    GPIO.setup(buzz,GPIO.OUT,initial = GPIO.LOW)
    GPIO.setup(led1,GPIO.OUT,initial = GPIO.LOW)
    GPIO.setup(led2,GPIO.OUT,initial = GPIO.LOW)
    #GPIO.setup(led2,GPIO.OUT,initial = GPIO.LOW)
    # set motor pins
    GPIO.setup(servo,GPIO.OUT)
    GPIO.setup(limit_switch1,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(limit_switch2,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(limit_switch3,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(limit_switch4,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    

if __name__ == "__main__":
	try:
		while(True):
			'''
    start code here
			''' 
			init()
			#if GPIO.input (limit_switch1) == GPIO.LOW and GPIO.input (limit_switch2) == GPIO.LOW: 
			if GPIO.input (limit_switch1) == GPIO.LOW: 
			   # print("Train Arrived")
			    GPIO.output(led1,GPIO.HIGH)
			    move_servo()
			    write(token,"v0",f"{1}")
			    write(token,"v1",f"{0}")
			    write(token,"v2",f"{1}")
			elif GPIO.input (limit_switch3) == GPIO.LOW:
			    GPIO.output(led1 , GPIO.LOW)
			    GPIO.output(led2 , GPIO.HIGH)
			    move_servo()
			    write(token,"v1",f"{1}")
			    write(token,"v0",f"{0}")
			    write(token,"v2",f"{0}")
			   # print("Train PASS")
			else:
			    print ('OH SHIT')
	finally:
		GPIO.cleanup()			
