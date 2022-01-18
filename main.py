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

help_texts = {
    "NAVIGATE": "navigate: ↑ / ↓",
    "SELECT": "select: ENTER",
    "NEW": "add new: n",
    "QUIT": "quit: q",
    "BACK": "back: q",
    "DELETE": "delete: d",
    "RENAME": "rename: r",
    "ADJUST": "adjust: ← / →"
}

# start curses
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
curses.curs_set(0)
stdscr.keypad(True)

win_height, win_width = stdscr.getmaxyx()


def add_list():
    pass


def print_help_bar(win, options):
    help_text = help_texts[options[0]]
    for o in options[1:]:
        help_text += " " * 4 + help_texts[o]

    win.addstr(win_height - 1, 0, f"{help_text:^{win_width-1}}", curses.A_BOLD)


def create_box(text, title):
    box_w = win_width // 2
    box_h = 7
    x_pos = win_width // 4
    y_pos = win_height // 4

    box = curses.newwin(box_h, box_w, y_pos, x_pos)
    box.keypad(True)

    box.box()
    box.addstr(0, 2, title)

    box.addstr(2, 3, text)

    return box


def delete_box(box):
    del box
    stdscr.touchwin()
    stdscr.refresh()


def input_box(text, title="Input"):
    curses.echo()
    curses.curs_set(1)
    box = create_box(text, title)

    box.addstr(4, 3, " " * (box.getmaxyx()[1] - 6), curses.A_UNDERLINE)
    box.move(4, 3)

    stdscr.refresh()
    box.refresh()

    text_entered = box.getstr()

    delete_box(box)

    curses.curs_set(0)
    curses.noecho()

    # input comes in bytes, so decode it
    return text_entered.decode("utf-8")


def confirm_box(text):
    box = create_box(text, "Confirm")
    choice = False
    while True:
        box.addstr(4, 3, "Yes", curses.A_STANDOUT if choice else curses.A_NORMAL)
        box.addstr(4, 9, "No", curses.A_NORMAL if choice else curses.A_STANDOUT)
        box.refresh()

        ch = box.getkey()
        if ch == "KEY_LEFT":
            choice = True
        elif ch == "KEY_RIGHT":
            choice = False
        elif ch == '\n':
            break
    
    delete_box(box)

    return choice


def select_show():
    # initial screen
    shows = list(watch_data)

    selected_line = 0
    selected = False

    stdscr.clear()
    stdscr.addstr(0, 0, "Shows List", curses.A_BOLD)
    help_text = "navigate: ↑ / ↓        select: ENTER        add new: n        quit: q"
    print_help_bar(stdscr, ("NAVIGATE", "SELECT", "NEW", "RENAME", "DELETE", "QUIT"))
    while True:
        for show in range(len(shows)):
            mod = curses.A_STANDOUT if show == selected_line else curses.A_NORMAL
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

        elif ch == 'n':
            new_name = input_box("Enter series name:", "New Series")
            if new_name and new_name not in watch_data:
                watch_data[new_name] = {}
                num_seasons = input_box("Enter the number of seasons:", "Seasons")
                while not num_seasons.isnumeric():
                    num_seasons = input_box("Please enter an integer amount of seasons.", "Seasons")
                num_seasons = int(num_seasons)

                for season in range(1, num_seasons + 1):
                    watch_data[new_name][str(season)] = {}
                    num_episodes = input_box(f"Enter the number of episodes in season {season}:", "Episodes")
                    while not num_episodes.isnumeric():
                        num_episodes = input_box(f"Please enter an integer number of episodes for season {season}.", "Episodes")
                    num_episodes = int(num_episodes)
                    for e in range(1, num_episodes + 1):
                        watch_data[new_name][str(season)][e] = 0

            # need to reload shows list
            shows = list(watch_data)

        elif ch == 'd':
            if confirm_box(f"Permanently delete data for the show \"{shows[selected_line]}\"?"):
                del watch_data[shows[selected_line]]
                stdscr.move(len(shows), 0)
                stdscr.clrtoeol()
            shows = list(watch_data)

        elif ch == 'r':
            new_name = input_box(f"Input a new name for {shows[selected_line]}:", "Rename")
            if new_name:
                watch_data[new_name] = watch_data.pop(shows[selected_line])
                shows = list(watch_data)

        elif ch == '\n':
            # user selected a show
            show_name = shows[selected_line]
            selected = True
            break

    if selected:
        episodes_screen(show_name)


def episodes_screen(show_name):
    stdscr.clear()
    stdscr.addstr(0, 0, f"Episode List for {show_name}", curses.A_BOLD)
    stdscr.addstr(1, 0, "  Episode       Watch Count")
    print_help_bar(stdscr, ("NAVIGATE", "ADJUST", "BACK"))
    episode_data = watch_data[show_name]

    episode_count = sum(len(v) for v in episode_data.values())

    selected_line = 0
    while True:
        ep_index = 0
        for season in episode_data:
            for episode in episode_data[season]:
                if ep_index == selected_line:
                    mod = curses.A_STANDOUT
                    selected_season = season
                    selected_episode = episode
                else:
                    mod = curses.A_NORMAL
                # print like S01E01 with the watch count separated by spaces
                text = f"  S{season:0>2}E{episode:0>2}{' '*8}{episode_data[season][episode]}"
                # pad to fill whole screen
                stdscr.addstr(ep_index+2, 0, f"{text:<{win_width}}", mod)
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

