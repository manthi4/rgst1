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
from art import *


def main(mainwin):
    # f = open("some.txt", "r+")
    # st = f.read()
    # f.close()
    curcols, curlines = stdscr.getmaxyx()
    hewo = text2art("hello!")
    hewo_w = 30
    hewo_h = 7
    def draw_mainwin(mainwin):
        mainwin.clear()
        mainwin.border('|','|', '-','-', '+', 'O', '+', '4')
        printyloc = 2
        mainwin.addstr(printyloc, 2, "Cols: " +  str(curcols)) # loc = (y, x) y = cols down , x = lines right
        mainwin.addstr(printyloc+1, 2, "Lines: " +  str(curlines))

    def create_winny():
        begin_x = int(curlines/2 - hewo_w/2)
        begin_y = int(curcols/2 - hewo_h/2)
        height = hewo_h
        width = hewo_w #try not use fixed widths
        termage = climage.convert('spiderlily.png', is_unicode=False)
        winny = curses.newwin(height, width, begin_y, begin_x)
        return winny
        
    def draw_winny(winny):
        winny.clear()
        winny.border('x','x', 'x','x', 'O', 'O', 'O', 'O')
        winny.addstr(hewo)
        # winny.addstr(termage)
        # winny.refresh()

    
    winny = create_winny()
    while(True):
        # mainwin.clear()
        # if curlines != str(curses.LINES) or currcols != str(curses.COLS):
        #     printyloc += 2
        #     currcols = str(curses.COLS)
        #     curlines = str(curses.LINES)
        #     mainwin.addstr(printyloc, 2, "Cols: " +  currcols) # loc = (y, x) y = cols down , x = lines right
        #     mainwin.addstr(printyloc+1, 2, "Lines: " +  curlines)
        curcols, curlines = stdscr.getmaxyx()
        time.sleep(1)
        draw_mainwin(mainwin)
        draw_winny(winny)
        mainwin.refresh()
        winny.refresh()






stdscr = curses.initscr()
wrapper(main)
