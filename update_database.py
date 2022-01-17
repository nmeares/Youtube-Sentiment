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

        self._insert_or_replace("categories", categories)  
    
    def _insert_or_replace(self, table, dictionary:dict):
        keys = dictionary.keys()
        values = [f":{key}" for key in dictionary.keys()]
        try:
            with sqlite3.connect(self.db) as conn:
                sql = f"INSERT OR REPLACE INTO \
                    {table}({keys}) \
                    VALUES({values})"
                conn.executemany(sql, dictionary)
                print(f"{table} table updated successfully!")
                
        except sqlite3.Error as error:
            print(f"Error while updating a {table} table", error)
    
    
    
    