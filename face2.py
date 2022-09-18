print("initing")
import os
from textwrap import wrap
import time
import curses
from curses import wrapper

def main(mainwin):
    print("starting")
    
    mainwin.clear()
    mainwin.border('|','|', '-','-', '+', 'O', '+', '4')
    mainwin.refresh()

wrapper(main)