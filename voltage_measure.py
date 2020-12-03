#Ska flyttas till main.
'''import machine

adc = machine.ADC()             # create an ADC object
raw_voltage = adc.channel(pin='P18', attn=adc.ATTN_11DB)        # create an analog pin on P13. 11DB to span over 2.1V.
'''
def voltage_measure(value):
    vref = 2.1      #voltage reference.
    resolution_12bits = vref/4096       #(2^12 = 4096)
    Vin = value * resolution_12bits
    Vbat = Vin / (10000/(47000+10000))
    return Vbat
