import time
import ctypes
import random
import math
import pyautogui
from itertools import product
from pynput import keyboard
import threading
import numpy as np
import easyocr
reader = easyocr.Reader(['en'])

MOUSEEVENTF_MOVE = 0x0001
CLICK_DELAY = 0.15
SEQUENCES = [
    "".join(p)
    for length in range(3, 5)
    for p in product(["L", "R"], repeat=length)
]
Y = 405 
HEIGHT = 134
# FULLSCREEN
# X = 755
# WIDTH = 391

# HALFSCREEN
X = 1252
WIDTH = 351
running = False
worker = None

def move_condense(dx, dy, steps=60):
    dx += random.randint(-10, 10)
    dy += random.randint(-10, 10)
    
    steps = random.randint(30, 55)
    total_time = random.uniform(0.10, 0.20)
    base_delay = total_time / steps
    curve_bias = random.uniform(0.9, 1.1)

    sent_x = 0
    sent_y = 0

    for i in range(steps - 1):
        t = i / (steps - 1)

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

        time.sleep(base_delay * random.uniform(0.65, 1.35))

    ctypes.windll.user32.mouse_event(
        MOUSEEVENTF_MOVE,
        dx - sent_x,
        dy - sent_y,
        0,
        0
    )

def condense():
    move_condense(900,80)
    time.sleep(0.25)
    for _ in range(5):
        pyautogui.click(button="right")
        time.sleep(1)
    move_condense(-900,-80)

def detect():
    screenshot = pyautogui.screenshot(region=(X, Y, WIDTH, HEIGHT))
    img = np.array(screenshot)
    text = reader.readtext(img, allowlist='LR', detail=0)
    if text:
        print(f'detected text: {text}')
    for seq in sorted(SEQUENCES, key=len, reverse=True):
        if seq in text:
            return seq
    return None

def execute_sequence(seq):
    for c in seq:
        if c == "L":
            pyautogui.click(button="left")
        elif c == "R":
            pyautogui.click(button="right")
        time.sleep(CLICK_DELAY)
    pyautogui.press('2')
    pyautogui.press('1')
    
def fishing_loop():
    global running
    counter = 0
    while running:
        if(counter >= 30):
            condense()
            counter = 0
        for i in range(1):
            time.sleep(0.25)
            pyautogui.click(button="right")
        print(f'fishing loop {counter+1}')
        waiting = True
        while waiting and running:
            detected_seq = detect()
            if detected_seq:
                print(f"Final seq: {detected_seq}")
                waiting = False
                execute_sequence(detected_seq)
                counter += 1
            else:
                time.sleep(0.10)

def on_press(key):
    global running, worker
    try:
        if key.char == '=':
            if not running:
                running = True
                worker = threading.Thread(target=fishing_loop, daemon=True)
                print("Start fishing.")
                worker.start()
            else:
                print("Stop fishing.")
                running = False
    except AttributeError:
        pass

def main():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()
