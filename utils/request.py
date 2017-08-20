#!/usr/bin/python

import time, sys
from multiprocessing import Process, Queue

from .download import downloadWithURL

class UrlRequestProcessor(object):
    def __init__(self):
        self.urlQueue = Queue()
        self.process = Process()
    
    def checkQueueAndDownload(self, q):
        results = []
        while (not q.empty()):
            results.append(downloadWithURL(q.get()))
        return results

    def startProcess(self):
        if not (self.urlQueue.empty() or self.process.is_alive()):
            self.process = Process(target=self.checkQueueAndDownload, args=(self.urlQueue,))
            self.process.start()

    def addUrlToQueue(self, url):
        self.urlQueue.put(url)

    
    def isFinished(self):
        return not self.process.is_alive()



