import os
import json
import helpers
import googleapiclient.discovery
import googleapiclient.errors
from pprint import pprint

def main():
    
    with open("./key.json") as f:
        DEVELOPER_KEY = json.load(f)['key']
    
    youtube = api_init(DEVELOPER_KEY)

    stats = category_search(youtube, 28)
    ids = helpers.dict_search(stats, "videoId")
    ids = [id['videoId'] for id in ids]
    stats = video_stats(youtube, ids)
    
    pprint(stats)
   

def api_init(key):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    return googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=key)


def paginated(func):
    combined = []
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        combined.append(response)
        pageToken = response['nextPageToken']
        while pageToken:
            combined.append(wrapper(*args, **kwargs, pageToken=pageToken))
        return combined    
    return wrapper

# Retrieve stats for video IDs
def video_stats(api_object: googleapiclient.discovery.build, id, pageToken=None):
    # Convert to string list
    id = ",".join(id) if isinstance(id, str) else id
    
    request = api_object.videos().list(
        part="statistics",
        id=id,
        pageToken=pageToken
    )
    return request.execute() 

def popular(api_object: googleapiclient.discovery.build, videoCategoryId, pageToken=None):
    
    request = api_object.videos().list(
        part="snippet",
        chart="mostPopular",
        videoCategoryId=videoCategoryId,
        pageToken=pageToken
    )
    return request.execute()

# Retrieve list of video categories
def VideoCategories(api_object: googleapiclient.discovery.build, regionCode, pageToken=None):
    
    # API videoCategory list request
    request = api_object.videoCategories().list(
        part="snippet",
        regionCode=regionCode,
        pageToken=pageToken
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

@paginated
def category_search(api_object: googleapiclient.discovery.build, videoCategoryId, pageToken=None):
    
    request = api_object.search().list(
        part="snippet",
        type="video",
        videoCategoryId=videoCategoryId,
        order="viewCount",
        pageToken=pageToken
    )
    return request.execute()



if __name__ == "__main__":
    main()
    
# TODO: search for individual video's stats using the video list call
# TODO: Work out sentiment from title, description or comments (can we see all comments?)
