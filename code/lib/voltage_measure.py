
def vbat_measure(vbat_value):
    '''Calculate battery voltage from Vbat_value.'''
    vref = 2.198     #voltage reference. Calculated on 12.52V when battery is 100% charged.
    resolution_12bits = vref/4096       #(2^12 = 4096)
    vin = vbat_value * resolution_12bits
    vbat = vin / (10000/(47000+10000))
    return round(vbat,2)
