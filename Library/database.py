import sqlite3
import os
from decouple import config
from datetime import datetime

from data_api import youtube
from helpers import dict_search
import pathlib

PARENT_PATH = str(pathlib.Path(__file__).parent.parent)

class yt_sentiment():

    def __init__(self, db=PARENT_PATH + '/Database/yt_sentiment.db'):
        self.db = db if os.path.exists(db) else print(
            f"{db} does not exist! Please create and re-run.")
        try:
            self.DEVELOPER_KEY = config('YT_API_KEY')
        except:
            print(
                f"Unable to find API key in .env file when initiating {self.__name__} object!")
        self.yt = youtube(self.DEVELOPER_KEY)

    # Update categories for a specific region
    def update_categories(self, region):
        dt = datetime.now()

        raw_categories = self.yt.VideoCategories(region)
        categories = dict_search(raw_categories, ["id", "title", "assignable"])

        for cat in categories:
            cat['region'] = region
            cat['time_updated'] = dt
            # re-name 'id' key to 'categories_id'
            cat['category_id'] = cat.pop('id')

        self._insert_or_replace("categories", categories)

    # Function to insert or replace a list of key value pairs into a sqlite3 database
    def _insert_or_replace(self, table, value_list: list):
        # Create key and value lists and sql query string
        keys = ",".join(list(value_list[0].keys()))
        values = ",".join([f":{key}" for key in value_list[0].keys()])
        # Okay to use f-strings in this context as low likelyhood of injection attacks here
        sql = f"INSERT OR REPLACE INTO {table}({keys}) VALUES({values})"

        try:
            with sqlite3.connect(self.db) as conn:
                conn.executemany(sql, value_list)
                print(f"{table} table updated successfully!")

        except sqlite3.Error as error:
            print(f"Error while updating a {table} table. ERROR:", error)
