from adafruit_servokit import ServoKit
kit = ServoKit(channels=16, address=0x41)

while True:
  kit.servo[0].angle = 0
  print(kit.servo[0].angle)