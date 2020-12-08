#libraries
import lora
import pycom
import time
import ubinascii
import machine
import voltage_measure
from amg88xx import AMG88XX
import machine
import utime
import _thread

adc = machine.ADC()             # create an ADC object
value = adc.channel(pin='P18', attn=adc.ATTN_11DB)        # create an analog pin on P18. 11DB to span over 2.198V.

#LoRa
# create an OTAA authentication parameters, change them to the provided credentials
app_eui = ubinascii.unhexlify('70B3D57ED00390DD')
app_key = ubinascii.unhexlify('44FC4474848061790EDB15E3689685AB')


#variables
highest_temp = 0


def temperature():
    global highest_temp
    i2c = machine.I2C(1)
    sensor = AMG88XX(i2c)
    while True:

        utime.sleep(0.2)
        sensor.refresh()

        for row in range(8):
            for col in range(8):
                 if sensor[row, col] > highest_temp:
                     highest_temp = sensor[row, col]
        if highest_temp > 75:
            lora.alarm()        #set of alarm if temperature is to high
            print("Alarm!")
        print(highest_temp)



def main_program():
    while True:
        try:
            Vbat = 11.54# voltage_measure.Vbat(value)

            if not lora.lora_connected or not lora.lora.has_joined():
                lora.connect_lora(app_eui,app_key)

            else:
                lora.send_values(highest_temp,Vbat)   #send 2 floats
                time.sleep(5)       # just for testing, remove when shit get real

            time.sleep(2)     # cant be changed? lora fucks up

        except OSError as er:
            print("Connectivity issue: " + str(er))
            lora.lora_connected = False
            pycom.rgbled(0x050500)      #yellow
        except Exception as ex:
            print("General error: " + str(ex)) # give us some idea on what went wrong
            lora.lora_connected = False
            pycom.rgbled(0x050500)      #yellow

#program starts
print("ost")
_thread.start_new_thread(temperature)
_thread.start_new_thread(main_program)
