from utils.download import downloadWithURL
import time

url0 = 'https://www.youtube.com/watch?v=YLfkgo-3_sk'
url1 = 'cEe5NOd7bLc'

# try full url
ts = time.time()
log0 = downloadWithURL(url0, dryRun=False)
print(log0['output'])
print('download with full url, time: ' + str(time.time() - ts) )

# try id
ts = time.time()
log1 = downloadWithURL(url1, dryRun=False)
print(log1['output'])
print('download with youtube id, time: ' + str(time.time() - ts))

