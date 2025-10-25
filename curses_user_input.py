import curses
import textwrap

def get_wrapped_input(stdscr, prompt="Enter text (press Enter to finish):"):
    curses.curs_set(1)
    stdscr.clear()
    stdscr.addstr(0, 0, prompt)
    stdscr.refresh()

    max_y, max_x = stdscr.getmaxyx()
    input_top = 1
    max_input_height = max_y - input_top - 1  # Reserve last line for buffer or messages

    input_text = ""
    cursor_pos = 0

    scroll_offset = 0

    while True:
        # Wrap input text into lines based on current terminal width
        wrapped_lines = textwrap.wrap(input_text, width=max_x)
        total_lines = len(wrapped_lines)

        # Determine current cursor position (row, col) based on wrapped text
        char_count = 0
        cursor_row, cursor_col = 0, 0
        for i, line in enumerate(wrapped_lines):
            if cursor_pos <= char_count + len(line):
                cursor_row = i
                cursor_col = cursor_pos - char_count
                break
            char_count += len(line)

        # Handle scrolling
        if cursor_row >= scroll_offset + max_input_height:
            scroll_offset = cursor_row - max_input_height + 1
        elif cursor_row < scroll_offset:
            scroll_offset = cursor_row

        # Redraw input area
        for i in range(max_input_height):
            stdscr.move(input_top + i, 0)
            stdscr.clrtoeol()
            line_index = scroll_offset + i
            if 0 <= line_index < total_lines:
                stdscr.addstr(input_top + i, 0, wrapped_lines[line_index])

        # Place the cursor
        stdscr.move(input_top + cursor_row - scroll_offset, cursor_col)
        stdscr.refresh()

        key = stdscr.getch()

        if key in (10, 13):  # Enter key
            break
        elif key in (curses.KEY_BACKSPACE, 127, 8):
            if cursor_pos > 0:
                input_text = input_text[:cursor_pos - 1] + input_text[cursor_pos:]
                cursor_pos -= 1
        elif 32 <= key <= 126:  # Printable characters
            input_text = input_text[:cursor_pos] + chr(key) + input_text[cursor_pos:]
            cursor_pos += 1
        # Optionally, add left/right arrow key handling
        elif key == curses.KEY_LEFT and cursor_pos > 0:
            cursor_pos -= 1
        elif key == curses.KEY_RIGHT and cursor_pos < len(input_text):
            cursor_pos += 1

    curses.curs_set(0)
    return input_text


def main(stdscr):
    user_input = get_wrapped_input(stdscr)
    stdscr.clear()
    stdscr.addstr(0, 0, "You entered:\n")
    wrapped_output = textwrap.wrap(user_input, width=curses.COLS)
    for idx, line in enumerate(wrapped_output):
        stdscr.addstr(idx + 1, 0, line)
    stdscr.addstr(len(wrapped_output) + 2, 0, "Press any key to exit...")
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)
