from utils.request import UrlRequestProcessor
import time

urlPool = UrlRequestProcessor()

urlList = ['UGG7tUMg77A', 'NiIVTXTuQug', '46MIgupU8UY', '06d8SwcSm_Q'] 

# insert urls in a loop
ts = time.time()

for u in urlList:
    print('adding: ' + u)
    urlPool.addUrlToQueue(u)
    urlPool.startProcess()
    print('start .. process at: ' + str(time.time() - ts))
    time.sleep(1)

while(True):
    if urlPool.isFinished():
        print('finish downloading: ' + str(time.time() - ts))
        break
    time.sleep(5)





