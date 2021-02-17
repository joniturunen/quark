import sys
import settings
from googleapiclient.discovery import build
from uritemplate import api
from dotenv import dotenv_values
from pathlib import Path


class YoutubeSearch:
    def __init__(self):
        qenv = settings.Qenvs()
        self.api_key = qenv.google_api_key

    def get_service(self):
        # Get developer key from "credentials" tab of api dashboard
        return build("youtube", "v3", developerKey=self.api_key)

    def search(self, search_term, maxResults=1, json_output=False):
        youtube = self.get_service()
        request = youtube.search().list(
            part="snippet",
            maxResults=maxResults,
            type="video",
            q=search_term
        )
        response = request.execute()

        if json_output:
            return response
        else:
            return response.get('items')[0].get('id').get('videoId')


if __name__ == '__main__':
    # try:
    yt = YoutubeSearch()
    print(yt.search(sys.argv[1]))
    # except:
    #     print(f'Check you have GOOGLE_API_KEY in .env')
