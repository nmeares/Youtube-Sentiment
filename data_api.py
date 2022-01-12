import os
import googleapiclient.discovery
import googleapiclient.errors
from functools import wraps
from pprint import pprint

class youtube():
    
    def __init__(self, api_key) -> None:
        self.api_key = api_key
        self.api = self.api_init(self.api_key)
    
    def api_init(self, key):
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"

        return googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=key)

    # Decorator function to expand paginated responses
    def _paginated(func):
        combined = []
        @wraps
        def wrapper(*args, **kwargs):
            response = func(*args, **kwargs)
            combined.append(response)
            pageToken = response['nextPageToken']
            kwargs['pageToken'] = pageToken
            while pageToken:
                combined.append(wrapper(*args, **kwargs))
            return combined    
        return wrapper

    # Retrieve stats for video specific IDs
    @_paginated
    def video_stats(self, id, pageToken=None):
        # Convert to string list
        id = ",".join(id) if isinstance(id, str) else id
        
        request = self.api.videos().list(
            part="statistics",
            id=id,
            pageToken=pageToken,
            maxResults=50
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
            maxResults=50
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
            maxResults=50
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
    def category_search(self, videoCategoryId:int, pageToken=None):
        
        request = self.api.search().list(
            part="snippet",
            type="video",
            videoCategoryId=videoCategoryId,
            order="viewCount",
            pageToken=pageToken,
            maxResults=50
        )
        return request.execute()