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


def add_list():
    pass


def select_show():
    # initial screen
    shows = list(watch_data)

    selected_line = 0
    selected = False

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
            show_name = shows[selected_line]
            selected = True
            break

    if selected:
        episodes_screen(show_name)


def episodes_screen(show_name):
    stdscr.clear()
    stdscr.addstr(0, 0, f"Episode List for {show_name}", curses.A_BOLD)
    episode_data = watch_data[show_name]

    episode_count = sum(len(v) for v in episode_data.values())

    selected_line = 0
    while True:
        ep_index = 0
        for season in episode_data:
            for episode in episode_data[season]:
                if ep_index == selected_line:
                    mod = curses.A_REVERSE
                    selected_season = season
                    selected_episode = episode
                else:
                    mod = curses.A_NORMAL
                # print like S01E01 with the watch count separated by spaces
                text = f"  S{season:0>2}E{episode:0>2}{' '*8}{episode_data[season][episode]}"
                # pad to fill whole screen
                stdscr.addstr(ep_index+1, 0, f"{text:<{win_width}}", mod)
                ep_index += 1
        stdscr.refresh()

        ch = stdscr.getkey()
        if ch == 'q':
            break
        elif ch == "KEY_DOWN":
            if selected_line < episode_count - 1:
                selected_line += 1
        elif ch == "KEY_UP":
            if selected_line > 0:
                selected_line -= 1
        elif ch == "KEY_LEFT":
            if watch_data[show_name][selected_season][selected_episode] > 0:
                watch_data[show_name][selected_season][selected_episode] -= 1
        elif ch == "KEY_RIGHT":
            watch_data[show_name][selected_season][selected_episode] += 1

    select_show()


select_show()


# exit program
curses.endwin()
write_file()

