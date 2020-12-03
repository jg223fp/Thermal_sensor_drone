#libraries
import lora
import pycom
import time
import ubinascii

#LoRa
# create an OTAA authentication parameters, change them to the provided credentials
app_eui = ubinascii.unhexlify('70B3D57ED00390DD')
app_key = ubinascii.unhexlify('44FC4474848061790EDB15E3689685AB')

#program starts
while True:
    try:
        #exampel values
        vin = 11.31
        temp = 22.45

        if not lora.lora_connected or not lora.lora.has_joined():
            lora.connect_lora(app_eui,app_key)

        elif temp > 75:
            lora.alarm()        #set of alarm if temperature is to high
            print("Alarm!")

        else:
            lora.send_values(temp,vin)   #send 2 floats

        time.sleep(2)     # cant be changed? lora fucks up

    except OSError as er:
        print("Connectivity issue: " + str(er))
        lora.lora_connected = False
        pycom.rgbled(0x050500)      #yellow
    except Exception as ex:
        print("General error: " + str(ex)) # give us some idea on what went wrong
        lora.lora_connected = False
        pycom.rgbled(0x050500)      #yellow
