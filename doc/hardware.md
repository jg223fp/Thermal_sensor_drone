# Hardware
## Components list
|Component  | Quantity   |Price (SEK) |
|:----|:------------- |:---------------|
|Cheerson CX-20 drone |1|Owned(2990) 
|Pycom expansionboard 3.1 |1|Borrowed(189) 
|Pycom Lopy 4 |1|Borrowed(465) 
|Pycom Lora antenna|1|Borrowed(130) 
|Adafruit AMG8833 IR Thermal camera|1|366 
|Buzzer|1|38 
|Junction box IP65|1|65 
|10 kΩ resistor|1|1 
|47 kΩ resistor|1|1 
|Gopro camera mount|1|Owbed(35) 
|Breadboard jumper wire male to male|10|32 
|Breadboard jumper wire female to female|4|13 
|Total||516 SEK


</BR>


## Circuit diagram
![Circuit diagram](/doc/img/circuit_diagram.png "Circuit diagram")


## Cheerson CX-20 drone
The drone we have used for this project is a Cheerson CX-20. It is a quite big drone but is still affordable. We needed a drone with some lift capacity so that we could mount our device underneath. There is no specified number of how much this drone can carry but there are videos on youtube where it flies with weights of 1.5 Kg. We will aim at making our device lightweight but still protective.
This drone also fits us perfectly beacuse of the pins it has underneath. It has both regulated 5V and also 12V straight from the battery. This will be used to power our device and to monitor the battery level.
It also has a stock gopro camera mount that we can use to attach the device.

![Drone](/doc/img/drone.jpg "Drone")
![Pins](/doc/img/pins.jpg "Drone pins")



## Voltage divider
To measure the battery level we needed to scale the voltage down from 12 to beneath 3.3V witch is the maximum tolerance for input on the lopy pins. This is done with a voltage divider. It is a simple circuit containg two resistors with calculated values. 

![Voltage divider](/doc/img/vd1.jpg "Voltage divider")
![Voltage divider](/doc/img/vd2.jpg "Voltage divider")
![Voltage divider](/doc/img/vd3.jpg "Voltage divider")


## Adafruit AMG8833 IR Thermal camera
This is the sensor that will be used for monitoring temperatures. It detects 64(8x8) individual temperatures by IR with a framerate of up to 10Hz. The tempereatures is returned in arrays via I2C communication. It can detect temperatures in a range from 0 to 80 °C on the paper. However, we did discover temperatures up to 138 °C. The viewing angle is 60 ° and detections distance is up to 7 meters. While testing it did detected temperatures on 7 meters but they where very incorrect. The temperature drops ¤¤¤¤¤¤¤¤¤¤¤¤

4.5 mA power consumption 

![thermal sensor](/doc/img/thermal1.jpg "thermal sensor")
![thermal sensor](/doc/img/thermal2.jpg "thermal sensor")




## The build
To protect the electronics in case of bad weather or a crash we needed to put it all in a casing. For this a junction box with IP66 classing was used.
It turned out that the sensor and pycom developmentboard was fitting perfect inside. A small hole for the sensor was made in the bootom of the box using a rotating file. Small screws was used to attatch it and then some hotglue was placed on the screws on the outside. The buzzer was hot glued on the outside. 
As mentioned earlier we needed to keep things lightweight in order to make the battery last longer and for the drone to be able to fly with the device attatched. We know the drone was built for flying with gopro cameras attatched to it using the mount underneath. Gopro cameras weight somewhere between 100 and 200 g with housing and SD-card depending on what model. Our device ended up with a weight of 186 g so it should be fine.  


![Components](/doc/img/build1.jpg "Components")
![Sensor hole](/doc/img/build3.jpg "Sensor hole")
![Inside](/doc/img/build4.jpg "Inside junction box")
![Complete](/doc/img/complete1.jpg "The completed device")
![Attatched](/doc/img/complete2.jpg "Attached to drone")