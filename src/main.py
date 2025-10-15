import asyncio
import json
import os
import threading
from concurrent.futures import ThreadPoolExecutor
from queue import Empty, Queue

import websockets
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

# Thread pool for handling servo operations
servo_executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix="servo_worker")
# Message queue for buffering incoming servo commands
servo_queue = Queue(maxsize=1000)
# Flag to control the servo processing thread
running = True


def process_servo_command(servo_name: str, angle: int):
    """Process a single servo command in a separate thread."""
    try:
        servo_actions.set_angle(servo_name, angle)
    except Exception as e:
        print(f"Error setting servo {servo_name} to angle {angle}: {e}")


def servo_worker():
    """Worker thread that processes servo commands from the queue."""
    while running:
        try:
            # Get command from queue with timeout to allow checking running flag
            command = servo_queue.get(timeout=0.1)
            if command is None:  # Sentinel value to stop the thread
                break
            servo_name, angle = command
            process_servo_command(servo_name, angle)
            servo_queue.task_done()
        except Empty:
            # This is expected when the queue is empty, just continue
            continue
        except Exception as e:
            print(f"Error in servo worker: {e}")


# Start the servo worker thread
servo_thread = threading.Thread(target=servo_worker, daemon=True)
servo_thread.start()


async def handle_connection(websocket: websockets.ServerConnection):
    print("Client connected.")
    try:
        async for message in websocket:
            data: dict[str, str] = json.loads(message)
            print(f"Received: {data}")

            # Process all servo commands asynchronously
            for key, value in data.items():
                if key in BLENDER_LEG_TO_SERVO:
                    servo_name: str = BLENDER_LEG_TO_SERVO[key]
                    angle = int(value)

                    # Add command to queue for processing by worker thread
                    try:
                        servo_queue.put_nowait((servo_name, angle))
                    except Exception as e:
                        print(f"Queue full, dropping command for {servo_name}: {e}")

    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected.")


async def start_server():
    async with websockets.serve(handle_connection, BLENDER_URL, 8080) as server:
        print(f"WebSocket server started on ws://{BLENDER_URL}:8080")
        try:
            await server.serve_forever()  # Run forever
        except KeyboardInterrupt:
            print("Shutting down...")
            global running
            running = False
            servo_queue.put(None)  # Signal worker thread to stop
            servo_executor.shutdown(wait=True)
            print("Done! Cleaned up")


if __name__ == "__main__":
    task = None
    try:
        task = asyncio.run(start_server())
    except KeyboardInterrupt:
        print("Shutting down...")
        running = False
        servo_queue.put(None)
        servo_executor.shutdown(wait=True)
        print("Done! Cleaned up server...")
