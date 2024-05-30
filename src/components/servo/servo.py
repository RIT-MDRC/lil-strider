from dataclasses import dataclass
import logging

import adafruit_pca9685
import busio
from adafruit_motor.servo import Servo

import components.servo.i2c as i2c_actions
from statemanagement.device import (
    create_context,
    device_action,
    device_parser,
)

hat_ctx = create_context("ServoHat", adafruit_pca9685.PCA9685)


@device_parser(hat_ctx)
def parse_hat(config: dict):
    config["i2c_bus"] = (
        config["i2c"]
        if isinstance(config["i2c_bus"], busio.I2C)
        else i2c_actions.ctx[config["i2c_bus"]]
    )
    if not isinstance(config["address"], int):
        # in case the address is a string of hex or binary number in json file we need to convert it to int
        base = 16 if "address_base" not in config else config["address_base"]
        if "address_base" in config:
            del config["address_base"]
        addr = int(config["address"], base)
        config["address"] = addr
    del config["_identifier"]
    
    return adafruit_pca9685.PCA9685(**config)


ctx = create_context("Servo", Servo)
"""main ctx to use for servo component."""


@device_parser(ctx)
def parse_servo(config: dict):
    hat = config.get("hat")
    channel_index = config.get("channel")
    min_pulse = config.get("min_pulse", 500)
    max_pulse = config.get("max_pulse", 2500)
    if hat is None or channel_index is None:
        raise ValueError("hat and channel are required for a servo")
    if isinstance(hat, str):
        hat = hat_ctx.store.get(hat)
        if hat is None:
            raise Exception("Hat was not found")
    return Servo(hat.channels[channel_index], min_pulse=min_pulse, max_pulse=max_pulse, actuation_range=270)


@device_action(ctx)
def set_angle(device: Servo, angle: int):
    logging.info("setting servo to %s", str(angle))
    device.angle = angle
