# Immersion Tracker
Track how many of each episode of different series you have watched.

# Installation
Immersion Tracker does not require any additional Python packages to be installed, but it does require a UNIX-like operating system like Mac, Linux or OpenBSD that has the ncurses library.
Clone the repo or download and extract the ZIP, then change directory to the folder and run
```sh
python3 main.py
```
* on Windows or other operating systems, you may have to use `py` or `python` instead of `python3`

# Usage
Vim binds or arrow keys can be used to navigate.
### Shows List Screen
- q : quit
- ↑ / k : up
- ↓ / j : down
- ENTER : select highlighted series
- n : add new series
- r : rename highlighted series
- d : delete highlighted series
### Episode List Screen
- q : back to shows list
- ↑ / k : up
- ↓ / j : down
- ← / h : decrease watch count
- → / l : increase watch count

# TODO
- Add ability to edit season/episode count
- Display total time watched for each season as well as a grand total
- Remember currently highlighted selection between sessions
- Redesign UI for better usability and readability

