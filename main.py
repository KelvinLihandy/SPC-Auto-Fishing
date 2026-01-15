import time
import pyautogui
import pytesseract
from itertools import product

TYPING_DELAY = 0.25
SEQUENCES = [
    "".join(p) for p in product(["L", "R"], repeat=4)
]

def condense():

            # add move to crafting table here
            
            for _ in range(10):
                pyautogui.click(button="right")
                x, y = pyautogui.position()
                print(f"Right-click at ({x}, {y})")
                time.sleep(0.5) # wait cooldown condense
            print('condensed')

def fishing_loop():
    counter = 0
    while True:
        if(counter > 10):
            condense()
            counter = 0
        pyautogui.click(button="right")
        
        # wait catch done
        
        time.sleep(0.5)
        counter += 1
        print(f'fishing loop {counter}')

def main():
    fishing_loop()

if __name__ == "__main__":
    main()