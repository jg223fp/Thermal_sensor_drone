# Setup

## The code

### Boot file
We choosed to setup our pins in the boot file since its something that will only be carried out ones.
The bootfile will also perform some selftests to verify that the hardware is working properly.
This flowchart will give a brief explenation.</BR>

<img src="/img/flow2.jpg" width="500">
</BR>

### Main file
To make the main file work fast we used a module named thread_. This module allows us to run things paralelly in different threads. 
If we would have ran everything in the same loop, LoRa would have slowed everything down and we would miss meny temperatures. In a reallife event this could have had devastating consequences. We tried to make things even faster by shrinking the sending time for LoRa but without any luck. The standard time is 3 seconds. Even a small adjustment down to 2.5 seconds resulted in a unreliable and unstable program. 
The LoRa thread has a loop time of 3 seconds and the temperature detection thread loops with a time of 250 ms.
We dont send every detected value. When the LoRa thread has finished sending a value it will grab the most recent detected temperature and the battery voltage and send. If the temperature thread detects a temperature wich is over the limit an alarm will be triggered. When this happens the program starts sounding the buzzer and keeps sending the triggering temperature over and over for a given time (20 s) to make sure it is noticed.
This flowchart gives a basic explanation of the two threads.

<img src="/img/FLOW1.jpg" width="650">
</BR>

The temperature sensor detects 64 temperatures at the same time. This function goes through all of the 64 values, selecting the highest one detected as that is the one witch we are intereseted in.
```python
def read_temperature():
    i2c = machine.I2C(1)
    sensor = AMG88XX(i2c)
    while True:
        highest_temp = 0
        utime.sleep(0.2)
        sensor.refresh()
        for row in range(8):
            for col in range(8):
                if sensor[row, col] > highest_temp:  
                     highest_temp = sensor[row, col]
        return highest_temp
```



### Libraries

#### lora
To keep our main file clean we put all the code for LoRa in a seperate file except the app_eui and the app_key as those will be provided from the main file when making the conncetion. We simplified the usage by making one function for connecting and one function for sending.
Our sending function is adapted to our project as it encodes two float values with the struct module.
```python
def send_values(temp,vbat):
    payload = struct.pack(">ff", temp,vbat)     #encode payload
    s.send(payload)     #send payload
    print("Sending payload...")
```

#### amg88xx
This library is for the thermal sensor AMG8833.
The first library we found for this sensor was written in circuit python and we thought that maby with some guiding and help we could edit it into micropython. But with some luck we stumbled across this library written in micropython. It was written by Dean Miller, Scott Shawcroft for Adafruit Industries under MIT license.

#### voltage_measure
This is a library which contains a function for calculating the measured battery voltage. The measuring is done by an ADC converter.

#### sounds
A library containing all the different buzzer sounds. At first both the main and the boot file contained the sounds they needed. When cleaning the code we realized how blurry it made the code and moved them to a seperate file.



## Why we choosed LoRa
We have chosen to use LoRa connection for the data sent by the drone. We know that this may not be the best solution for the project because of LoRas limitations in bandwidth. TTN has a fair access policy of 30 seconds per day for up links, and 10 messages per day for down links. A more suitable solution for our scenario would properly be a strong Wi-Fi covering the
waste facility. But this project is also about learning and LoRa is a new and exciting technique. That's why we still choose to go with it. It also has the advantages of long range, low cost and low power consumption.

## Our goal
Just a short and basic description of what we're aiming to do here.
Our target is to upload values to TTN via LorA. On TTN we will decode the values. The values will be sent to Ubidots and to IFTTT. Ubidots will be used as a dashboard for showing the values and to send pushnotifications if the alarm is activated. IFTTT will forward the data to log it in spreadsheets in Google Drive


## Setting up TTN
Here is a short explanation of how to set up The Things Network(TTN) when sending the data by LoRa.
First of we will need an account on www.thethingsnetwork.org.
The second thing we want to do is to create an application. The application is our own small program that will receive the packages that we send.

<img src="/img/TTN1.jpg" width="850">
</BR>

When we’re done with creating the app we can navigate to it. On the tab "overview" we will see something called Application EUIS. This is the apps address.We will need it for our LoRa code to know where to send the packages on TTN. We also need the app key for this. But tog get that we first need to register our device to the application.
<img src="/img/TTN2.jpg" width="850">
</BR>

For this we will need our devices unique id, so called devEUI. Get it by running the following code:
```python
from network import LoRa
import ubinascii

lora = LoRa()
print("DevEUI: %s" % (ubinascii.hexlify(lora.mac()).decode('ascii')))
```

Now we can register the device to the application.

<img src="/img/TTN3.jpg" width="850">
</BR>

When registration is completed, navigate to the registered device to retrieve the app key


<img src="/img/TTN4.jpg" width="850">
</BR>


Basically we’re good to go now and can start sending and receiving data from TTN. But due to LoRas limited bandwidth we also need to package our data, and that means we also have to unpack it when it’s received. There is a variation of different formats to use when packing. The worst example for this being strings. It seems to be an unwritten rule never to send strings. Here is a comparison between sending a short, a float and a string after being packed with the struct module:

| Format      | Data |Amount of bytes|  Payload in bytes  |
|:------------- |:---------------:| -------------:|----------:|
| Short |7           |2| 00 07         |
|Float|7.00|4|       40 E0 00 00|
|String|"seven"|5| 73 65 76 65 6e |

</BR>
We used Pythons built in struct module.
Data is represented as 2 float values, each of 4 bytes. The ">" arrow sets the byte order to 'big-endian' when packing.

```python
payload = struct.pack(">ff", value1,value2) #encode payload
```
</BR>
Now we only need to unpack the data when its received in our application on TTN.
This is done under the tab "Payload formats". The decoder should be written in javascript. As we jet don't know how to write this we googled and found a working decoder that we modified to suit our needs.
</BR>
<img src="/img/TTN5.jpg" width="850">
</BR>

Here is the code for our payload decoder, it returns the two float values that we send.
```javascript
function Decoder(bytes, port) {

  var payload = bytes.length;
  var decoded = {};
  var bits = (bytes[0] << 24) | (bytes[1] << 16) | (bytes[2] << 8) | (bytes[3]);
  var sign = ((bits >>> 31) == 0) ? 1.0 : -1.0;
  var e = ((bits >>> 23) & 0xff);
  var m = (e == 0) ? (bits & 0x7fffff) << 1 : (bits & 0x7fffff) | 0x800000;
  var f = sign * m * Math.pow(2, e - 150);

  decoded.temperature = +f.toFixed(2);

  var bits = (bytes[4] << 24) | (bytes[5] << 16) | (bytes[6] << 8) | (bytes[7]);
  var sign = ((bits >>> 31) == 0) ? 1.0 : -1.0;
  var e = ((bits >>> 23) & 0xff);
  var m = (e == 0) ? (bits & 0x7fffff) << 1 : (bits & 0x7fffff) | 0x800000;
  var f = sign * m * Math.pow(2, e - 150);

  decoded.voltage  = +f.toFixed(2);

  return decoded;
}


```


Now the data tab will show our received and decoded payloads

<img src="/img/TTN6.jpg" width="850">
</BR>


The last thing we want to do on TTN is to add integrations for IFTTT and Ubidots.
We will use IFTTT to log our transmitted data in a google spreadsheet and Ubidots for showing a dashboard and activating the alarm.
We do this by going to the tab integrations. There are a few to choose from.
### IFTTT
IFTTT is a free to use automation service. It works by a basic concept, that if this happens, then do that.
There is a lot of services connected to IFTTT witch you can combine so the possibilities is endless.
We first used IFTTT to pass on our values to adafruit but this turned out to be a slow choice and we there for used it for data logging instead.
Explanation of the fields:
* Create a Process ID: this can be anything you want, it’s a unique identifier for the IFTTT process
* Create an Event ID: this is what our event within IFTTT will be called, make something up!
* Key: we will get this from IFTTT after creating the IFTTT app
* Values: Here we type the name of our payload values that we will send. We can send up to three.

<img src="/img/TTN7.jpg" width="850">

### Ubidots
Explenation of  the fields:
* Access Key: Select default key
* Token: This is your personal token found on ubidots

<img src="/img/TTN8.jpg" width="850">


## Data visualization
Since we already connected TTN to IFTTT it was fairly easy to create a new app that sent the data to Adafruit and be visualized in a dashboard. However, during tests we discovered that the delay of shown values was sometimes over 10 sec. We took a decision to see if we could decrease the delay by connection a service directly to TTN instead of via IFTTT. TTN natively support connection to Ubidots and after some research we tested how big delay we got using the Ubidots dashboard instead. This decreased the delay to about 5 seconds which made us decided that it should be our dashboard of choice. Below is images from the dashboard in normal status and when an alarm occurs.

<img src="/img/ubidots_no_alarm.png" width="850">
<img src="/img/ubidots_alarm.png" width="850">

## Alarm notifications
We've looked into different solutions to notify supervisors if an alarm occur. With IFTTT there were several service available for notifications and SMS like Notifications (IFTTT app), Pushover and "SMS". Since SMS has a fee and most notification services is relatively unknown and demand a user account we've chosen to use Slack. It's a well established platform where it's easy to add new supervisors to a workspace when needed.
To integrate with Slack we use Ubidots events to forward alarms if the trigger level is reached. The alarms will appear in a workspace we've created for the purpose which is configured to notify the users at all time.

<img src="/img/slack_alarm.png" width="700">
<img src="/img/slack_push.jpeg" width="300">

## System logging
Most systems need to have a log so users can see the history of generated data. In our setup we reused the webhooks we already set up from TTN to IFTTT and created two new applets.
 

<img src="/img/IFTTT_log_app1.png" width="300">
<img src="/img/IFTTT_log_app2.png" width="300">


These will forward "value1" and "value2" together with timestamp to spreadsheets in Google Drive.


<img src="/img/google_logging.png" width="500">


When 2000 events has been added new sheets are created. A full spreadsheet will have a minimal size of 23kb.


<img src="/img/temp_log.JPG" width="500">
