import pprint
import json
import sqlite3

from data_api import youtube
from helpers import dict_search


def main():
    
    with open("./key.json") as f:
        DEVELOPER_KEY = json.load(f)['key']
    
    yt = youtube(DEVELOPER_KEY)

    top_tech = yt.category_search(28)
    ids = dict_search(top_tech, "videoId")
    ids = [id['videoId'] for id in ids]
    
    raw_stats = yt.video_stats(ids)
    
    stats = dict_search(raw_stats, ["id", "viewCount", "likeCount", "favoriteCount", "commentCount"])
    
    raw_categories = yt.VideoCategories('GB')
    cats = dict_search(raw_categories, ["id", "title", "assignable"])
    
    with sqlite3.connect('yt_sentiment.db') as conn:
        sql = "INSERT OR REPLACE INTO TABLE \
            categories(category_id, title, assignable, region, time_updated) \
            VALUES(:id, :title, :assignable, ?, ?)"
        
        conn.executemany(sql, )
        
    
    



 
if __name__ == "__main__":
    main()
    

    
# TODO: search for individual video's stats using the video list call
# TODO: Work out sentiment from title, description or comments (can we see all comments?)
