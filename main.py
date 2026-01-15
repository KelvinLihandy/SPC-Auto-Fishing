import time
import pyautogui
from itertools import product
from pynput import keyboard
import threading
import numpy as np
import easyocr
reader = easyocr.Reader(['en'])

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

# def condense():

#     # add move to crafting table here
        
#     for _ in range(10):
#         pyautogui.click(button="right")
#         x, y = pyautogui.position()
#         print(f"Right-click at ({x}, {y})")
#         time.sleep(0.5)
#     print('condensed')
    
#     # add return to spot here1

def detect():
    screenshot = pyautogui.screenshot(region=(X, Y, WIDTH, HEIGHT))
    img = np.array(screenshot)
    text = reader.readtext(img, allowlist='LR', detail=0)
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

def fishing_loop():
    # maybe add sound detecting
    global running
    counter = 0
    while running:
        # if(counter > 10):
        #     condense()
        #     counter = 0
        for i in range(3):
            # multi right click to avoid not casting caused by lag
            if i > 0:
                time.sleep(0.2)
            pyautogui.click(button="right")
        waiting = True
        while waiting and running:
            detected_seq = detect()
            if detected_seq:
                print(f"Final seq: {detected_seq}")
                waiting = False
                execute_sequence(detected_seq)
                counter += 1
                print(f'fishing loop {counter}')
            else:
                time.sleep(0.10)

        time.sleep(0.5)

def on_press(key):
    global running, worker
    try:
        if key.char == '1':
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
