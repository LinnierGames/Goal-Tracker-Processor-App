import paho.mqtt.client as mqtt
import requests
import os
from dotenv import load_dotenv

load_dotenv()

MQTT_SERVER = "localhost"

REMOTE_STORE_API_KEY = os.getenv('KEY')
 
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
        most_recent_report_filepath = most_recent_report_filepath()
        files = {'report': open(most_recent_report_filepath, 'rb')}

        print("Start uploading pdf", most_recent_report_filepath)
        r = requests.post(url, files=files, headers={ 'key': REMOTE_STORE_API_KEY })
        print(r)
        print("Finish uploading pdf")

import glob
import os

def most_recent_report_filepath():
    dir_name = '/Users/ericksmicrowave/Documents/Habits/Reports/'
    # Get list of all files only in the given directory
    list_of_files = filter( os.path.isfile,
                            glob.glob(dir_name + '*') )
    # Sort list of files based on last modification time in ascending order
    list_of_files = sorted( list_of_files,
                            key = os.path.getmtime)

    most_recent_report = list_of_files[-1]

    return most_recent_report

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
 
client.connect(MQTT_SERVER, 1883, 60)
 
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
