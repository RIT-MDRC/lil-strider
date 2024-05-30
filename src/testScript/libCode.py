from adafruit_servokit import ServoKit
kit = ServoKit(channels=16, address=0x41)

servo1 = kit.servo[1]

while True:
  servo1.angle = 180
  print(servo1.angle)