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

def paginated(func):
    def wrapper():
        
        pass
    pass    

def api_init(key):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    return googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=key)

# Retrieve stats for video IDs
def video_stats(api_object: googleapiclient.discovery.build, id):
    # Convert to string list
    id = ",".join(id) if isinstance(id, str) else id
    
    request = api_object.videos().list(
        part="statistics",
        id=id
    )
    return request.execute() 

def popular(api_object: googleapiclient.discovery.build, videoCategoryId):
    
    request = api_object.videos().list(
        part="snippet",
        chart="mostPopular",
        videoCategoryId=videoCategoryId
    )
    return request.execute()

# Retrieve list of video categories
def VideoCategories(api_object: googleapiclient.discovery.build, regionCode):
    
    # API videoCategory list request
    request = api_object.videoCategories().list(
        part="snippet",
        regionCode=regionCode
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

def category_search(api_object: googleapiclient.discovery.build, videoCategoryId):
    
    request = api_object.search().list(
        part="snippet",
        type="video",
        videoCategoryId=videoCategoryId,
        order="viewCount"
    )
    return request.execute()



if __name__ == "__main__":
    main()
    
# TODO: search for individual video's stats using the video list call
# TODO: Work out sentiment from title, description or comments (can we see all comments?)
