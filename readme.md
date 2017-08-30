# A command line music player for Youtube

## Install

Dependency:

```bash
# for playback
mpv
# for converting music
ffmpeg
libvorbis

# python and libraries
python (version >= 3.5)
python-mpv
youtube-dl
google-api-python-client
isodate
```

Install from source:

```bash
git clone https://github.com/nmtzwh/radtube.git
cd radtube
git checkout ncurses

# use virtualenv
python3 -m venv ./venv
. ./venv/bin/activate

# install python dependencies
pip install -r requirements.txt
```

Generate path and files (for private data):

```bash
# in radtube root path
mkdir data
mkdir secrets

# edit /secrets/youtube.secret
echo "your youtube api key" > secrets/youtube.secret
```

Now you should be able to run the app with:

```bash
python radtube_cli.py
```

## Basic usages

Press '?' on your keyboard to view all the key-bindings.

In the beginning, you need to search for your music using '/' and 
then typing your keyword. The first 25 results will show up in your 
screen, it is time to select which one your want to put into the 
download queue by entering its number (entering anything else to cancel). 
After queuing several tracks, just press 'd' to start downloading. 
Please be patient in this step, feel free to grab a tea or coffee and chill. 

All the tracks you've downloaded are stored in `data` directory. You can 
press 'a' to view your collections and add them to playlist.
This page use the `vim` key-bindings to navigate through the database, 
i.e. 'hjkl' to look around, 'y' to add track, 'q' to quit current session.
When your playlist is not empty, you can now press lowercase 'p' to start / pause playing, 
while pressing uppercase 'P' will guide you to the current playlist.

## todos

- [ ] window resize bug
- [x] `mpv` thread is blocking when quiting the app
- [ ] use database for better management of information
- [ ] add more playback function, e.g. shuffle, repeat
- [ ] isolate `Control` module for readability
- [ ] non-blocking download process with callback


