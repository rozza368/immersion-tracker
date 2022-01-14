# IDEA
This program aims to provide a user-friendly graphical way of tracking how many times episodes of separate series have been watched.
It is mainly aimed at those who are learning a language and are interested to track how much content they have watched.

# USING
User can navigate between added series.
User has the option to add new series.
To add new series, user must input name of the series as well as the number of seasons and episodes per season.

# ADD LATER
- Rename shows
- Asjust episode count

# INTERFACE
- Start screen shows available series
- Navigate using arrows or vim bindings, enter/space to select
- Show list of episodes and count watched, eg: (possibly separate season and episode?)
```
Series: Non Non Biyori
    S01E01      2
    S01E02      1
    S01E03      1
    etc
```
- Adjust count using arrow keys, vim binds

# BACKEND
- Load JSON, read series names
- Once user selects a show, load data for selected show
- In show window, edit dict in memory and edit value displayed
- Save JSON when user exits screen?/program?

# STORING
json file like this:

```
{
    "series name": {
        season#: {
            episode#: amount
        }
    }
}
```

eg:
```
{
    "Non Non Biyori": {
        1: {
            1: 1,
            2: 1,
            3: 1,
            4: 1,
            [etc]
        },
        2: {
            1: 2,
            2: 1,
            [etc]
        }
    }
}
```
