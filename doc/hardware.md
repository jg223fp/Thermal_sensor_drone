# Hardware
## Components list
|Component  | Quantity   |Price |
|:----:|:------------- |:---------------|
|Cheerson CX-20 drone|1|2990 SEK
|Pycom expansionboard 3.1|1|189 SEK
|Pycom Lopy 4|1|465 SEK
|Pycom Lora antenna|1|130 SEK
|Adafruit AMG8833 IR Thermal camera|1|366 SEK
|Buzzer|1|38 SEK
|Junction box IP65|1|65 SEK
|10 kΩ resistor|1|1 SEK
|47 kΩ resistor|1|1 SEK
|Gopro camera mount|1|35 SEK
|Breadboard jumper wire male to male|10|32 SEK
|Breadboard jumper wire female to female|4|13 SEK
|Total||4325 SEK


</BR>


## Circuit diagram
![Circuit diagram](/doc/img/circuit_diagram.png "Circuit diagram")


## Cheerson CX-20 drone
The drone we have used for this project is a Cheerson CX-20. It is a quite big drone but is still affordable. We needed a drone with some lift capacity so that we could mount our device underneath. There is no specified number of how much this drone can carry but there are videos on youtube where it flies with weights of 1.5 Kg.
This drone also fits us perfectly beacuse of the pins it has underneath. It has both regulated 5V and 12V straight from the battery. This will be used to power out device and to monitor the battery level.
It also has a stock gopro camera mount that we can use to attach the device.

![Drone](/doc/img/drone.jpg "Drone")
![Pins](/doc/img/pins.jpg "Drone pins")



## Voltage divider
To measure the battery level we needed to scale the voltage down from 12 to beneath 3.3V witch is the maximum tolerance for input on the lopy pins. This is done with a voltage divider. It is a simple circuit containg two resistors with calculated values. 

![Voltage divider](/doc/img/vd1.jpg "Voltage divider")
![Voltage divider](/doc/img/vd2.jpg "Voltage divider")
![Voltage divider](/doc/img/vd3.jpg "Voltage divider")


## Adafruit AMG8833 IR Thermal camera
This is the sensor that will be used for monitoring temperatures. It detects 64(8x8) individual temperatures by IR with a framerate of up to 10Hz. The tempereatures is returned in arrays via I2C communication. It can detect temperatures in a range from 0 to 80 °C on the paper. However, we did discover temperatures up to 138 °C. The viewing angle is 60 ° and detections distance is up to 7 meters. 
4.5 mA power consumption 






Notes: 

Device weight: 186 g

Gopros with housings 100 - 200 g