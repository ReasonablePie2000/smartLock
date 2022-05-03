# smartLock
A small project that uses a raspberry pi to turn a normal door lock into a smart door lock that can unlock with facial recognition and display the room's temp and humidity.


The lock is mounted on a cardboard box and controlled by an s3003 servo motor which is connected to the Raspberry pi 4B. The sense that will measure the temperature and humidity of the room. Then display the temp and humidity on the display on senseHat. Users can control the whole system by using the joystick on the senseHat.

Since the GPIO pins are needed for the motor, I choose to connect the senseHat with a breadboard so I can also connect the motor at the same time.

![alt text](https://github.com/ReasonablePie2000/smartLock/blob/master/image/lock_01.JPG)
(Picture of the smart lock)
