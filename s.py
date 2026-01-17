import ctypes
import time
from pynput import keyboard
import random
import math

MOUSEEVENTF_MOVE = 0x0001

import ctypes
import time
import random
import math

MOUSEEVENTF_MOVE = 0x0001

def move_condense(dx, dy, steps=60):
    # 🔀 Per-run randomness (NEW)
    dx += random.randint(-10, 10)
    dy += random.randint(-10, 10)
    steps = random.randint(30, 55)              # fewer steps = faster
    total_time = random.uniform(0.10, 0.20)     # REQUIRED range
    base_delay = total_time / steps
    curve_bias = random.uniform(0.9, 1.1)        # curve variation

    sent_x = 0
    sent_y = 0

    for i in range(steps - 1):
        t = i / (steps - 1)

        # human-like easing with randomized curve
        ease = (1 - math.cos(math.pi * t)) / 2
        ease = pow(ease, curve_bias)

        target_x = dx * ease
        target_y = dy * ease

        step_x = int(target_x - sent_x)
        step_y = int(target_y - sent_y)

        sent_x += step_x
        sent_y += step_y

        ctypes.windll.user32.mouse_event(
            MOUSEEVENTF_MOVE,
            step_x,
            step_y,
            0,
            0
        )

        # per-step timing jitter
        time.sleep(base_delay * random.uniform(0.65, 1.35))

    # 🎯 exact correction (no drift, ever)
    ctypes.windll.user32.mouse_event(
        MOUSEEVENTF_MOVE,
        dx - sent_x,
        dy - sent_y,
        0,
        0
    )


def on_press(key):
    try:
        if key.char == '1':
            print("Replaying mouse movement...")
            move_condense(900, 80)
        if key.char == '2':
            print("Replaying mouse movement...")
            move_condense(-900, -80)
    except AttributeError:
        pass

print("Press 1 to replay mouse movement")

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
