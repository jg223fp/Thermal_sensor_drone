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


#RGB onboardled colors
pycom.heartbeat(False)
green = 0x000500
yellow = 0x090500
red = 0x050000

#pins
adc = machine.ADC(bits=12)             # create an ADC object
voltage_pin = adc.channel(pin='P18', attn=adc.ATTN_11DB)        # create an analog pin on P18. 11DB to span over 2.198V.
adc.vref(2198)

#set up pin PWM timer for output to alarm buzzer
tim = PWM(0, frequency=0)
ch = tim.channel(2, pin="P19", duty_cycle=0)

#LoRa
# create an OTAA authentication parameters, change them to the provided credentials
app_eui = ubinascii.unhexlify('70B3D57ED00390DD')
app_key = ubinascii.unhexlify('44FC4474848061790EDB15E3689685AB')

#variables
sensor_temp = 0
alarm_temp = 0
alarm_active = False

#functions
def alarm_sound():
    while alarm_active:
        tim = PWM(0, frequency=500)
        ch.duty_cycle(0.9)
        time.sleep(0.07)
        ch.duty_cycle(0)
        time.sleep(0.07)
    ch.duty_cycle(0)

def lora_connected_sound():
    tim = PWM(0, frequency=100)
    ch.duty_cycle(0.9)
    time.sleep(0.1)
    ch.duty_cycle(0)
    time.sleep(0.1)
    tim = PWM(0, frequency=5000)
    ch.duty_cycle(0.9)
    time.sleep(0.1)
    ch.duty_cycle(0)
    time.sleep(0.1)
    tim = PWM(0, frequency=50000)
    ch.duty_cycle(0.9)
    time.sleep(0.1)
    ch.duty_cycle(0)

def read_temperature():
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
        return highest_temp

def check_temperature():
    global alarm_active
    global sensor_temp
    global alarm_temp
    while True:
        highest_temp = read_temperature()
        if highest_temp >= 40:
            highest_temp = round(highest_temp * 3.75)      #compensation for temperature loss by distance
        sensor_temp = highest_temp      # updates sensor_temp with new value, highest_temp cant be the value we send beacuse it is reset every cycle
        if highest_temp >= 150 and not alarm_active :       #activate alarm if temperature is to high
            alarm_temp = highest_temp
            alarm_active = True
            _thread.start_new_thread(alarm_sound, ())    #starts alarmsound in a new thread
            _thread.start_new_thread(alarm_timer, ([20]))    # starts a timer in a new thread witch will turn of alarm after x seconds.

def alarm_timer(alarm_time):
    global alarm_active
    start = time.time()
    while alarm_active:
        if time.time() - start > alarm_time:
            alarm_active = False

def main_program():
    print("\nStarting program...\n")
    while True:
        try:
            if not lora.lora_connected:        #if lora isn't connected, connect it.
                lora.connect_lora(app_eui,app_key)
                if lora.lora_connected:        #if lib crash: dont play sound
                    pycom.rgbled(green)
                    lora_connected_sound()

            elif alarm_active:
                print("Alarm!")
                lora.send_values(alarm_temp,vbat)      #send 2 floats: alarm temperature and voltage

            else:
                vbat = voltage_measure.vbat_measure(voltage_pin.voltage())       #get new battery voltage value
                lora.send_values(sensor_temp,vbat)      #send 2 floats: sensor temperature and battery voltage

        except OSError as er:
            print("Connectivity issue: " + str(er))
            lora.lora_connected = False
        except Exception as ex:
            print("General error: " + str(ex))
            lora.lora_connected = False

#program starts
pycom.rgbled(yellow)
_thread.start_new_thread(check_temperature, ())      #start temperature sensoring in a thread
_thread.start_new_thread(main_program, ())      #start the main program in a thread
