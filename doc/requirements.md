# Solution purpose
The project aimed to develop a simple, yet effective, IoT-device that could help monitor heat generation in wide areas (e.g a disposal processing plant) and notify personnel and/or ultimately the fire brigade.

#### Priority:
1 = Highest

3 = Lowest

## Features
|No.  |Feature    |Description  |Priority   |Test   |Dependants     |
|:----:|:------------- |:---------------|:-------------|:----------|:----------|
|1    |Airbourne device.         |To be able to monitor wide areas the solution must be airborne.   |1|
|2    |Monitor power supply/battery level.   | Monitor power supply/battery status of all hardware included in solution to ensure that the device is working.   |2     | |8
|3    |Send data from device to a task automator.      |Send data through long-range network to a web-based task automator, e.g IFTTT, for further process.   |1   |    |2, 6
|4    |Display data.               |Display data on a web-based dashboard. Delay may not be more than 10 seconds.   |2   | |3
|5    |Continued measurement of temperature on surface.  |Measuring must be functional from a vertical height of min 5m.    |1    | ||1, 8
|6    |Activate alarm on pre-defined temperature.| If the temperature reach above a preset level, an alarm function shall be activated. A buzzer shall sound in the device and a notification is sent to a platform used by the supervisors. The buzzer shall be deactivated after 10 seconds.    |1 | |3, 6
|7   |Continue No. 5 after buzzer.   |After the buzzer is deactivated the device shall continue report new temperatures.   |   |1   |   |5, 6
|8    |Power hardware from battery.   | All included hardware should be powered by a battery.      |1    | |
|9   |Casing protection.   |Shall be a minimum of IP22 to sustain some solid particles and liquids.   |1   |
|10   |Automated detection routing.   |Schedule automated flying route to monitor area periodically.   |3   ||1
|11  |Weather forecast control.   |Prevent automated routing if weather forecast is rain or snow.|3    ||3, 10
|12  |Track geoposition.  |Track the units geoposition to track where the abnormal temperature is discovered   |3   |   |8
