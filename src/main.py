from components.servo import set_angle
from statemanagement.device import configure_device

configure_device("config.json")

set_angle("servo5", 0)
