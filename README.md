![Fire and drone](/img/project_plan_front.jpg "fire_drone")

# Thermal sensor drone

#### Members: Johan Gustafsson (jg223fp), Pierre Oskarsson (po222gu)
#### Program: Computer Science  
#### Course:  Introducing project (1DT308)
#### Date of submission: 21xx-xx-xx

## Abstract
The project aimed to develop a simple, yet effective, IoT-device that could help monitor heat generation in wide areas (e.g a disposal processing plant) and notify personel and/or ultimately the fire brigade.

## Background
The idea came from a relative who works as an engineer at a municipality energy department.

He described how the vast property of a disposal processing plant or a recycling facility can be hard to monitor. A fire can be devastating so if heat generation can be detected in an early stage, the risk of injuries and damage on environment can be minimized.

## Idea
Develop an airborne product that periodically measures surface temperature to detect anomalis and report them via wireless network for further processing.

## Method
[Requirements](/doc/requirements.md)

[Setup](/doc/setup.md)

[Hardware](/doc/hardware.md)

[Test](/doc/test.md)

[Timelog](/doc/timelog.md)

## Results
Presentation movie on Youtube: [Link](https://youtu.be/mJG1LvA-VR4)

By connection a thermal sensor to a Pycom micro-controller we were able to fetch data that could be processed and transmitted via LoRa. The devices where attached to a drone to be airborne and also powered by it's battery. The collected data is the temperature from each pixel in the sensor as well as the drone battery voltage that we measured through a voltage divider.
Measured temperature will decrease over distance so compensating for that inaccuracy is part of the processing. The data is sent to The Things Network that is LoRa server community and then forwarded via webhooks to the service integrator IFTTT and the IoT platform Ubidots. Ubidots is used to visualize the data in a dashboard and it also triggers alarm notifications. IFTTT is used to log data into a spreadsheet on Google Drive. For notifications we use Slack since it's a widly used platform we're it's easy to add supervisors that should respond to alarms.

<img src="/img/complete2.jpg" width="400">

While we think all the primarily requirements have been fulfilled this project has many development possibilites. We used a drone that was already in our posses so in order to make scheduled and pre-defined flights we would have to have another drone. Our initial plan was also to extract GPS coordinates from the drone but after some research this would require much deeper knowledge.

Summarized it has been a tremendously fun project where we are well under way to create a device that really could be a great help and service to the real world.
