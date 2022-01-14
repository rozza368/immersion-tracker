import curses
import json
import os

save_file = "shows.json"

if os.path.exists(save_file):
    with open(save_file, "r") as f:
        watch_data = json.load(f)
else:
    watch_data = {}


def write_file():
    with open(save_file, "w") as f:
        json.dump(watch_data, f, indent=2)

# start curses
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)

stdscr.clear()

# initial screen
shows = list(watch_data)

stdscr.addstr(0, 0, "Shows List", curses.A_BOLD)

win_width = stdscr.getmaxyx()[1]

selected_line = 1

keys_pressed = []

while True:
    for show in range(len(shows)):
        if show == selected_line:
            mod = curses.A_REVERSE
        else:
            mod = curses.A_NORMAL
        stdscr.addstr(show+1, 0, f"  {shows[show]}"+" "*(win_width - 2 - len(shows[show])), mod)
    stdscr.refresh()

    ch = stdscr.getkey()
    keys_pressed.append(ch)
    if ch == 'q':
        break
    elif ch == "KEY_DOWN":
        if selected_line < len(shows) - 1:
            selected_line += 1
    elif ch == "KEY_UP":
        if selected_line > 0:
            selected_line -= 1
    elif ch == "\n":
        stdscr.addstr(str(selected_line))



# exit program
curses.endwin()
write_file()

