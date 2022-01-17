from decouple import config
import sqlite3
import os
from datetime import datetime

from data_api import youtube
from helpers import dict_search


class yt_database():

    def __init__(self, db='yt_sentiment.db'):
        self.db = db if os.path.exists(db) else print(f"{db} does not exist! Please create and re-run.")
        try:
            self.DEVELOPER_KEY = config('YT_API_KEY')
        except KeyError:
            print(f"Unable to find API key in .env file when initiating {self.__name__} object!")
        self.yt = youtube(self.DEVELOPER_KEY)
            
    def update_categories(self):
        dt = datetime.now()

        raw_categories = self.yt.VideoCategories('GB')
        categories = dict_search(raw_categories, ["id", "title", "assignable"])
            
        for cat in categories:
            cat['region'] = 'GB'
            cat['time_updated'] = dt

        try:
            with sqlite3.connect(self.db) as conn:
                sql = "INSERT OR REPLACE INTO \
                    categories(category_id, title, assignable, region, time_updated) \
                    VALUES(:id, :title, :assignable, :region, :time_updated)"
                conn.executemany(sql, categories)
                print("Categories table updated successfully!")
                
        except sqlite3.Error as error:
            print("Error while creating a sqlite table", error)   
    
    def _insert_or_replace(self):
        
    
    
    
    