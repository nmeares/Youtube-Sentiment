import pprint
import json

import data_api
import helpers




def main():
    
    with open("./key.json") as f:
        DEVELOPER_KEY = json.load(f)['key']
    
    youtube = data_api.api_init(DEVELOPER_KEY)

    stats = data_api.category_search(youtube, 28)
    ids = helpers.dict_search(stats, "videoId")
    ids = [id['videoId'] for id in ids]
    stats = data_api.video_stats(youtube, ids)
    
    pprint(stats)


 
if __name__ == "__main__":
    main()
    

    
# TODO: search for individual video's stats using the video list call
# TODO: Work out sentiment from title, description or comments (can we see all comments?)
