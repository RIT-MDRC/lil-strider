import argparse

from components import servo as servo_actions
from statemanagement.device import configure_device

# Set up argument parser
parser = argparse.ArgumentParser(description="Control servo angles")
parser.add_argument(
    "-a",
    "--angle",
    type=int,
    default=0,
    help="Angle to set for all servos (default: 0)",
)
parser.add_argument(
    "-s",
    "--servo",
    type=int,
    default=None,
    help="Servo to set angle to(default: all)",
)

args = parser.parse_args()

configure_device("config.json")

SERVOS = list(map(lambda i: f"servo{i}", range(1, 18)))
ANGLE = args.angle

if args.servo is not None:
    servo_actions.set_angle(f"servo{args.servo}", ANGLE)
else:
    for servo in SERVOS:
        servo_actions.set_angle(servo, ANGLE)

print("Done!")
