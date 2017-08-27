#!/usr/bin/python

import youtube_dl
import subprocess

class SimpleLogger(object):
    def __init__(self):
        self.mDebug = ""
        self.mWarn = ""
        self.mError = ""
        self.mOutput = ""

    def debug(self, msg):
        self.mDebug = msg
    
    def warning(self, msg):
        self.mWarn = msg

    def error(self, msg):
        self.mError = msg

    def statusHook(self, d):
        if d['status'] == 'finished':
            self.mOutput = d['filename'] 
        elif d['status'] == 'error':
            self.mOutput = 'ERROR!'

def downloadWithURL(input_url, outPath='./data/', dryRun=False):
    logger = SimpleLogger()

    ydl_opts = {
            'simulate': dryRun,
            'format': 'bestaudio/best',
            'postprocessors': [
                {   
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'best',
                    'preferredquality': '5'
                },
                {
                    'key': 'ExecAfterDownload',
                    'exec_cmd': (
                        'ffmpeg -i {} ' + 
                        '-ar 44100 -qscale:a 4 ' + 
                        outPath + '{}.ogg ' + 
                        '&& rm {}'
                        )
                }
            ],
            'logger': logger,
            'progress_hooks': [logger.statusHook]
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([input_url])
    
    return { 'output': logger.mOutput, 
             'debug' : logger.mDebug, 
             'warning' : logger.mWarn, 
             'error' : logger.mError}

# def convertToOgg(filename, musicPath='./data/'):
    # cmd = ('ffmpeg -i ' + filename + 
            # ' -ar 44100 -qscale:a 4 ' + 
            # musicPath + filename.rsplit('.', 1)[0] + '.ogg' +
            # ' && rm ' + filename)
    # proc = subprocess.Popen(cmd, 
            # shell=True, 
            # stdin=subprocess.PIPE, 
            # stderr=subprocess.PIPE, 
            # stdout=subprocess.PIPE)


