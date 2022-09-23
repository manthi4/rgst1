import os
from textwrap import wrap
import time
import curses
from curses import wrapper
import climage
from gif_for_cli.execute import execute
import sys
from art import *
from interface_utils import *


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
f_hi = text2art("Hello!")



def main(mainwin):
    def draw_mainwin(mainwin):
        mainwin.clear()
        mainwin.border('|','|', '-','-', '+', 'O', '+', '4')
        
    while(True):
        time.sleep(1)

        #init
        draw_mainwin(mainwin)
        t_win = create_t_window(mainwin)
        b_win = create_b_window(mainwin)
        bl_win = create_l_window(b_win, overlap_parent=True)
        br_win = create_r_window(b_win, overlap_parent=True)

        #write things
        printyloc = 2
        printxloc = 2
        br_win.addstr(printyloc, printxloc, "sysname:\t" +  str(os.uname()[0])) # loc = (y, x) y = cols down , x = lines right
        br_win.addstr(printyloc+1, printxloc, "node name:\t" +  str(os.uname()[1]))
        br_win.addstr(printyloc+2, printxloc, "machine:\t" + str(os.uname()[4]))
        curcols, curlines = stdscr.getmaxyx()
        br_win.addstr(printyloc+4, printxloc, "Cols: " +  str(curcols)) # loc = (y, x) y = cols down , x = lines right
        br_win.addstr(printyloc+5, printxloc, "Lines: " +  str(curlines))

        blwinny = draw_fancy_text(f_hi, center=True, parent=bl_win)
        twinny = draw_fancy_text(blank_face, center=True, parent=t_win)


        #refresh all windows
        mainwin.refresh()
        t_win.refresh()
        twinny.refresh()
        b_win.refresh()
        bl_win.refresh()
        blwinny.refresh()
        br_win.refresh()

    



stdscr = curses.initscr()
wrapper(main)
