import pprint
import json
import sqlite3
from datetime import datetime

from data_api import youtube
from helpers import dict_search


def main():
    
    with open("./key.json") as f:
        DEVELOPER_KEY = json.load(f)['key']
    
    yt = youtube(DEVELOPER_KEY)
    
    raw_categories = yt.VideoCategories('GB')
    cats = dict_search(raw_categories, ["id", "title", "assignable"])
    
    dt = datetime.now()
    
    for cat in cats:
        cat['region'] = 'GB'
        cat['time_updated'] = dt
    
    with sqlite3.connect('yt_sentiment.db') as conn:
        sql = "INSERT OR REPLACE INTO \
            categories(category_id, title, assignable, region, time_updated) \
            VALUES(:id, :title, :assignable, :region, :time_updated)"
        
        conn.executemany(sql, cats)
        
if __name__ == "__main__":
    main()
    

    
# TODO: search for individual video's stats using the video list call
# TODO: Work out sentiment from title, description or comments (can we see all comments?)
