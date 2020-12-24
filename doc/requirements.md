# Solution purpose
The project aimed to develop a simple, yet effective, IoT-device that could help monitor heat generation in wide areas (e.g a disposal processing plant) and notify personnel and/or ultimately the fire brigade.

#### Priority:
1 = Highest

3 = Lowest

## Features
|No.  |Feature    |Description  |Priority   |Test   |Dependants     |
|:----:|:------------- |:---------------|:-------------|:----------|:----------|
|1    |Airbourne device.         |To be able to monitor wide areas the solution must be airborne.   |1  |Test flying.   |-
|2    |Monitor power supply/battery level.   | Monitor power supply/battery status of all hardware included in solution to ensure that the device is working.   |2     |Check feeds in dashboard and compare to voltmeter result. |9
|3   |Send data from device.   |Send data through long-range network to a network service integrator for further process.   |1   |Verify that values for temperature and voltage is transmitted to dashboard and task automator.    |9   |
|4    |Log data from device.      |Send values to logfiles through task automator.   |1   |Verify that values for temperature and voltage are appended to logfiles.   |2, 7
|5    |Display data.               |Display data on a web-based dashboard. Delay may not be more than 10 seconds.   |2   |Verify that displayed data is correct and measure time delay.  |3
|6    |Measurement of temperature on surface.  |Continued measuring must be functional from a vertical height of min 3 m.    |1    |Fly the device over a heat generation verify that data is presented in dashboard. Measure detection distance in controlled environment. |1, 9
|7    |Activate alarm on pre-defined temperature.| If the temperature reach above a preset level, an alarm function shall be activated. A buzzer shall sound in the device and a notification is sent to a platform used by the supervisors. The buzzer shall be deactivated after 10 seconds.    |1  |Fly drone over heat generation above threshold to verify that buzzer i activated and notifications are sent.   |6, 7
|8   |Continue measurement after alarm.   |After the buzzer is deactivated the device shall continue report new temperatures.   |1   |Verify that dashboard is updated after alarm.   |6, 7   |
|9    |Power hardware from battery.   | All included hardware should be powered by a battery.      |1    |Verified by No. 4. |-
|10   |Casing protection.   |Shall be a minimum of IP22 to sustain some solid particles and liquids.   |1   |Fly drone in light rain.  |-
|11   |Automated detection routing.   |Schedule automated flying route to monitor area periodically.   |3   |Test route at pre-defined time.   |1
|12  |Weather forecast control.   |Prevent automated routing if weather forecast is rain or snow.|3    |Verify that weather-service sends forecast data to device.   |3, 11
|13  |Track geoposition.  |Track the units geoposition to track where the abnormal temperature is discovered   |3   |Verify reported postion in external GPS service.   |9

  [36804d87]: www.google.se "Google"
