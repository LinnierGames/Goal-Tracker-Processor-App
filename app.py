import paho.mqtt.client as mqtt
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# import RPi.GPIO as GPIO, time
# from gpiozero import DigitalOutputDevice

# fp_toggle_power_pin = DigitalOutputDevice(26)
# base2 = DigitalOutputDevice(6)
# base3 = DigitalOutputDevice(13)
# base4 = DigitalOutputDevice(5)

MQTT_SERVER = "localhost"
MQTT_PATH = "fireplace/#"

REMOTE_STORE_API_KEY = os.getenv('KEY')

# def fireplace_toggle_power():
#     fp_toggle_power_pin.on()
#     time.sleep(0.5)
#     fp_toggle_power_pin.off()
#     time.sleep(0.5)
 
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    client.subscribe("goals/new-data")
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic)
    print(msg.payload)
    
    if msg.topic == "goals/new-data":
        print("Got message for goals/new-data")

        print("Start papermill")
        os.system('(cd /Users/ericksmicrowave/Documents/Habits/Notebooks && papermill _3_Dashboard.ipynb /dev/null)')
        # os.system('papermill _3_Dashboard.ipynb /dev/null')
        print("Finish papermill")

        url = 'http://localhost:3000/reports'
        files = {'report': open('/Users/ericksmicrowave/Documents/Habits/Reports/Report-Grade 2022-03-16.pdf', 'rb')}

        print("Start uploading pdf")
        r = requests.post(url, files=files, headers={ 'key': REMOTE_STORE_API_KEY })
        print(r)
        print("Finish uploading pdf")
        
    #     payload_str = str(msg.payload.decode("utf-8"))
        
    #     if payload_str == "toggle-power":
    #         print("Toggle Power")
    #         fireplace_toggle_power()


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
 
client.connect(MQTT_SERVER, 1883, 60)
 
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
