#!/usr/bin/python

from apiclient.discovery import build
from isodate import parse_duration

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.

class YoutubeAPI:
    def __init__(self):
        with open('secrets/youtube.secret', 'r') as f:
            self.DEVELOPER_KEY = f.readline().split('\n')[0]

        self.YOUTUBE_API_SERVICE_NAME = 'youtube'
        self.YOUTUBE_API_VERSION = 'v3'
        # api initialization
        self.youtube = build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION,
                developerKey=self.DEVELOPER_KEY)
    
    def search(self, query, max_results=25, max_duration=1200):
        # Call the search.list method to retrieve results matching the specified
        # query term.
        search_response = self.youtube.search().list(
                q=query,
                part='id,snippet',
                maxResults=max_results,
                type='video',
                ).execute()

        # Add each result to the appropriate list, and then display the lists of
        temp_results = search_response.get('items', [])

        # loop these videos and get ids
        ids = []
        for res in temp_results:
            if res['id']['kind'] == 'youtube#video':
                ids.append(res['id']['videoId'])
        
        # query for video details and filter by duration
        video_response = self.youtube.videos().list(
                part='snippet,contentDetails,statistics',
                id=','.join(ids)
                ).execute()

        videos = []

        for res in video_response.get('items', []):
            duration = res['contentDetails']['duration']
            if (parse_duration(duration).total_seconds() <= max_duration):
                videos.append(res)

        return videos

