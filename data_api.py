import os
from urllib import response
from black import asyncio
import googleapiclient.discovery
import googleapiclient.errors
from helpers import paginated, chunked_list

PAGE_LIMIT = 2  # To prevent exhausting api call budget during testing


class youtube():

    def __init__(self, api_key, resultsPerPage=50, maxPages=1000) -> None:
        self.api_key = api_key
        self.maxResults = resultsPerPage
        self.maxPages = maxPages

        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        self.api_service_name = "youtube"
        self.api_version = "v3"
        self.api = googleapiclient.discovery.build(
            self.api_service_name,
            self.api_version,
            developerKey=self.api_key)

    # Retrieve stats for video specific IDs (max 50)
    def video_stats(self, id) -> list:
        values = []
        # Chunk the list by 50 to remain within query limits
        id_lst = chunked_list(id, 50)
        # Loop chunked list
        for ids in id_lst:
            # Convert to string list
            id = ",".join(ids) if isinstance(ids, list) else ids

            request = self.api.videos().list(
                part="snippet, statistics",
                id=id,
                maxResults=self.maxResults
            )
            values.append(request.execute())
        return values

    @paginated(PAGE_LIMIT)
    # Retrieve list of most popular videos
    def popular(self, videoCategoryId, regionCode=None, pageToken=None) -> dict:
        try:
            request = self.api.videos().list(
                part="snippet",
                chart="mostPopular",
                videoCategoryId=videoCategoryId,
                regionCode=regionCode,
                pageToken=pageToken,
                maxResults=self.maxResults
            ).execute()
            return request
        except Exception as error:
            print(f"Error when requesting popular: {error}")

    # Retrieve list of video categories
    def VideoCategories(self, regionCode) -> dict:

        # API videoCategory list request
        request = self.api.videoCategories().list(
            part="snippet",
            regionCode=regionCode,
        )
        return request.execute()

    @paginated(PAGE_LIMIT)
    # Search by category ID
    def category_search(self, categoryId: int, search_term=None, order="relevance", regionCode=None, pageToken=None) -> dict:
        '''Search by Category ID

        Parameters
        ----------
        categoryId : int
            ID relating to a particular video category 
        order : str, optional
            string list accepts 'date' 'rating' 'relevance' 'title' 'videoCount' 'viewCount', by default "relevance"
        pageToken : str, optional
            parameter used by paginate decorator to loop through pages and gather results, by default None

        Returns
        -------
        list
            returns a list of response dictionaries
        '''
        request = self.api.search().list(
            part="snippet",
            type="video",
            q=search_term,
            videoCategoryId=categoryId,
            regionCode=regionCode,
            order=order,
            pageToken=pageToken,
            maxResults=self.maxResults
        )
        return request.execute()

    # Retrieve comment thread details
    def commentThread(self, videoId, part="snippet", pageToken=None) -> list:
        '''Retrieve comment thread for specific video ID(s)

        Parameters
        ----------
        videoId : str
            Unique video ID string
        part : str, optional
            response type (accepts 'snippet,' 'id,' 'replies'), by default "snippet"
        pageToken : str, optional
            parameter used by paginate decorator to loop through pages and gather results, by default None

        Returns
        -------
        dict
            returns a dict
        '''
        # Create list of videoIds
        videoIds = [videoId] if isinstance(videoId, str) else videoId
        values = []
        for id in videoIds:
            try:
                request = self.api.commentThreads().list(
                    part=part,
                    videoId=id,
                    pageToken=pageToken,
                    maxResults=self.maxResults
                ).execute()
                values.append(request)
            except googleapiclient.errors.HttpError as error:
                values.append({id:error.error_details[0]['reason']})
            except Exception as error:
                print(f"Error on videoId {id}: {error}")
        return values


    def comment(self, commentId: str, part="snippet", pageToken=None) -> list:
        '''Retrieve information for specific comment ID(s)

        Parameters
        ----------
        videoId : str, list
            Unique video ID string, or list of strings
        part : str, optional
            response type (accepts 'snippet,' 'id,'), by default "snippet"
        pageToken : str, optional
            parameter used by paginate decorator to loop through pages and gather results, by default None

        Returns
        -------
        list
            returns a list of response dictionaries
        '''
        values = []
        # Chunk the list by 50 to remain within query limits
        id_lst = chunked_list(commentId, 50)

        for ids in id_lst:
            # Convert to string list
            id = ",".join(ids) if isinstance(ids, list) else ids

            request = self.api.comment().list(
                part=part,
                id=id,
                pageToken=pageToken,
                maxResults=self.maxResults
            )
            values.append(request.execute())
        return values
    
    # Retrieve channel information
    @paginated(PAGE_LIMIT)
    def channel(self, channelId, part="snippet", pageToken=None) -> list:
        values = []
        # Chunk the list by 50 to remain within query limits
        id_lst = chunked_list(channelId, 50)
        for ids in id_lst:
            id = ",".join(ids)
            request = self.api.channels().list(
                part=part,
                id=id,
                pageToken=pageToken,
                maxResults=self.maxResults
                )
            values.append(request.execute())
        return values
        
