#Ska flyttas till main.
'''import machine

adc = machine.ADC()             # create an ADC object
value = adc.channel(pin='P18', attn=adc.ATTN_11DB)        # create an analog pin on P13. 11DB to span over 2.198V.
'''
def voltage_measure(value):
    vref = 2.198     #voltage reference. Calculated on 12.52V when battery is 100% charged.
    resolution_12bits = vref/4096       #(2^12 = 4096)
    Vin = value * resolution_12bits
    Vbat = Vin / (10000/(47000+10000))
    return Vbat
