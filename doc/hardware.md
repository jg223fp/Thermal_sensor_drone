# Hardware
## Components list
|Component  | Quantity   |Price (SEK) |
|:----|:------------- |:---------------|
|Cheerson CX-20 drone (pre-owned) |1    |(2990)
|Pycom expansionboard 3.1 (provded by LNU)   |1   |(189)
|Pycom Lopy 4  (provded by LNU)  |1  |(465)
|Pycom LoRa antenna (provded by LNU)  |1   |(130)
|Adafruit AMG8833 IR Thermal camera|1|366
|Buzzer|1|38
|Junction box IP65|1|65
|10kΩ resistor|1|1
|47kΩ resistor|1|1
|GoPro camera mount (pre-owned)|1   |(35)
|Breadboard jumper wire male to male  |10   |32
|Breadboard jumper wire female to female    |4    |13
|Total||516 SEK


</BR>


## Cheerson CX-20 drone
The drone we have used for this project is a Cheerson CX-20. It's quite a big drone but still affordable. We needed a drone with some lift capacity so that we could mount our device underneath. There is no data on how much it can carry but there are videos on Youtube where it flies with weights of 1.5kg. We aimed to make our device lightweight but still resistant to some liquid.
The drone also suited us perfectly because of the pin connections underneath. It has both regulated 5V and also 12V straight from the battery. We used these to power our device and also to monitor the drones battery level.
It also had a GoPro camera mount that we could use to attach the device.

![Drone](/doc/img/drone.jpg "Drone")
![Pins](/doc/img/pins.jpg "Drone pins")



## Voltage divider
To measure the battery level we had to scale the voltage down from 12V to beneath 3.3V which is the maximum tolerance for input on the LoPy pins. We solved this issue with a voltage divider. It's a simple circuit containing two resistors with calculated values.

![Circuit diagram](/doc/img/circuit_diagram.png "Circuit diagram")

VREF calculation: </BR>
VREF = 12 * (10000 / 47000 + 10000) = 2.198 V

VBAT calculation: </BR>
PIN_voltage = PIN18 input / 1000 </BR>
VBAT = PIN_voltage / (10000 / 47000 + 10000)

![Voltage divider](/doc/img/vd1.jpg "Voltage divider")
![Voltage divider](/doc/img/vd2.jpg "Voltage divider")
![Voltage divider](/doc/img/vd3.jpg "Voltage divider")


## Adafruit AMG8833 IR Thermal camera
This is the sensor that will be used for monitoring temperatures. It detects 64(8x8) individual temperatures by IR with a framerate of up to 10Hz. The temperatures is returned in arrays via I2C communication. It can detect temperatures in a range from 0 to 80 °C on the paper. However, we did discover temperatures up to 138 °C. The viewing angle is 60° and detections distance is up to 7 meters. While testing it did detected temperatures on 7 meters but they where very incorrect. The temperature drops ¤¤¤¤¤¤¤¤¤¤¤¤

4.5 mA power consumption

![thermal sensor](/doc/img/thermal1.jpg "thermal sensor")
![thermal sensor](/doc/img/thermal2.jpg "thermal sensor")

Measured temperature will decrease with distance. The diagram below shows the result from a test that was performed with a set heat generation of 160°C. With the support of this data our belief is that the sensor should be able to detect a heat generation of 150°C from a distance of 4 meters by setting the alarm threshold at 40°C. Since paper self ignites at about 185°C (https://www.dafo.se/Arkiv/Faktabank/Brandrisker-och-riskhantering/Brandteori/Varme/) this configuration should give an eligible function. This will also prevent false alarm when the drone is flying very near the surface.

 ![degrees_distance_diagram](/doc/img/degrees_distance_diagram.png)

With a viewing angle of 60° we calculate:

x = 4 * tan(30°) = 2,3 m

A = (2,3 * 2)² = 21,2 m²

![sensor area](/doc/img/sensor_area_calculation.jpg "sensor_area_calculation")


## The build
To protect the electronics in case of bad weather or a crash we needed to put it all in a casing. For this a junction box with IP66 classing was used.
It turned out that the sensor and pycom developmentboard was fitting perfect inside. A small hole for the sensor was made in the bootom of the box using a rotating file. Small screws was used to attatch it and then some hotglue was placed on the screws on the outside. The buzzer was hot glued on the outside.
As mentioned earlier we needed to keep things lightweight in order to make the battery last longer and for the drone to be able to fly with the device attatched. We know the drone was built for flying with gopro cameras attatched to it using the mount underneath. Gopro cameras weight somewhere between 100 and 200 g with housing and SD-card depending on what model. Our device ended up with a weight of 186 g so it should be fine.  


![Components](/doc/img/build1.jpg "Components")
![Sensor hole](/doc/img/build3.jpg "Sensor hole")
![Inside](/doc/img/build4.jpg "Inside junction box")
![Complete](/doc/img/complete1.jpg "The completed device")
![Attatched](/doc/img/complete2.jpg "Attached to drone")
