import asyncio
import json
import os

import websockets
from adafruit_motor.servo import Servo
from dotenv import load_dotenv

from components import servo as servo_actions
from statemanagement.device import configure_device

load_dotenv()

BLENDER_URL = os.getenv("BLENDER_URL", "localhost")

configure_device("config.json")

BLENDER_LEG_TO_SERVO: dict[str, str] = {
    "Armature.000.Bone.01.Bone.02": "servo1",
    "Armature.000.Bone.01.Bone.02.Bone.00": "servo2",
    "Armature.000.Bone.01.Bone.02.Bone.00.Bone.03": "servo3",
    "Armature.001.Bone.01.Bone.02": "servo4",
    "Armature.001.Bone.01.Bone.02.Bone.00": "servo5",
    "Armature.001.Bone.01.Bone.02.Bone.00.Bone.03": "servo6",
    "Armature.002.Bone.01.Bone.02": "servo7",
    "Armature.002.Bone.01.Bone.02.Bone.00": "servo8",
    "Armature.002.Bone.01.Bone.02.Bone.00.Bone.03": "servo9",
    "Armature.003.Bone.01.Bone.02": "servo10",
    "Armature.003.Bone.01.Bone.02.Bone.00": "servo11",
    "Armature.003.Bone.01.Bone.02.Bone.00.Bone.03": "servo12",
    "Armature.004.Bone.01.Bone.02": "servo13",
    "Armature.004.Bone.01.Bone.02.Bone.00": "servo14",
    "Armature.004.Bone.01.Bone.02.Bone.00.Bone.03": "servo15",
    "Armature.005.Bone.01.Bone.02": "servo16",
    "Armature.005.Bone.01.Bone.02.Bone.00": "servo17",
    "Armature.005.Bone.01.Bone.02.Bone.00.Bone.03": "servo18",
}


async def handle_connection(websocket: websockets.ServerConnection):
    print("Client connected.")
    try:
        async for message in websocket:
            data: dict[str, str] = json.loads(message)
            for key, value in data.items():
                if key in BLENDER_LEG_TO_SERVO:
                    servo_name: Servo = BLENDER_LEG_TO_SERVO[key]  # type: ignore
                    angle = int(value)
                    print(f"Setting {servo_name} to {angle}")
                    servo_actions.set_angle(servo_name, angle)
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected.")


async def start_server():
    async with websockets.serve(handle_connection, BLENDER_URL, 8080) as server:
        print(f"WebSocket server started on ws://{BLENDER_URL}:8080")
        await server.serve_forever()  # Run forever


if __name__ == "__main__":
    asyncio.run(start_server())
