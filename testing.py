import database
from data_api import youtube
from pprint import pprint
import os
from helpers import dict_search
import pandas as pd
import nest_asyncio

nest_asyncio.apply()

DEVELOPER_KEY = 'AIzaSyC42N8_Sa6fsoSvG2tFkJNl2XLNYeT0fHk'
yt = youtube(DEVELOPER_KEY)

search = 'macbook'
response = yt.category_search(28, search_term=search, order='date')
raw_ids = dict_search(response, ["videoId"], list_depth=2)
ids = [row['videoId'] for row in raw_ids]

raw_stats = yt.video_stats(ids)
clean_stats = dict_search(raw_stats, [
    "id", 
    "title",
    "decription", 
    "channelTitle", 
    "categoryId", 
    "viewCount", 
    "likeCount", 
    "commentCount", 
    "publishedAt"], list_depth=2)
stats_df = pd.DataFrame(clean_stats)

raw_comments = yt.commentThread(ids)

print(raw_comments)