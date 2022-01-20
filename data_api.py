import os
import googleapiclient.discovery
import googleapiclient.errors
from helpers import paginated, chunked_list

PAGE_LIMIT = 2  # To prevent exhausting api call budget whilst testing


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
    def video_stats(self, id):
        values = []
        # Chunk the list by 50 to remain within query limits
        id_lst = chunked_list(id, 50)
        # Loop chunked list
        for ids in id_lst:
            # Convert to string list
            id = ",".join(ids) if isinstance(ids, list) else ids

            request = self.api.videos().list(
                part="statistics",
                id=id,
                maxResults=self.maxResults
            )
            values.append(request.execute())
        return values

    @paginated(PAGE_LIMIT)
    # Retrieve list of most popular videos
    def popular(self, videoCategoryId, regionCode=None, pageToken=None):
        try:
            request = self.api.videos().list(
                part="snippet",
                chart="mostPopular",
                h1="en",
                videoCategoryId=videoCategoryId,
                pageToken=pageToken,
                maxResults=self.maxResults
                ).execute()
            return request
        except Exception as error:
            print(f"Error when requesting popular: {error}")

    # Retrieve list of video categories
    def VideoCategories(self, regionCode):

        # API videoCategory list request
        request = self.api.videoCategories().list(
            part="snippet",
            regionCode=regionCode,
        )
        return request.execute()

    @paginated(PAGE_LIMIT)
    # Search by category ID
    def category_search(self, categoryId: int, search_term=None, order="relevance", pageToken=None):
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
            order=order,
            pageToken=pageToken,
            maxResults=self.maxResults
        )
        return request.execute()

    def commentThread(self, videoId: str, part="snippet", pageToken=None):
        '''Retrieve comment thread for specific video ID(s)

        Parameters
        ----------
        videoId : str, list
            Unique video ID string, or list of strings
        part : str, optional
            response type (accepts 'snippet,' 'id,' 'replies'), by default "snippet"
        pageToken : str, optional
            parameter used by paginate decorator to loop through pages and gather results, by default None

        Returns
        -------
        list
            returns a list of response dictionaries
        '''
        values = []
        # Chunk the list by 50 to remain within query limits
        id_lst = chunked_list(videoId, 50)

        for ids in id_lst:
            # Convert to string list
            id = ",".join(ids) if isinstance(ids, list) else ids

            request = self.api.commentThreads().list(
                part=part,
                id=id,
                pageToken=pageToken,
                maxResults=self.maxResults
            )
            values.append(request.execute())
        return values

    def comment(self, commentId: str, part="snippet", pageToken=None):
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
