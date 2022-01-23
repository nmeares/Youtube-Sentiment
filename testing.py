import asyncio

class test():
    def outer():
        async def factorial(name, number):
            f = 1
            for i in range(2, number + 1):
                print(f"Task {name}: Compute factorial({number}), currently i={i}...")
                await asyncio.sleep(1)
                f *= i
            print(f"Task {name}: factorial({number}) = {f}")
            return f

        async def main():
            # Schedule three calls *concurrently*:
            L = await asyncio.gather(
                factorial("A", 2),
                factorial("B", 3),
                factorial("C", 4),
            )
            return L
        asyncio.run(main())
        

test.outer()

### Import dependencies
import database
from data_api import youtube
from pprint import pprint
import os
from helpers import dict_search
import pandas as pd


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