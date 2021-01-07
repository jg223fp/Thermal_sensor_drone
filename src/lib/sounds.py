from machine import PWM
import time

# set up pin PWM timer for output to alarm buzzer in boot file
# with this line: sounds.ch = tim.channel(2, pin="P##", duty_cycle=0)

def alarm(duration):
    alarm_start = time.time()
    while time.time() - alarm_start < duration:
        tim = PWM(0, frequency=500)
        ch.duty_cycle(0.9)
        time.sleep(0.07)
        ch.duty_cycle(0)
        time.sleep(0.07)
    ch.duty_cycle(0)

def lora_connected():
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

def error():
    tim = PWM(0, frequency=100)
    ch.duty_cycle(0.5)
    time.sleep(0.5)
    ch.duty_cycle(0)
    time.sleep(0.5)

def boot_complete():
        tim = PWM(0, frequency=10000)
        ch.duty_cycle(0.7)
        time.sleep(0.1)
        ch.duty_cycle(0)
        time.sleep(0.1)
        tim = PWM(0, frequency=10000)
        ch.duty_cycle(0.7)
        time.sleep(0.1)
        ch.duty_cycle(0)
        time.sleep(0.1)

def buzzer_test():
    hertz = [100,300,1000,2000,3000,4000,10000]
    for hz in hertz:
        tim = PWM(0, frequency=hz)
        ch.duty_cycle(0.7)
        time.sleep(0.1)
        ch.duty_cycle(0)
        time.sleep(0.1)
