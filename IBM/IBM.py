# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 13:56:37 2020

@author: SmartBridgePC
"""


import time
import sys
import ibmiotf.application
import ibmiotf.device


#Provide your IBM Watson Device Credentials
organization = "nh1cxn"
deviceType = "SmartWeatherMonitoring"
deviceId = "11111"
authMethod = "token"
authToken = "12345678"

# Initialize GPIO

temp=60
pulse=70
oxygen= 30
lat =  17
lon = 18


def myCommandCallback(cmd):
    print("Command received: %s" % cmd.data['command'])
    print(cmd)
        


try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
	#..............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()

while True:
        #Get Sensor Data from DHT11
        
        data = {"d":{ 'temp' : temp, 'pulse': pulse ,'oxygen': oxygen,"lat":lat,"lon":lon}}
        #print data
        def myOnPublishCallback():
            print ("Published Temperature = %s C" % temp, "Humidity = %s %%" % pulse, "to IBM Watson")

        success = deviceCli.publishEvent("IoTSensor", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
        time.sleep(1)
        
        deviceCli.commandCallback = myCommandCallback

# Disconnect the device and application from the cloud
deviceCli.disconnect()
