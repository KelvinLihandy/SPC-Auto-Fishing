from pynput import mouse

def on_click(x, y, button, pressed):
    if pressed and button == mouse.Button.left:
        print(f"Left click detected at ({x}, {y})")

# Set up the listener
with mouse.Listener(on_click=on_click) as listener:
    print("Listening for left clicks... Press Ctrl+C to stop.")
    listener.join()
# 1340 415
# 1083 430
# 830 524