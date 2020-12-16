## Features
|No.  |Feature    |Test method  |Result
|:----:|:------------- |:---------------|:-------------|
|1    |Airbourne device.         |Test flying.    |Flying documented in presentation video.
|2    |Monitor power supply/battery level.   |Check feeds in dashboard and compare to voltmeter result.   |Voltmeter shows 2.156 V. With calculations that converts to 12.29 V which is what the dashboard was showing. See image xxx.
|3    |Send data from device to a task automator.      |Verify that triggers for alarm, temp., and voltage is executed.   |Activity log in IFTTT shows that the triggers are executed.
|4    |Display data.      |Verify that displayed data is correct and measure time delay.    |Delay time is  9.44, 9.55 and 8.78 which gives an average of 9.26 s. By switching from IFTTT/Adafruit to Ubidots we could lower the delay to 6.29, 5.87 and 5.08 which gives an average of 4.75 s.
|5    |Measurement of temperature on surface.  |Fly the device over a heat generation verify that data is presented in dashboard. Measure detection distance in controlled environment.   |
