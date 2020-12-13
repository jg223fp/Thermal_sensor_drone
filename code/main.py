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
from machine import Pin
from machine import PWM

#pins
adc = machine.ADC()             # create an ADC object
voltage_pin = adc.channel(pin='P18', attn=adc.ATTN_11DB)        # create an analog pin on P18. 11DB to span over 2.198V.

#set up pin PWM timer for output to alarm buzzer
tim = PWM(0, frequency=0)
ch = tim.channel(2, pin="P19", duty_cycle=0)

#LoRa
# create an OTAA authentication parameters, change them to the provided credentials
app_eui = ubinascii.unhexlify('70B3D57ED00390DD')
app_key = ubinascii.unhexlify('44FC4474848061790EDB15E3689685AB')

#variables
sensor_temp = 0
alarm_active = False

#functions
def alarm_sound():
    while True:
        tim = PWM(0, frequency=500)
        ch.duty_cycle(0.9)
        time.sleep(0.07)
        ch.duty_cycle(0)
        time.sleep(0.07)

def read_temperature():
    global alarm_active
    global sensor_temp
    i2c = machine.I2C(1)
    sensor = AMG88XX(i2c)
    while True:
        highest_temp = 0
        utime.sleep(0.2)
        sensor.refresh()
        for row in range(8):
            for col in range(8):
                if sensor[row, col] > highest_temp:     #select the highest of the sensors 64 detected temperatures
                     highest_temp = sensor[row, col]

        sensor_temp = highest_temp # updates sensor_temp with new value, highest_temp cant be the value we send beacuse it is reset every cycle

        if highest_temp > 75 :       #set of alarm if temperature is to high
            alarm_active = True

        print(highest_temp)

def main_program():
    #global lora.lora_connected
    while True:
        try:
            if not lora.lora_connected or not lora.lora.has_joined():       #if lora is´nt connected, connect it.
                lora.connect_lora(app_eui,app_key)


            elif alarm_active:
                print("Alarm!")
                _thread.start_new_thread(alarm_sound, ())    #starts alarmsound
                while True:          # sends alarm messeges by LoRa
                    lora.alarm()
                    time.sleep(2)

            else:
                vbat = voltage_measure.vbat_measure(voltage_pin.value())       #get new battery voltage value
                lora.send_values(sensor_temp,vbat)      #send 2 floats
                time.sleep(5)       # just for testing, remove when shit get real

            time.sleep(2)     # cant be changed? lora breaks

        except OSError as er:
            print("Connectivity issue: " + str(er))
            lora.lora_connected = False
        except Exception as ex:
            print("General error: " + str(ex))
            lora.lora_connected = False

#program starts
_thread.start_new_thread(read_temperature, ())      #start temperature sensoring in a thread
_thread.start_new_thread(main_program, ())      #start the main program in a thread
