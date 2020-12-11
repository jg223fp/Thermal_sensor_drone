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

#pins
adc = machine.ADC()             # create an ADC object
value = adc.channel(pin='P18', attn=adc.ATTN_11DB)        # create an analog pin on P18. 11DB to span over 2.198V.

# set up pin PWM timer for output to buzzer
tim = PWM(0, frequency=0)
ch = tim.channel(2, pin="P19", duty_cycle=0)

#LoRa
# create an OTAA authentication parameters, change them to the provided credentials
app_eui = ubinascii.unhexlify('70B3D57ED00390DD')
app_key = ubinascii.unhexlify('44FC4474848061790EDB15E3689685AB')

#variables
highest_temp = 0
previous_temp = 0

#functions
def alarm_sound():
    while True:
        tim = PWM(0, frequency=500)
        ch.duty_cycle(0.9)
        time.sleep(0.03)
        ch.duty_cycle(0)
        time.sleep(0.05)

def temperature():
    global highest_temp
    global previous_temp
    i2c = machine.I2C(1)
    sensor = AMG88XX(i2c)
    while True:
        highest_temp = 0
        utime.sleep(0.2)
        sensor.refresh()

        for row in range(8):
            for col in range(8):
                if sensor[row, col] > highest_temp:
                     highest_temp = sensor[row, col]

        previous_temp = average_temp # this is

        if highest_temp > 75:
            lora.alarm()        #set of alarm if temperature is to high
            print("Alarm!")
        print(highest_temp)

def main_program():
    while True:
        try:

            if not lora.lora_connected or not lora.lora.has_joined():
                lora.connect_lora(app_eui,app_key)

            else:
                vbat = 11.54 #voltage_measure.vbat(value)
                lora.send_values(prev_temp,vbat)   #send 2 floats
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
_thread.start_new_thread(temperature, ())
_thread.start_new_thread(main_program, ())
