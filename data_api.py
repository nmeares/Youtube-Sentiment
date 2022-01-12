import os
import googleapiclient.discovery
import googleapiclient.errors
from functools import wraps
from pprint import pprint


# Decorator function to expand paginated responses
def _paginated(func):
    # Memorise responses and return them as a list
    combined = []
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        combined.append(response)
        try:
            pageToken = response['nextPageToken']
        except:
            pageToken = None
        kwargs['pageToken'] = pageToken
        while pageToken != None:
            try:
                combined.append(wrapper(*args, **kwargs))
            except:
                return combined
        return combined
    return wrapper

class youtube():
    
    def __init__(self, api_key, maxResults=50) -> None:
        self.api_key = api_key
        self.maxResults = maxResults
        
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        self.api_service_name = "youtube"
        self.api_version = "v3"
        self.api = googleapiclient.discovery.build(
            self.api_service_name, 
            self.api_version, 
            developerKey=self.api_key)
  
    # Retrieve stats for video specific IDs
    @_paginated
    def video_stats(self, id, pageToken=None):
        # Convert to string list
        id = ",".join(id) if isinstance(id, str) else id
        
        request = self.api.videos().list(
            part="statistics",
            id=id,
            pageToken=pageToken,
            maxResults=self.maxResults
        )
        return request.execute()

    # Retrieve list of most popular videos
    @_paginated
    def popular(self, videoCategoryId, pageToken=None):
        
        request = self.api.videos().list(
            part="snippet",
            chart="mostPopular",
            videoCategoryId=videoCategoryId,
            pageToken=pageToken,
            maxResults=self.maxResults
        )
        return request.execute()

    # Retrieve list of video categories
    @_paginated
    def VideoCategories(self, regionCode, pageToken=None):
        
        # API videoCategory list request
        request = self.api.videoCategories().list(
            part="snippet",
            regionCode=regionCode,
            pageToken=pageToken,
            maxResults=self.maxResults
        )
        response = request.execute()
        
        # Return id, title, assignable only
        categories = []
        for row in response['items']:
            categories.append({
                "id":row['id'],
                "title":row['snippet']['title'],
                "assignable":row['snippet']['assignable']
            })
        
        return categories

    # Search by category ID
    @_paginated
    def category_search(self, categoryId:int, pageToken=None):
        
        request = self.api.search().list(
            part="snippet",
            type="video",
            videoCategoryId=categoryId,
            order="viewCount",
            pageToken=pageToken,
            maxResults=self.maxResults
        )
        return request.execute()