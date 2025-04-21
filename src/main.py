from components.servo import set_angle
from statemanagement.device import configure_device

configure_device("config.json")

while True:
    set_angle("servo1", 270)
