## Features
|No.  |Feature    |Test method  |Result
|:----:|:------------- |:---------------|:-------------|
|1    |Airbourne device.         |Test flying.    |Flying documented in presentation video.
|2    |Monitor power supply/battery level.   |Check feeds in dashboard and compare to voltmeter result.   |Voltmeter shows 2.156 V. With calculations that converts to 12.29 V which is what the dashboard was showing.
|3   |Send data from device.   |Verify that values for temperature and voltage is transmitted to dashboard and task automator.   |Activity status in TTN shows that webhooks are transmitted.  |
|4    |Log data from device.     |Verify that values for temperature and voltage are appended to logfiles.   |Activity log in IFTTT shows that the triggers are executed. Values are appended to [logfiles](/img/temp_log.JPG) in Google Drive.
|5    |Display data.      |Verify that displayed data is correct and measure time delay.    |Delay time is  9.44, 9.55 and 8.78 which gives an average of 9.26 s. By switching from IFTTT/Adafruit to Ubidots we could lower the delay to 6.29, 5.87 and 5.08 which gives an average of 5.75 s.
|6    |Measurement of temperature on surface.  |Fly the device over a heat generation verify that data is presented in dashboard. Measure detection distance in controlled environment.   |See dashboard [printscreen](/img/ubidots_alarm.png) and distance [graph](/img/degrees_distance_diagram.png).
|7    |Activate alarm on pre-defined temperature.   |Fly drone over heat generation above threshold to verify that buzzer i activated and notifications are sent.   |Buzzer is activated (see presentation video) and notifications are sent to [Slack](/img/slack_alarm.png).
|8   |Continue measurement after alarm.   |Verify that dashboard is updated after alarm.   |See time Ubidots [chart](/img/ubidots_no_alarm.png).
|9   |Power hardware from battery.   |Verified by No. 4.   |See battery voltage level in [dashboard](/img/ubidots_no_alarm.png).
|10   |Casing protection.   |Fly drone in light rain.   |In presentation video.   |
