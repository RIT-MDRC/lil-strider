from components import servo as servo_actions
from statemanagement.device import configure_device

configure_device("config.json")

SERVOS = list(map(lambda i: f"servo{i}", range(1, 18)))
ANGLE = 0


for servo in SERVOS:
    servo_actions.set_angle(servo, ANGLE)

print("Done!")
