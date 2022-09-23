import curses

def draw_fancy_text(ftext, parent, begin_x=1, begin_y =1, center=False):
    '''required for fancyText, draws the fancy text at specified coords or centers on parent'''
    w, h = get_ftext_size(ftext)
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

def get_ftext_size(fancy_text):
    '''Takes in a text2art obj from art lib, outputs width, height'''
    w = fancy_text.index("\n")+1
    h = sum([c=="\n" for c in fancy_text])+1
    return w, h

def create_t_window(win, overlap_parent= False):
    '''Creates a window in the bottom half of the parent, and returns a ref'''
    parent_y, parent_x = win.getmaxyx()
    p_beg_cols, p_beg_lines = win.getbegyx()
    begin_x = p_beg_lines +  (0 if overlap_parent else 1)
    begin_y = p_beg_cols +  (0 if overlap_parent else 1)
    width_x = parent_x - (0 if overlap_parent else 2)
    height_y = int(.5+ parent_y/2) - (0 if overlap_parent else 2)
    bl_win = curses.newwin(height_y, width_x, begin_y, begin_x)
    bl_win.border('|','|', '-','-', '+', 'O', '+', '4')
    return bl_win

def create_b_window(win, overlap_parent= False):
    '''Creates a window in the bottom half of the parent, and returns a ref'''
    parent_cols, parent_lines = win.getmaxyx()
    p_beg_cols, p_beg_lines = win.getbegyx()
    begin_x = p_beg_lines +  (0 if overlap_parent else 1)
    begin_y = int(.5+parent_cols/2)+p_beg_cols - (0 if overlap_parent else 1)
    width_x = parent_lines - (0 if overlap_parent else 2)
    height_y = int(.5+ parent_cols/2)
    bl_win = curses.newwin(height_y, width_x, begin_y, begin_x)
    bl_win.border('|','|', '-','-', '+', 'O', '+', '4')
    return bl_win

def create_l_window(win, overlap_parent= False):
    '''Creates a window in the left half of the parent, and returns a ref'''

    parent_y, parent_x = win.getmaxyx()
    p_beg_cols, p_beg_lines = win.getbegyx()
    begin_x = p_beg_lines +  (0 if overlap_parent else 1)
    begin_y = p_beg_cols +  (0 if overlap_parent else 1)
    width_x = int(.5+ parent_x/2) - (0 if overlap_parent else 1)
    height_y = parent_y- (0 if overlap_parent else 2)
    bl_win = curses.newwin(height_y, width_x, begin_y, begin_x)
    bl_win.border('|','|', '-','-', '*', '*', '*', '*')
    bl_win.getbegyx()
    return bl_win

def create_r_window(win, overlap_parent= False):
    '''Creates a window in the right half of the parent, and returns a ref'''

    parent_y, parent_x = win.getmaxyx()
    p_beg_cols, p_beg_lines = win.getbegyx()
    begin_x = p_beg_lines + int(.5+parent_x/2)
    begin_y = p_beg_cols +  (0 if overlap_parent else 1)
    width_x = int(.5+ parent_x/2) - (0 if overlap_parent else 1)
    height_y = parent_y- (0 if overlap_parent else 2)
    bl_win = curses.newwin(height_y, width_x, begin_y, begin_x)
    bl_win.border('|','|', '-','-', '*', '*', '*', '*')
    bl_win.getbegyx()
    return bl_win