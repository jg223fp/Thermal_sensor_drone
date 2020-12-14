# Solution purpose
The project aimed to develop a simple, yet effective, IoT-device that could help monitor heat generation in wide areas (e.g a disposal processing plant) and notify personnel and/or ultimately the fire brigade.

#### Priority:
1 = Highest</BR> 3 = Lowest

## Features
|No.|  Feature    |Description  |Priority   |Test   |Dependants     |
|:----:|:------------- |:---------------|:-------------|:----------|:----------|
|1    |Airbourne device.         |To be able to monitor wide areas the solution must be airborne.   ||
|2    |Monitor power supply/battery level.   | Monitor power supply/battery status of all hardware included in solution to ensure that the device is working.   |     |8
|3    |Send data from device to a task automator.      |Send data through long-range network to a web-based task automator, e.g IFTTT, for further process.   |   |
|4    |Display data.               |Display data on a web-based dashboard. Delay may not be more than 20 seconds.   | |3,4
|6    |Measure temperature on surface.  |   Measuring must be functional from a vertical height of min 5m.|                                                           | |1,8
|7    |Activate alarm on pre-defined temperature.| If the temperature reach above a preset level, an alarm function shall be activated. A buzzer shall sound in the device and notification is sent to supervisors. The buzzer shall be deactivated after 180 seconds.    ||6,8
|8    |Power hardware from battery.               | All included hardware should be powered by a battery.                                                               | |
|9   |   |   |   |
