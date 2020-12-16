
def vbat_measure(vbat_voltage):
    '''Calculate battery voltage from Vbat_voltage.'''
    vin = vbat_voltage/1000
    vbat = vin / (10000/(47000+10000))
    return round(vbat,2)
