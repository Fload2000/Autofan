# Overview
This is script for an automated fan control for the Raspberry-Pi. It sets the fan speed depending on the chip temperature. There is even a silentime, where the fan should not spin (e.g. at night if the Raspberry-Pi is in your Bedroom and you want to keep it quiet)

# Setup - Hardware
Wiring:  
![alt text](https://github.com/Fload2000/Autofan/blob/master/src/img/wiring.png "Wiring")

# Setup/Customize - Script
There a basically three things you can setup/customize in this script:
### (1) FanPin

### (2) Desired temperature of the CPU

### (3) Time when the fan should not spin


# Start script on startup

## Cronjob
First type in the following command: 
```sh
~ crontab -e
```
Then enter this line (but change the path to the directory where the script is located on your Pi):
```sh
@reboot sudo python /home/user/autofan.py &
```
Close the editor and reboot. The script should start now during the startup.

## Systemd
First type in the following command:
```sh
~ sudo vim /etc/systemd/system/autofan.service
```
If you are not familiar with vim, use nano.  
Then insert the following lines:
```sh
[Unit]
Description=Autofan
After=multi-user.target

[Service]
Type=simple
User=user
Group=user
ExecStart=/usr/bin/python /home/user/autofan.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```
(In case you have to edit the service file later on, you have to run `~ systemctl daemon-reload` so systemd knows you changed something)
Save the file and run following command:
```sh
~ sudo systemctl enable autofan
```
This should enable the service.
Now we only have to start the service, which could be done by the following command:
```sh
~ sudo systemctl start autofan
```

## rc.local
First type in the following command:
```sh
~ sudo vim /etc/rc.local
```
If you are not familiar with vim, use nano.

You should see the following text:
```sh
#!/bin/sh -e
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.

exit 0
```
Now write before the `exit 0` following line (but change the path to the directory where the script is located on your Pi):
```sh
/usr/bin/python /home/user/autofan.py
```
Now you can save the file and the scipt should autostart.

# License

```
MIT License

Copyright (c) 2019 Fload

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```