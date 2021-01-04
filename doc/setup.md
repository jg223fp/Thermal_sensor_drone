# Setup
## Why we choosed LoRa
We have chosen to use LoRa connection for the data sent by the drone. We know that this may not be the best solution for the project beacuse of LoRas limitations in bandwidht. TTN has a fair access policy of 30 seconds per day for uplinks, and 10 messages per day for downlinks. A more suitable solution for our scenario would proberly be a strong WiFi covering the
waste facility. But this project is also about learning and LoRa is a new and exciting technique. Thats why we still choose to go with it. It also has the advantages of long range, low cost and low power consuption.

## What we gonna do
Just a short and basic description of what we're aiming to do here.
Our target is to upload values to TTN via LorA. On TTN we will decode the values. After that we will use IFTTT and webhooks to send them further to feeds on adafruit io. If the firealarm is set of we will use......(something)


## Setting up TTN
Here is a short explenation of how to set up The Things Network(TTN) when sending the data by LoRa.
First of we will need an acount on www.thethingsnetwork.org.
The second thing we want to do is to create an application. The application is our own small program that will receive the packages that we send.

<img src="/doc/img/TTN1.jpg" width="850">
</BR>

When we´re done creating the app we can navigate to it. On the tab "overview" we will see something called Application EUIS. This is the apps adress. we will need it for our LoRa code to know where to send the packages on TTN. We also need the app key for this. But tog get that we first need to register our device to the application.
<img src="/doc/img/TTN2.jpg" width="850">
</BR>

For this we will need our devices unique id, so called devEUI. Get it by running the following code:
```python
from network import LoRa
import ubinascii

lora = LoRa()
print("DevEUI: %s" % (ubinascii.hexlify(lora.mac()).decode('ascii')))
```

Now we can register the device to the application.

<img src="/doc/img/TTN3.jpg" width="850">
</BR>

When registration is completed, navigate to the registred device to retrieve the app key


<img src="/doc/img/TTN4.jpg" width="850">
</BR>


Basicly we´re good to go now and can start sending and recieving data from TTN. But due to LoRas limited bandwidht we also need to package our data, and that means we also have to unpack it when it´s recived. There is a variation of different formats to use when packing. The worst example for this beeing strings. It seems to be an unwritten rule never to send strings. Here is a comparison between sending a short, a float and a string after beeing packed with the struct module:

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
This is done under the tab "Payload formats". The decoder should be written in javascript. As we jet dont know how to write this we googled and found a prewritten decoder that we modified to suit our needs.
</BR>
<img src="/doc/img/TTN5.jpg" width="850">
</BR>

Here is the code for our payload decoder, it return the two float values that we send.
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


Now the data tab will show our recieved and decoded payloads

<img src="/doc/img/TTN6.jpg" width="850">
</BR>


The last thing we want to do on TTN is to add integrations for IFTTT and Ubidots.
We will use IFTTT to log our transmitted data in a google spreadsheet and Ubidots for showing a dashboard and activating the alarm.
We do this by going to the tab integrations. There are a few to choose from.
### IFTTT
Explanation of the fields:
* Create a Process ID: this can be anything you want, it’s a unique identifier for the IFTTT process
* Create an Event ID: this is what our event within IFTTT will be called, make something up!
* Key: we will get this from IFTTT after creating the IFTTT app
* Values: Here we type the name of our payload values that we will send. We can send up to three.

<img src="/doc/img/TTN7.jpg" width="850">

### Ubidots
Explenation of  the fields:
* Access Key: Select default key
* Token: This is your personal token found on ubidots

<img src="/doc/img/TTN8.jpg" width="850">

### IFTTT
IFTTT is a free to use automation service. It works by a basic concept, that if this happends, then do that.
There is a lot of services connected to IFTTT witch you can combine so the possibilities is endless.
We first used IFTTT to pass on our values to adafruit but this turned out to be a slow choise and we there for used it for datalogging instead.

## Data visualization
Since we already connected TTN to IFTTT it was fairly easy to create a new app that sent the data to Adafruit and be visualized in a dashboard. However, during tests we discovered that the delay of shown values was sometimes over 10 sec. We took a decision to see if we could decrease the delay by connection a service directly to TTN instead of of via IFTTT. TTN natively support connection to Ubidots and after some research we tested how big delay we got using the Ubidots dashboard instead. This decreased the delay to about 5 seconds which made us decided that it should be our dashboard of choice. Below is images from the dashboard in normal status and when an alarm occurs.

<img src="/doc/img/ubidots_no_alarm.png" width="850">
<img src="/doc/img/ubidots_alarm.png" width="850">

## Alarm notifications
We've looked into different solutions to notify supervisors if an alarm occur. With IFTTT there were several service available for notifications and SMS like Notifications (IFTTT app), Pushover and "SMS". Since SMS has a fee and most notification services is relatively unknown and demand a user account we've chosen to use Slack. It's a well established platform were it's easy to add new supervisors to a workspace when needed.
To integrate with Slack we use Ubidots events to forward alarms if the trigger level is reached. The alarms will appear in a workspace we've created for the purpose which is configurated to notify the users at all time.

<img src="/doc/img/slack_alarm.png" width="700">
<img src="/doc/img/slack_push.jpeg" width="300">

## System logging
Most systems need to have a log so users can see the history of generated data. In our setup we reused the webhooks we already set up from TTN to IFTTT and created two new applets.
 

<img src="/doc/img/IFTTT_log_app1.png" width="300">
<img src="/doc/img/IFTTT_log_app2.png" width="300">


These will forward "value1" and "value2" together with timestamp to spreadsheets in Google Drive.


<img src="/doc/img/google_logging.png" width="500">


When 2000 events has been added new sheets are created. A full spreadsheet will have a minimal size of 23kb.


<img src="/doc/img/temp_log.JPG" width="500">
