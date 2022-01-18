import os
import googleapiclient.discovery
import googleapiclient.errors
from functools import wraps

# Decorator function to expand paginated responses
def _paginated(max_pages):
    def decorate(func):
        # Memorise responses and return them as a list
        combined = []
        page = 1
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal page
            while page <= max_pages:
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
    
    def __init__(self, api_key, resultsPerPage=50, maxPages=1000) -> None:
        self.api_key = api_key
        self.maxResults = resultsPerPage
        self.maxPages = maxPages
        
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        self.api_service_name = "youtube"
        self.api_version = "v3"
        self.api = googleapiclient.discovery.build(
            self.api_service_name, 
            self.api_version, 
            developerKey=self.api_key)
  

    # Retrieve stats for video specific IDs (max 50)
    def video_stats(self, id, pageToken=None):
        values = []
        # Chunk the list by 50 to remain within query limits
        id_lst = [id[i:i + 50] for i in range(0, len(id), 50)]
        # Loop chunked list
        for ids in id_lst:
            # Convert to string list
            id = ",".join(ids) if isinstance(ids, list) else ids
            
            request = self.api.videos().list(
                part="statistics",
                id=id,
                pageToken=pageToken,
                maxResults=self.maxResults
            )
            values.append(request.execute())
        return values

    # Retrieve list of most popular videos
    @_paginated(2) # Increase paginate in prod
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
    def VideoCategories(self, regionCode):
        
        # API videoCategory list request
        request = self.api.videoCategories().list(
            part="snippet",
            regionCode=regionCode,
        )
        return request.execute()

    # Search by category ID
    @_paginated(2) # Increase paginate in prod
    def category_search(self, categoryId:int, search_term=None, order="relevance", pageToken=None):
        '''Search by Category ID

        Parameters
        ----------
        categoryId : int
            ID relating to a particular video category 
        order : str, optional
            string list accepts 'date' 'rating' 'relevance' 'title' 'videoCount' 'viewCount', by default "relevance"
        pageToken : str, optional
            parameter used by paginate decorator to loop through pages and gather results, by default None

        Returns
        -------
        list
            returns a list of dictionaries
        '''
        request = self.api.search().list(
            part="snippet",
            type="video",
            q=search_term,
            videoCategoryId=categoryId,
            order=order,
            pageToken=pageToken,
            maxResults=self.maxResults
        )
        return request.execute()