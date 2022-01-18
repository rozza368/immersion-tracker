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
curses.curs_set(0)
stdscr.keypad(True)

win_width = stdscr.getmaxyx()[1]

def select_show():
    # initial screen
    shows = list(watch_data)

    selected_line = 1

    stdscr.clear()
    stdscr.addstr(0, 0, "Shows List", curses.A_BOLD)
    while True:
        for show in range(len(shows)):
            # reverse colours of selected line
            mod = curses.A_REVERSE if show == selected_line else curses.A_NORMAL
            stdscr.addstr(show+1, 0, f"  {shows[show]}"+" "*(win_width - 2 - len(shows[show])), mod)
        stdscr.refresh()

        ch = stdscr.getkey()
        if ch == 'q':
            break
        elif ch == "KEY_DOWN":
            if selected_line < len(shows) - 1:
                selected_line += 1
        elif ch == "KEY_UP":
            if selected_line > 0:
                selected_line -= 1
        elif ch == "\n":
            # user selected a show
            show_info = watch_data[shows[selected_line]]

            stdscr.clear()
            stdscr.addstr(str(show_info))
            break


select_show()
stdscr.getch()


# exit program
curses.endwin()
write_file()

