import os
import json
import helpers
import googleapiclient.discovery
import googleapiclient.errors
from functools import wraps
from pprint import pprint


def api_init(key):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    return googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=key)

# Decorator function to loop paginated responses
def paginated(func):
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
@paginated
def video_stats(api_object: googleapiclient.discovery.build, id, pageToken=None):
    # Convert to string list
    id = ",".join(id) if isinstance(id, str) else id
    
    request = api_object.videos().list(
        part="statistics",
        id=id,
        pageToken=pageToken,
        maxResults=50
    )
    return request.execute()

# Retrieve list of most popular videos
@paginated
def popular(api_object: googleapiclient.discovery.build, videoCategoryId, pageToken=None):
    
    request = api_object.videos().list(
        part="snippet",
        chart="mostPopular",
        videoCategoryId=videoCategoryId,
        pageToken=pageToken,
        maxResults=50
    )
    return request.execute()

# Retrieve list of video categories
@paginated
def VideoCategories(api_object: googleapiclient.discovery.build, regionCode, pageToken=None):
    
    # API videoCategory list request
    request = api_object.videoCategories().list(
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
@paginated
def category_search(api_object: googleapiclient.discovery.build, videoCategoryId, pageToken=None):
    
    request = api_object.search().list(
        part="snippet",
        type="video",
        videoCategoryId=videoCategoryId,
        order="viewCount",
        pageToken=pageToken,
        maxResults=50
    )
    return request.execute()

    
# TODO: search for individual video's stats using the video list call
# TODO: Work out sentiment from title, description or comments (can we see all comments?)
