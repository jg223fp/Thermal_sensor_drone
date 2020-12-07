# Setup
We have chosen to use LoRa connection for the data sent by the drone. We know that this may not not be the best solution fot the project beacuse of LoRas limitations in bandwidht. TTN has a fair access policy of 30 seconds per day for uplinks, and 10 messages per day for downlinks. A more suitable solution for us would proberly be a strong WiFi covering the 
waste facility. But this project is also about learning and LoRa is a new and exciting technique. Thats why we still choose to go with it. It also has the advantages of long range, low cost and low power consuption.


## Setting up TTN
Here is a short explenation of how to set up The Things Network(TTN) when sending your data by LoRa.
First of you will need an acount on www.thethingsnetwork.org so create one if you haven´t.
The second thing you want to do is to create an application. The application is our own small program that will receive the packages that we send.

![Adding new application](/doc/img/TTN1.jpg "Adding new application")

When we´re done creating the app we can navigate to it. On the tab "overview" we will see something called Application EUIS. This is the apps adress. we will need it for our LoRa code to know where to send the packages on TTN. We also need the app key for this. But tog get that we first need to register our device to the application.
![app eui](/doc/img/TTN2.jpg "app eui")

For this we will need our devices unique id, so called devEUI. Get it by running the following code:
```python
from network import LoRa
import ubinascii

lora = LoRa()
print("DevEUI: %s" % (ubinascii.hexlify(lora.mac()).decode('ascii')))
```

Now we can register the device to the application.
![Register device](/doc/img/TTN3.jpg "Register device")

When registration is completed, navigate to the registred device to retrieve the app key


![app key](/doc/img/TTN4.jpg "app key")


Basicly we´re good to go now and can start sending and recieving data from TTN. But due to LoRas limited bandwidht we also need to package our data, and that means we also have to unpack it when it´s recived. There is a variation of different formats to use when packing. The worst example for this beeing strings. It seems to be an unwritten rule never to send strings. Here is a comparison between sending a short, a float and a string:

| Format      | Data |Amount of bytes|  Payload in bytes  |
|:------------- |:---------------:| -------------:|----------:|
| Short |7           |1| 37         |
|Float|7.00|4|       37 2e 30 30|
|String|"seven"|7|22 73 65 76 65 6e 22|

</BR>
We used Pythons built in struct module.
Data is represented as 2 float values, each of 4 bytes. The ">" arrow sets the byte order to 'big-endian' when packing.

```python
payload = struct.pack(">ff", value1,value2) #encode payload
```

Now we only need to unpack the data when its received in our application on TTN.
This is done under the tab "Payload formats". The decoder should be written in javascript. As we jet dont know how to write this we googled and found a prewritten decoder that we modified to suit our needs.
![Payload decoder](/doc/img/TTN4.jpg "Payload decoder")

Here is the code for our payload decoder, it return the two float values that we send but if the payload is shorter than 4 bytes it activates the alarm function meaning a fire has been detected. So instead of sending a string saying "alarm activated", we just send a short payload and then the payload decoder will know what to do. 
```javascript
function Decoder(bytes, port) {
  
  var payload = bytes.length;
  
  if (payload<4) {  // if the payload is shorter than 4 the alarm will be set off
   var objects = {};
   var alarm = 'active'; 
  
  objects.alarm = alarm;
  return objects;
}

  else {
  
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
}}

```







