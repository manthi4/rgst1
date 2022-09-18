print("hello")

import climage
import os
import time
import curses

def clear():
    os.system("cls||clear")

while(True):
    termage = climage.convert('spiderlily.png')
    print("hey", "qt")
    print("break"+ termage)
    time.sleep(1)
    clear()
    time.sleep(1)
    curses.beep()
