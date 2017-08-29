#!/usr/bin/env python

# description:
# test youtube api v3: searching videos with keywords and time limit

from utils.search_youtube import YoutubeAPI

api = YoutubeAPI()

keyword = 'YUI tokyo' #input()
numOfResults = 10
maxDuration = 10 * 60 # in seconds

try:
    res = api.search(keyword, numOfResults, maxDuration)
    print('total number of results: ' + str(len(res)))
    print('first result is: ' + res[0]['snippet']['title'] + ' from ' + res[0]['snippet']['channelTitle'])
    print('video url is: https://www.youtube.com/watch?v=' + res[0]['id'])
except:
    print('some error has accured!')




