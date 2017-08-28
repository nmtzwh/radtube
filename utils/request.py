#!/usr/bin/python

import time, sys, glob
from multiprocessing import Process, Queue

from .download import downloadWithURL

class UrlRequestProcessor(object):
    def __init__(self):
        self.urlQueue = Queue()
        self.process = Process()
        self.resQueue = Queue()
    
    def checkQueueAndDownload(self, q):
        while (not q.empty()):
            u = q.get()
            result = downloadWithURL(u)
            if result['error'] == '':
                fname = result['output'].rsplit('.',1)[0]
                self.resQueue.put({
                    'id': u,
                    'file': glob.glob('./data/'+fname+'*')[0]
                    })
            else:
                self.resQueue.put({
                    'id': u,
                    'file': '',
                    'error': result['error']
                    })

    def startProcess(self):
        if not (self.urlQueue.empty() or self.process.is_alive()):
            self.process = Process(target=self.checkQueueAndDownload, args=(self.urlQueue,))
            self.process.start()

    def addUrlToQueue(self, url):
        self.urlQueue.put(url)

    
    def isFinished(self):
        return not self.process.is_alive()



