print("initing")
import os
from ossaudiodev import SOUND_MIXER_ALTPCM
from textwrap import wrap
import time
import curses
from curses import wrapper
import climage
from gif_for_cli.execute import execute
import sys


def main(mainwin):
    # f = open("some.txt", "r+")
    # st = f.read()
    # f.close()
    
    while(True):
        mainwin.clear()
        mainwin.border('|','|', '-','-', '+', 'O', '+', '4')
        mainwin.addstr(2, 2, "Cols: " +  str(curses.COLS))
        mainwin.addstr(3, 2, "Lines: " +  str(curses.LINES))
        # mainwin.addstr(4, 2, st)
        # execute(os.environ,["spiderlily.png"],sys.stdout)
        mainwin.refresh()

        begin_x = 20; begin_y = 7
        height = 20; width = 100
        termage = climage.convert('spiderlily.png', is_unicode=False)
        winny = curses.newwin(height, width, begin_y, begin_x)
        winny.border('x','x', 'x','x', 'O', 'O', 'O', 'O')
        winny.addstr(termage)
        winny.refresh()


curses.initscr()
wrapper(main)
