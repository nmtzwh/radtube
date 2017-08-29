#!/usr/bin/env python

# try to build a command line youtube music
# lessons learned:
# + use getstr for unicode input
# + re-encoding the getstr output 

import curses
from curses.textpad import Textbox

import time, glob

# unicode support 
import locale
locale.setlocale(locale.LC_ALL, '')

# utils
from utils.search_youtube import YoutubeAPI
from utils.request import UrlRequestProcessor
from mpv import MPV


class Control(object):
    def __init__(self, db):
        self.api = YoutubeAPI()
        self.pool = UrlRequestProcessor()
        self.urlQueue = []
        self.DB = db
        self.player = MPV()
        
    def doSearchAndUpdate(self, key, win):
        try:
            result = self.api.search(key)
        except:
            raise
        win.clear()
        y, x = win.getmaxyx()
        for i in range(0, min(y-1, len(result))):
            win.addnstr(i+1, 0, str(i) + ': ' + 
                    result[i]['snippet']['title'], x)
        win.addstr(0, 0, 'Choose video number: ', curses.A_REVERSE)
        win.noutrefresh()
        curses.doupdate()
        curses.echo()
        num = win.getstr().decode(encoding='utf-8')
        curses.noecho()
        if num.isdigit() and int(num)<len(result):
            entry = result[int(num)]
            self.pool.addUrlToQueue(entry['id'])
            self.urlQueue.append({'title': entry['snippet']['title'], 'id': entry['id']})
        # display current queue
        self.displayQueue(win)

    def startDownload(self, win):
        win.clear()
        self.urlQueue = []
        self.pool.startProcess()
        # draw info
        win.addstr(0,0, 'Start downloading: ', curses.A_REVERSE)
        ts = time.time()
        while not self.pool.isFinished():
            win.addstr(1, 0, str(int(time.time()-ts)) + ' sec ... please be patient')
            win.noutrefresh()
            curses.doupdate()
            time.sleep(5)
        win.addstr(1, 0, 'Download finished in ' +  str(int(time.time()-ts)) + ' seconds')
        win.noutrefresh()
        curses.doupdate()
        # insert song into database
        self.refreshDB()

    def displayQueue(self, win):
        win.clear()
        y, x = win.getmaxyx()
        for i in range(0, min(y-1, len(self.urlQueue))):
            win.addnstr(i+1, 0, self.urlQueue[i]['id'] + ': ' + 
                    self.urlQueue[i]['title'], x)
        win.addstr(0, 0, 'Currently in queue: ', curses.A_BOLD)
        win.noutrefresh()
        curses.doupdate()

    def showHelp(self, win):
        win.clear()
        win.addstr(0, 0, 'Available command: ', curses.A_REVERSE)
        win.addstr(1, 0, '+ type \'/\' to begin a search; ')
        win.addstr(2, 0, '+ type \'d\' to begin downloading; ')
        win.addstr(3, 0, '+ type \'p\' to play or pause; ')
        win.addstr(4, 0, '+ type \'a\' to modify playlist')
        win.addstr(5, 0, '+ type \'q\' to quit; ')
        win.addstr(6, 0, '+ type \'?\' to show this message. ')
        win.noutrefresh()
        curses.doupdate()

    def refreshDB(self):
        while not self.pool.resQueue.empty():
            # dumb db: need ... modification
            self.DB.append(self.pool.resQueue.get())

    def playlistChange(self, win):
        win.clear()
        page = 0
        lineNum = 0
        y, x = win.getmaxyx()
        pageMax = len(self.DB) // (y-1) + 1
        n = len(self.DB)
        # list songs in database
        def listPage(p):
            win.clear()
            win.addstr(0, 0, 'Database: \'hjkl\' move around, \'y\' add, \'q\' quit', curses.A_REVERSE)
            for i in range(p*(y-1), min(n, (p+1)*(y-1))):
                win.addnstr(i+1-p*(y-1), 0, self.DB[i]['file'], x)
            imax = i + 1 - p * (y - 1)
            win.chgat(lineNum % imax + 1, 0, -1, curses.A_BLINK)
            win.move(0, 0)
            win.noutrefresh()
            curses.doupdate()
            return imax, lineNum % imax
        # initialize 
        lineMax, lineNum = listPage(page)
        # wait for keypress
        while (True):
            k = win.getch()
            if k == ord('q'):
                break
            if k == ord('j'):
                win.chgat(lineNum+1, 0, -1, curses.A_NORMAL)
                lineNum = (lineNum + 1) % lineMax
                win.chgat(lineNum+1, 0, -1, curses.A_BLINK)
                win.noutrefresh()
                curses.doupdate()
            if k == ord('k'):
                win.chgat(lineNum+1, 0, -1, curses.A_NORMAL)
                lineNum = (lineNum - 1) % lineMax
                win.chgat(lineNum+1, 0, -1, curses.A_BLINK)
                win.noutrefresh()
                curses.doupdate()
            if k == ord('h'):
                page = (page - 1) % pageMax
                lineMax, lineNum = listPage(page)
            if k == ord('l'):
                page = (page + 1) % pageMax
                lineMax, lineNum = listPage(page)
            if k == ord('y'):
                item = page * (y-1) + lineNum
                self.player.playlist_append(self.DB[item]['file'])
    
    def playOrPauseMusic(self, win):
        if self.player.playlist_count == 0:
            return
        if self.player.playlist_pos == None:
            self.player.playlist_pos = 0
            return
        self.player.pause = not self.player.pause
        # update window info
        win.clear()
        y, x = win.getmaxyx()
        win.addstr(0, 0, 'Current playlist: ', curses.A_REVERSE)
        for i in range(0, min(y-1, self.player.playlist_count)):
            win.addnstr(i+1, 0, self.player.playlist[i]['filename'], x)
        win.addstr(0, 20, ('paused' if self.player.pause else 'playing'))
        win.noutrefresh()
        curses.doupdate()

    def quit(self):
        # self.player.playlist_clear
        self.player.quit()
        


def main(stdscr):
    # clear screen
    stdscr.clear()

    # initialize control
    audioFiles = glob.glob('./data/*.ogg')
    dumbDB = [ {'file': f} for f in audioFiles ]
    control = Control(dumbDB)

    # add the title and bottom line
    stdscr.addstr('Youtube Music CLI', curses.A_REVERSE)
    stdscr.chgat(-1, curses.A_REVERSE)
    stdscr.addstr(curses.LINES-1, 0, 'Press \'?\' for help, press \'q\' to exit')
    
    # create main window
    main_window = curses.newwin(curses.LINES-5, curses.COLS, 1,0)
    main_window_vis = main_window.subwin(curses.LINES-7, curses.COLS-4, 2, 2)
    main_window.box()
    control.showHelp(main_window_vis)

    # create input field
    text_window = curses.newwin(3, curses.COLS, curses.LINES-4, 0)
    text_window.addstr(1, 2, 'search here: ')
    text_window.box()

    text_window_vis = text_window.subwin(1, curses.COLS-20, curses.LINES-3, 15) 

    # refresh
    stdscr.noutrefresh()
    main_window.noutrefresh()
    text_window.noutrefresh()
    curses.doupdate()

    # main loop
    while (True):
        k = main_window.getch()
        # response to key press
        if k == ord('q'):
            control.quit()
            break
        if k == ord('?'):
            control.showHelp(main_window_vis)
        if k == ord('/'):
            curses.echo()
            sKey = text_window_vis.getstr().decode(encoding='utf-8') 
            curses.noecho()
            control.doSearchAndUpdate(sKey, main_window_vis)
            text_window_vis.clear()
            text_window_vis.noutrefresh()
            curses.doupdate()
        if k == ord('d'):
            # start downloading 
            control.startDownload(main_window_vis)
        if k == ord('p'):
            control.playOrPauseMusic(main_window_vis)
        if k == ord('a'):
            control.playlistChange(main_window_vis)

if __name__ == '__main__':
    curses.wrapper(main)
