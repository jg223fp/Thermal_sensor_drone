#libraries
from network import LoRa
import socket
import time
import ubinascii
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
# create an OTAA authentication parameters, change them to the provided credentials
app_eui = ubinascii.unhexlify('70B3D57ED00390DD')
app_key = ubinascii.unhexlify('44FC4474848061790EDB15E3689685AB')


#functions
def connect_lora():
    global lora_connected
    pycom.rgbled(yellow)      #yellow
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
        pycom.rgbled(green)      #green
        lora_connected = True
        time.sleep(0.5)
    except Exception as e:
       print("Couldn't connect to LoRa.",e)


#program starts
while True:
    try:
        #exampel values
        vin = 11.31
        temp = 22.45




        if not lora_connected or not lora.has_joined():
            connect_lora()
            # create a LoRa socket
            s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
            # set the LoRaWAN data rate
            s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
            #remove blocking
            s.setblocking(False)

        elif temp > 75:
            alarm = 1     #must be a payload shorter than length 4 to set of the alarm on TTN. Notice: dont send text!
            s.send(bytes(alarm))
            print("Alarm!")

        else:
            payload = struct.pack(">ff", temp,vin) #encode payload
            s.send(payload)
            print(payload)
            print("Sending payload...")

        time.sleep(2)

    except OSError as er:
        print("Connectivity issue: " + str(er))
        lora_connected = False
        pycom.rgbled(0x050500)      #yellow
    except Exception as ex:
        print("General error: " + str(ex)) # give us some idea on what went wrong
        lora_connected = False
        pycom.rgbled(0x050500)      #yellow
