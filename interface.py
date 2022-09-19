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


##assets
blank_face=\
    "        ____________            ____________        \n"+\
    "       /            \          /            \       \n"+\
    "      |      /\      |        |      /\      |      \n"+\
    "      |     /[]\     |        |     /[]\     |      \n"+\
    "      |     \__/     |        |     \__/     |      \n"+\
    "       \____________/          \____________/       \n"+\
    "                         /\                         \n"+\
    "                        /  \                        \n"

f_hello_world = text2art("hellow World!")
f_hi = text2art("UwU")

def get_ftext_size(fancy_text):
    w = fancy_text.index("\n")+1
    h = sum([c=="\n" for c in fancy_text])+1
    return w, h

def main(mainwin):
    # f = open("some.txt", "r+")
    # st = f.read()
    # f.close()
    # termage = climage.convert('spiderlily.png', is_unicode=False)

    update_flag= False

    def draw_mainwin(mainwin):
        mainwin.clear()
        mainwin.border('|','|', '-','-', '+', 'O', '+', '4')
        printyloc = 2
        mainwin.addstr(printyloc, 2, "Cols: " +  str(curcols)) # loc = (y, x) y = cols down , x = lines right
        mainwin.addstr(printyloc+1, 2, "Lines: " +  str(curlines))

    def create_bl_window():
        begin_x, begin_y = 1, int(curcols/2)
        bl_win = curses.newwin(int(curcols/2)-1, int(curlines/2), begin_y, begin_x)
        bl_win.border('|','|', '-','-', '+', 'O', '+', '4')
        bl_win.getbegyx()
        return bl_win

    def get_center_xy(obj_h, obj_w, win):
        begy, begx = win.getbegyx()
        curcols, curlines = win.getmaxyx()
        return begy + int(curcols/2 - obj_h/2), begx+int(curlines/2 - obj_w/2)

    def draw_fancy_text(ftext, begin_x=1, begin_y =1, center=False, parent =stdscr):
        w, h = get_ftext_size(ftext)
        if center:
            begin_y, begin_x = get_center_xy(h, w, parent)
        winny = curses.newwin(h, w, begin_y, begin_x)
        winny.addstr(ftext)
        return winny
        
    while(True):
        curcols, curlines = stdscr.getmaxyx()
        time.sleep(1)
        draw_mainwin(mainwin)
        #should I be deleting old winnys as new ones are created?
        # winny = draw_fancy_text(blank_face, center = True)
        bl_win = create_bl_window()
        blwinny = draw_fancy_text(f_hi, center=True, parent=bl_win)
        mainwin.refresh()
        bl_win.refresh()
        blwinny.refresh()
        # winny.refresh()

    



stdscr = curses.initscr()
wrapper(main)
