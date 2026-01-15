from pynput import keyboard
import pyautogui

Y = 405 
HEIGHT = 134
# FULLSCREEN
# X = 755
# WIDTH = 391

# HALFSCREEN
X = 1252
WIDTH = 351

def on_click(key):
    if key.char == '1':
        img = pyautogui.screenshot(region=(X, Y, WIDTH, HEIGHT))
        img.save("debuge.png")
        print("saved debuge")


# Set up the listener
with keyboard.Listener(on_press=on_click) as listener:
        listener.join()
# 1340 415
# 1083 430
# 830 524
