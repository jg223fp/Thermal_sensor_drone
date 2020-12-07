# Setup

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











