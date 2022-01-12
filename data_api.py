import os
import googleapiclient.discovery
import googleapiclient.errors
from functools import wraps


# Decorator function to expand paginated responses
def _paginated(max_pages):
    def decorate(func):
        # Memorise responses and return them as a list
        combined = []
        page = 0
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal page
            while page < max_pages:
                response = func(*args, **kwargs)
                combined.append(response)
                page += 1
                try:
                    pageToken = response['nextPageToken']
                    kwargs['pageToken'] = pageToken
                    wrapper(*args, **kwargs)
                except:
                    return combined
            
            return combined
        return wrapper
    return decorate
class youtube():
    
    def __init__(self, api_key, resultsPerPage=50, maxpages=1000) -> None:
        self.api_key = api_key
        self.maxResults = resultsPerPage
        self.maxPages = maxpages
        
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
    @_paginated(self.maxPages)
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
    @_paginated(self.maxPages)
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
    @_paginated(self.maxPages)
    def VideoCategories(self, regionCode, pageToken=None):
        
        # API videoCategory list request
        request = self.api.videoCategories().list(
            part="snippet",
            regionCode=regionCode,
            pageToken=pageToken,
            maxResults=self.maxResults
        )
        return request.execute()

    # Search by category ID
    @_paginated(self.maxPages)
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