import curses
from dataclasses import dataclass
from enum import Enum
import logging
import asyncio
import logging


def draw_fancy_text(ftext, parent, begin_x=1, begin_y =1, center=True):
    '''required for fancyText, draws the fancy text at specified coords or centers on parent'''
    w = ftext.index("\n")+1
    h = sum([c=="\n" for c in ftext])+1
    if center:
        begin_y, begin_x = get_center_xy(h, w, parent)
    winny = curses.newwin(h, w, begin_y, begin_x)
    winny.addstr(ftext)
    return winny

def get_center_xy(obj_h, obj_w, win):
    '''Takes in an objects h,w, and parent window, returns global start coords of object to center it'''
    begy, begx = win.getbegyx()
    curcols, curlines = win.getmaxyx()
    return begy + int(curcols/2 - obj_h/2), begx+int(curlines/2 - obj_w/2)

@dataclass
class WindowConfig:
    relative_size: int = 1
    margin: int = 0    # number of rows/cols to leave as margin inside parent window
    min_height: int = 3  # minimum size of the window
    min_width: int = 3

    def __post_init__(self):
        if self.relative_size < 0:
            raise ValueError("relative_size must be non-negative")
        if self.margin < 0:
            raise ValueError("margin must be non-negative")
        if self.min_height < 0:
            raise ValueError("min_height must be non-negative")
        if self.min_width < 0:
            raise ValueError("min_width must be non-negative")
        # if isinstance(self.parent_win, AsyncWindow):
        #     self.parent_win = self.parent_win.curses_window
        # elif not isinstance(self.parent_win, curses.window):
        #     raise TypeError("parent_win must be a curses window or AsyncWindow")

class Direction(Enum):
    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"


class AsyncWindow():
    '''A subclass of curses window that supports async updates'''

    # THE UPDATE FUNCTION SHOULD BE AN ASYNC FUNCTION and refresh the passed windows
    # The update function should handle having a cancelled_error raised when the window is destroyed
    def __init__(self, name: str, windowConfig: WindowConfig, update_function, children_direction: Direction,  children:list = [],  *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Additional initialization for async behavior can be added here
        self.name = name
        self.windowConfig = windowConfig
        self.update_function = update_function  # function to call for updates
        self.children = children
        self.children_direction = children_direction
        self.async_update_task = None  # Placeholder for the async update task
    
    def refresh_window(self):
        self.curses_window.refresh()
        logging.debug(f"Refreshed window.{self.name}")
        for child in self.children:
            child.refresh_window()

    async def create_window(self, parent_win: curses.window, weight_before: int, total_weight: int, direction: Direction):
        if self.async_update_task is not None:
            self.async_update_task.cancel()
        logging.debug(f"Creating window {self.name} with config: {self.windowConfig}, weight_before: {weight_before}, total_weight: {total_weight}")
        self.curses_window = create_window(parent_win, self.windowConfig, weight_before, total_weight, direction)
        if not self.children == []:
            children_total_weight = sum([child.windowConfig.relative_size for child in self.children])
            children_weight_before = 0
            for child in self.children:
                await child.create_window(self.curses_window, children_weight_before, children_total_weight, self.children_direction)
                children_weight_before += child.windowConfig.relative_size
        else:
            logging.debug("No children to create for this window.")
        # self.child_tasks = [asyncio.create_task(child.update_function(child)) for child in self.children]
        # asyncio.gather(*self.child_tasks)
        self.async_update_task = asyncio.create_task(self.update_function(self))

def create_window(parent_win: curses.window, windowConfig: WindowConfig, weight_before: int, total_weight: int, direction: Direction) -> curses.window:
    '''Creates a window in a specified quadrant of the parent window.
    side: Side enum indicating which side to place the window
    relative_size: float between 0 and 1 indicating size of window relative to parent
    margin: int number of rows/cols to leave as margin inside parent window
    Returns a reference to the created window.
    '''
    parent_y, parent_x = parent_win.getmaxyx()
    parent_begin_y, parent_begin_x = parent_win.getbegyx()
    relative_fraction = windowConfig.relative_size / total_weight

    if direction == Direction.VERTICAL:
        prev_wins_height = int(parent_y * (weight_before / total_weight))
        begin_y = parent_begin_y + prev_wins_height
        begin_x = parent_begin_x
        win_height = int(parent_y * relative_fraction) - (2 * windowConfig.margin)
        win_width = parent_x - (2 * windowConfig.margin)
    else:
        prev_wins_width = int(parent_x * (weight_before / total_weight))
        begin_y = parent_begin_y
        begin_x = parent_begin_x + prev_wins_width
        win_height = parent_y - (2 * windowConfig.margin)
        win_width = int(parent_x * relative_fraction) - (2 * windowConfig.margin)

    begin_y += windowConfig.margin
    begin_x += windowConfig.margin

    if win_height < windowConfig.min_height:
        logging.warning(f"Window height {win_height} is less than minimum {windowConfig.min_height}. Canceling window creation.")
        raise ValueError(f"Window height {win_height} is less than minimum {windowConfig.min_height}.")
    if win_width < windowConfig.min_width:
        logging.warning(f"Window width {win_width} is less than minimum {windowConfig.min_width}. Canceling window creation.")
        raise ValueError(f"Window width {win_width} is less than minimum {windowConfig.min_width}.")
    logging.debug(f"Creating window at ({begin_y}, {begin_x}) with size ({win_height}, {win_width})")
    new_win = curses.newwin(win_height, win_width, begin_y, begin_x)
    new_win.border('|','|', '-','-', '*', '*', '*', '*')
    return new_win

async def basic_update_function(window: AsyncWindow):
    try:
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        logging.info("Update task cancelled.")
        return