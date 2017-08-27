from utils.search_youtube import YoutubeAPI
from utils.request import UrlRequestProcessor
import time, random

keywords = ['gumi', '真赤goosehouse', 'to the beginning', '魔法って言っていいかな']

api = YoutubeAPI()
pool = UrlRequestProcessor()

numOfResults = 10
maxDuration  = 10 * 60

ts = time.time()

for k in keywords:
    try:
        searchResults = api.search(k, numOfResults, maxDuration)
        # simulate user select
        url = searchResults[random.randint(0, len(searchResults))]
        if (len(url) == 0):
            print('cannot find results from keyword ' + k)
            continue
        # push to queue and random sleep 
        print('downloading ' + url['snippet']['title'] + ' at: ' + str(time.time() - ts))
        pool.addUrlToQueue(url['id'])
        pool.startProcess()
        time.sleep(random.randint(5,20))
    except:
        print('some error happened ...')
        raise
        #continue

while(True):
    if pool.isFinished():
        print('finish downloading: ' + str(time.time() - ts))
        break
    time.sleep(5)

