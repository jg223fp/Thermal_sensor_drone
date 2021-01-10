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
import sounds

#RGB onboard LED colors
pycom.heartbeat(False)
green = 0x000500
yellow = 0x090500
red = 0x050000

#LoRa
#create OTAA authentication parameters, change them to the provided credentials
app_eui = ubinascii.unhexlify('70B3D57ED00390DD')
app_key = ubinascii.unhexlify('44FC4474848061790EDB15E3689685AB')

#global variables
sensor_temp = 0     #The last detected temperature
alarm_temp = 0      #The temperature which triggered the alarm
alarm_active = False

#functions
def read_temperature():
    '''Read temperatures from sensor on I2C bus and set the highest detected temperature to variable highest_pixel_value.'''

    i2c = machine.I2C(1)
    sensor = AMG88XX(i2c)
    try:
        while True:
            highest_pixel_temp = 0
            utime.sleep(0.2)
            sensor.refresh()    #refresh values from all pixels in sensor.
            for row in range(8):
                for col in range(8):
                    if sensor[row, col] > highest_pixel_temp:     #select the highest of the pixel 64 detected temperatures
                         highest_pixel_value = sensor[row, col]
            return highest_pixel_temp

    except Exception as e:
        print("Temperature read error: " + str(e))

def temperature_alarm_thread():
    '''Check highest temperature via read_temperature function and activate alarm if threshold is reached.'''

    global alarm_active
    global sensor_temp
    global alarm_temp
    while True:
        try:
            highest_temp = read_temperature()       #get new value from sensor
            highest_temp = round(highest_temp * 3.75)      #compensation for temperature loss by distance. Multiply value calculated from distance/temp diagram. 150/40=3.75.
            sensor_temp = highest_temp      # updates sensor_temp with new value, highest_temp can't be the value sent beacuse i's resets every cycle
            if highest_temp >= 150:       #activate alarm if temperature is to high
                alarm_temp = highest_temp
                alarm_active = True
                sounds.alarm(20)        # activates alarm sound on drone.
                alarm_active = False

        except Exception as e:
            print("Temperature alarm error:" + str(e))

def lora_thread():
    '''Handles connection to LoRa,reads drone voltage battery and sends data values.'''

    print("\nStarting program...\n")
    while True:
        try:
            vbat = voltage_measure.vbat_measure(voltage_pin.voltage())       #get new battery voltage value

            if not lora.lora_connected:        #if lora isn't connected, connect it.
                lora.connect_lora(app_eui,app_key)
                pycom.rgbled(green)
                sounds.lora_connected()

            elif alarm_active:
                print("Alarm!")
                lora.send_values(alarm_temp,vbat)      #send 2 floats: alarm temperature and voltage

            else:
                lora.send_values(sensor_temp,vbat)      #send 2 floats: sensor temperature and battery voltage

        except OSError as er:
            print("Connectivity issue: " + str(er))
            lora.lora_connected = False
        except Exception as e:
            print("General error: " + str(e))
            lora.lora_connected = False

#program starts
pycom.rgbled(yellow)
_thread.start_new_thread(temperature_alarm_thread, ())      #start temperature sensoring in a thread
_thread.start_new_thread(lora_thread, ())      #start the lora program in a thread
