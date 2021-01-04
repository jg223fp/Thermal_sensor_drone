#Libraries
import machine
from amg88xx import AMG88XX


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


#Thermalsensor AMG8833 selftest
test_value = read_temperature()
print(test_value)
