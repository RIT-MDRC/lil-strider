from dataclasses import dataclass

import board
import busio

from statemanagement.device import create_context, device, device_parser, identifier

ctx = create_context("I2C", busio.I2C)


@device_parser(ctx)
def parse_i2c(_: dict):
    return busio.I2C(board.SCL, board.SDA)
