from pynput.mouse import Controller, Button
from pynput import mouse
import keyboard

from mss import mss
import numpy as np
import time

from colorama import init, Fore, Style
import pyfiglet 

import os
import json

#*
#*      Oque-Trigger
#*      Made by fadegor05
#*      Project on Github:
#*      https://github.com/fadegor05/Oque-Trigger
#*

#* Constants
TITLE=f"{Fore.CYAN}"+pyfiglet.figlet_format("Oque-Trigger", font="slant") + f"\nv1.0.0{Style.RESET_ALL}\nMade by {Fore.GREEN}Fadeev Egor ( fadegor05 ){Style.RESET_ALL}\nProject on {Fore.GREEN}Github:{Style.RESET_ALL} https://github.com/fadegor05/Uni-Trigger\n"
DATA_FILE = 'config.json'
JSON_TEMPLATE = { "width": 1920, "height": 1080, "tp_width": 15, "tp_height": 15, "timing": 0.1, "sensitivity": 5, "key": "alt" }

#* Get json config data function
def get():
    # Get config from json file
    with open(DATA_FILE,'r') as file:
        return json.load(file)

#* Set bind key function
def bind(key):
    out = get()
    out['key'] = key
    # Rewrite keybind in json file
    with open(DATA_FILE,'w') as file:
        file.write(json.dumps(out))

#* Contain json config file function
def json_check():
    # Checking does project folder contain data file
    if not os.path.isfile(DATA_FILE):
        # Create it if not contain
        with open(DATA_FILE, 'w') as file:
            file.write(json.dumps(JSON_TEMPLATE))

#* Render title function
def title():
    # Clear console history
    os.system('cls')
    # Print project title
    print(TITLE)

#* Init function
def init():
    try:
        # Checking json file availability
        json_check()
        # Getting config data from json files
        data = get()
        # Render title function
        title()
        print(f"{Fore.GREEN}Do you want change bind from [{Style.RESET_ALL}{data['key']}{Fore.GREEN}]?{Style.RESET_ALL} [y/n]: ")
        if keyboard.read_key().lower() == "y":
            title()
            print(f"{Fore.GREEN}Enter key that you want to be binded...{Style.RESET_ALL}")
            while True:
                key = keyboard.read_key()

                if key == "esc":
                    break
                elif key != get()['key']:
                    title()
                    bind(key)
                    print(f"{Fore.GREEN}Current bind is [{Style.RESET_ALL}{key}{Fore.GREEN}]{Style.RESET_ALL}\n{Fore.GREEN}[{Style.RESET_ALL}ESC{Fore.GREEN}] to continue...{Style.RESET_ALL}")
        title()
        print(f"{Fore.GREEN}Current bind is [{Style.RESET_ALL}{get()['key']}{Fore.GREEN}]{Style.RESET_ALL}{Fore.GREEN}Done!{Style.RESET_ALL} Ready to shot...\n")
        main()
    except KeyboardInterrupt:
        pass

#* Capture frame average
def capture(data):
    screen = mss().grab({'top': (data['height']-data['tp_height'])//2, 'left': (data['width']-data['tp_width'])//2, 'width': data['tp_height'], 'height': data['tp_height']})
    return np.average(np.array(screen))

#* Main function
def main():
    data = get()
    # Saving first frame
    frame = capture(data)
    # Catching KeyboardInterrupt error
    try:
        while True:
            # Checking does activation key pressed
            if keyboard.is_pressed(data['key']):
                # Timer setup
                timer = time.time()
                # Capture new frame
                next_frame = capture(data)
                # Checking is shot needed
                if abs(next_frame - frame) > data['sensitivity']:
                    Controller().click(Button.left)
                    print(f"{Fore.GREEN}[o] {Style.RESET_ALL}Clicked within {Fore.GREEN}{str(int((time.time() - timer)*1000))}{Style.RESET_ALL} ms")
                frame = next_frame
            else:
                # Passing screen to frame
                frame = capture(data)
            time.sleep(data['timing'])
    except KeyboardInterrupt:
        pass

#* Starting Script
if __name__ == '__main__':
    init()