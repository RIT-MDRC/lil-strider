from dataclasses import dataclass

import adafruit_pca9685
import busio

import components.i2c as i2c_actions
from statemanagement.device import create_context, device, device_parser, identifier

hat_ctx = create_context("ServoHat", adafruit_pca9685.PCA9685)


@device_parser(hat_ctx)
def parse_hat(config: dict):
    config["i2c"] = (
        config["i2c"]
        if isinstance(config["i2c"], busio.I2C)
        else i2c_actions.ctx[config["i2c"]]
    )
    if not isinstance(config["address"], int):
        # in case the address is a string of hex or binary number in json file we need to convert it to int
        base = 16 if "address_base" not in config else config["address_base"]
        if "address_base" in config:
            del config["address_base"]
        addr = int(config["address"], base)
        config["address"] = addr

    return adafruit_pca9685.PCA9685(**config)


@device
@dataclass
class Servo:
    intdex: int
    servo_hat: adafruit_pca9685.PCA9685 = identifier(hat_ctx)


servo_ctx = create_context("Servo", Servo)
ctx = servo_ctx
"""main ctx to use for servo component."""


@device_parser(servo_ctx)
def parse_servo(config: dict):
    return Servo(**config)
