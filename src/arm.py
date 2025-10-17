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

args = parser.parse_args()

configure_device("config.json")

SERVOS = list(map(lambda i: f"servo{i}", range(1, 18)))
ANGLE = args.angle


for servo in SERVOS:
    servo_actions.set_angle(servo, ANGLE)

print("Done!")
