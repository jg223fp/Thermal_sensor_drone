#libraries
from network import LoRa
import socket
import time
import pycom
import struct

#variables
lora_connected = False

#RGB onboardled colors
pycom.heartbeat(False)
green = 0x000500
yellow = 0x090500
red = 0x050000

#LoRa
# Initialise LoRa in LORAWAN mode.
# Europe = LoRa.EU868
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

#functions
def connect_lora(app_eui,app_key):
    global lora_connected
    global s
    pycom.rgbled(yellow)
    count = 0
    try:
        while not lora.has_joined():                #reconnect 3 times else raise error
            print("Trying to connect to LoRa...")
            count += 1
            lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)   # join a network using OTAA (Over the Air Activation)
            time.sleep(3)
            if count == 3:
                raise Exception("")

        print("\nConnected to LoRa\n")
        pycom.rgbled(green)
        lora_connected = True
        s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)      # create a LoRa socket
        s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)      # set the LoRaWAN data rate
        s.setblocking(False)        #remove blocking
        time.sleep(0.5)
    except Exception as e:
       print("Couldn't connect to LoRa.",e)

def alarm():
            alarm = 1     #must be a payload shorter than length 4 to set of the alarm on TTN. Notice: dont send text!
            s.send(bytes(alarm))        #encode payload and send
            print("Sending alarm messege!")

def send_values(temp,vbat):
    payload = struct.pack(">ff", temp,vbat)     #encode payload
    s.send(payload)     #send payload
    print("Sending payload...")
