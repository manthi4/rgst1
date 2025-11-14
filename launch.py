from assets.system_details import log_system_details, get_system_details
from assets.assets import *
from assets.window_utils import *
import logging
import curses
from curses import wrapper
import datetime
import os
import asyncio


async def update_time_window(win: AsyncWindow):
    while True:
        logging.debug(f"Updating window {win.name}")
        f_time = get_f_time()
        y, x = get_center_ftext(f_time, win.curses_window)
        win.curses_window.addstr(y, x, f_time)
        win.refresh_window()
        await asyncio.sleep(1)

async def add_system_details_to_window(asyncWin: AsyncWindow):
    try:
        system_details = get_system_details()
        lines = [
            f"OS:\t\t" + system_details['os_name'],
            f"host name:\t" +system_details['hostname'],
            "Total RAM:\t" + str(system_details['total_ram_gb'])+ " GB",
            "Free disk:\t" + str(system_details['free_disk_gb']) + " GB",
        ]
        printxloc = 2
        current_line = 2
        for line in lines:
            asyncWin.curses_window.addstr(current_line, printxloc, line)
            current_line += 1
        asyncWin.curses_window.refresh()
    except asyncio.CancelledError:
        logging.debug("System details update task cancelled.")
        return
    except Exception as e:
        logging.warning(f"Could not add system details to window: {e}")
    

async def core_ui(mainwin):
    
    # Initialize init state
    system_details = get_system_details()
    curcols, curlines = mainwin.getmaxyx()

    # Initialize windows
    ##TODO: Make this more dynamic/declarative
    def refresh_mainwin(mainwin):
        mainwin.clear()
        mainwin.border('|','|', '-','-', '+', 'O', '+', '4')
    refresh_mainwin(mainwin)

    base_win = AsyncWindow("base_win", WindowConfig(margin=0), update_function=basic_update_function, children_direction=Direction.VERTICAL)
    t_win = AsyncWindow("top win", WindowConfig(margin=1), update_function=basic_update_function, children_direction=Direction.VERTICAL)
    b_win = AsyncWindow("bottom_win", WindowConfig(margin=1), update_function=basic_update_function, children_direction=Direction.HORIZONTAL)
    bl_win = AsyncWindow("bl_win", WindowConfig(relative_size = 4, margin=1), update_function=basic_update_function, children_direction=Direction.HORIZONTAL)
    br_win = AsyncWindow("br_win", WindowConfig(relative_size = 6, margin=1), update_function=update_time_window, children_direction=Direction.HORIZONTAL)

    base_win.children = [t_win, b_win]
    b_win.children = [bl_win, br_win]

    mainwin.refresh()
    await base_win.create_window(mainwin, 0, 1, Direction.VERTICAL)
    base_win.refresh_window()
    while True:
        await asyncio.sleep(10)

    # t_win = create_window(WindowConfig(parent_win=mainwin, side=Side.TOP))
    # b_win = create_window(WindowConfig(parent_win=mainwin, side=Side.BOTTOM))
    # bl_win = create_window(WindowConfig(parent_win=b_win, side=Side.LEFT, relative_size=0.6))
    # br_win = create_window(WindowConfig(parent_win=b_win, side=Side.RIGHT, relative_size=0.4))

    

    # Each window should also have its own task to update its contents

    # while(True):
    #     time.sleep(1)

        #init
        # lines = [
        #     f"OS:\t\t" + system_details['os_name'],
        #     f"host name:\t" +system_details['hostname'],
        #     "Total RAM:\t" + str(system_details['total_ram_gb'])+ " GB",
        #     "Free disk:\t" + str(system_details['free_disk_gb']) + " GB",
        #     "Cols: " +  str(curcols),
        #     "Lines: " +  str(curlines),
        # ]
        # #write things
        # printxloc = 2
        # current_line = 2
        # for line in lines:
        #     br_win.addstr(current_line, printxloc, line)
        #     current_line += 1

        # f_time = get_f_time()
        # blwinny = draw_fancy_text(f_time, center=True, parent=bl_win)
        # twinny = draw_fancy_text(blank_face, center=True, parent=t_win)


        # #refresh all windows
        # mainwin.refresh()
        # t_win.refresh()
        # twinny.refresh()
        # b_win.refresh()
        # bl_win.refresh()
        # blwinny.refresh()
        # br_win.refresh()

def main(mainwin):
    logging.info("Starting system details logging...")
    log_system_details()
    asyncio.run(core_ui(mainwin))


if __name__ == "__main__":
    now = datetime.datetime.now()
    formatted_time = now.strftime("%Y_%m_%d_%H_%M_%S" )
    logging.basicConfig(filename=f'./logs/{formatted_time}_logs.log', level=logging.DEBUG)
    logging.debug("Launching application...")
    wrapper(main)