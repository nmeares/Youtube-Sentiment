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

    stats = video_stats(youtube, 28)
    
    pprint(stats)

    

def api_init(key):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    return googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=key)


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

def video_stats(api_object: googleapiclient.discovery.build, videoCategoryId):
    
    request = api_object.search().list(
        part="snippet",
        type="video",
        videoCategoryId=videoCategoryId,
        order="viewCount"
    )
    response = request.execute()
    return helpers.dict_search(response, ["kind"], list_depth=0)

if __name__ == "__main__":
    main()
    
# TODO: search for individual video's stats using the video list call
# TODO: Work out sentiment from title, description or comments (can we see all comments?)
