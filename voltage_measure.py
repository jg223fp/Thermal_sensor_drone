#Ska flyttas till main.
'''import machine

adc = machine.ADC()             # create an ADC object
raw_voltage = adc.channel(pin='P13', attn=adc.ATTN_11DB)        # create an analog pin on P13. 11DB to span over 2.1V.
'''
def voltage_measure(raw_voltage):
    vref = 2.1      #voltage reference.
    resolution_12bits = vref/4096       #(2^12 = 4096)
    return raw_voltage * resolution_12bits
    
