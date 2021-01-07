#libraries
import machine
import utime
import time
from amg88xx import AMG88XX
from machine import PWM
import voltage_measure
import sounds

#pins
adc = machine.ADC(bits=12)             # create an ADC object
voltage_pin = adc.channel(pin='P18', attn=adc.ATTN_11DB)        # create an analog pin on P18. 11DB to span over 2.198V.
adc.vref(2198)

#set up pin PWM timer for output to alarm buzzer
tim = PWM(0, frequency=0)
sounds.ch = tim.channel(2, pin="P19", duty_cycle=0)

#functions
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

try:
    print("Initiating Thermalsensor drone startup selftest\n")

    #thermalsensor AMG8833 selftest
    print("Testing thermalsensor AMG8833...")
    test_value = read_temperature()
    print("Returned value: ",test_value," C")
    if test_value < 0 or test_value > 130:     # value must be in sensorlimits
        raise Exception
    print("Test completed!")
    time.sleep(1)

    #battery level test
    print("Reading battery voltage...")
    vbat = voltage_measure.vbat_measure(voltage_pin.voltage())       #get new battery voltage value
    print("Battery voltage: ",vbat," V")
    if vbat < 3:                    # 11 V for  battery, 3 V for USB
        raise ValueError
    print("Test completed!")
    time.sleep(1)

    #buzzer test
    print("Testing buzzer...")
    print("Playing tones... If silent: remove battery and check hardware")
    sounds.buzzer_test()
    time.sleep(1)
    print("Test completed!")

    #selftest complete
    time.sleep(1)
    sounds.boot_complete()
    print("\nAll tests completed!")

except ValueError:
        print("The battery level is to low! Remove battery and recharge!")
        while True:
            sounds.error()

except Exception:
        print("Sensor error! The sensor have returned none or an out of range value. Remove battery and check hardware!")
        while True:
            sounds.error()
