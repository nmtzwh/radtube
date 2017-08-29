# An command line music player for Youtube

## Install

Dependancy:

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

Generate path and files (since it's private):

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

## todos

- [ ] `mpv` thread is blocking when quiting the app
- [ ] use database for better management of information
- [ ] add more playback function, e.g. shuffle, repeat
- [ ] isolate `Control` module for readability
- [ ] non-blocking download process with callback


