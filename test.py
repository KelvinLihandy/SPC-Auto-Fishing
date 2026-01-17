from pynput import mouse, keyboard

dx_total = 0
dy_total = 0
last = None

def on_move(x, y):
    global last, dx_total, dy_total
    if last:
        dx_total += x - last[0]
        dy_total += y - last[1]
    last = (x, y)

def on_press(key):
    global dx_total, dy_total
    try:
        if key.char == '1':
            print(f"Measured movement → ΔX: {dx_total}, ΔY: {dy_total}")
            dx_total = 0
            dy_total = 0
    except AttributeError:
        pass

mouse.Listener(on_move=on_move).start()
keyboard.Listener(on_press=on_press).join()


# start = 480 -10
