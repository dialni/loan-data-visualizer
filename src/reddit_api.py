import requests
import os
from dotenv import load_dotenv
from time import time, sleep
import example
from models import Post

# Register apps at https://www.reddit.com/prefs/apps

class APITool():
    '''Tool for easily creating and maintaining access to Reddit's API'''
    # Config
    loadEnvFromFile = True
    requestTimeout = time()

    # Auth
    APIConnDetails = {}
    access_token: str
    token_type: str
    user_agent = "python:loan-data-visualizer:v1.0.0 (by /u/OverallSoup)"
    
    def __init__(self):
        self.GetEnv()
        
    def GetEnv(self) -> None:
        '''Get relevant enviornment variables for connecting to '''
        
        # Optionally, load from .env file instead.
        if self.loadEnvFromFile:
            if not load_dotenv('.env'):
                raise SystemExit('Could not load .env file, exiting.')
                
        self.APIConnDetails = {'REDDIT_USERNAME': os.getenv('REDDIT_USERNAME'),
                               'REDDIT_PASSWORD': os.getenv('REDDIT_PASSWORD'),
                               'CLIENT_ID': os.getenv('CLIENT_ID'),
                               'CLIENT_SECRET': os.getenv('CLIENT_SECRET')}
        
        # Ensure all environment variables are found
        if None in self.APIConnDetails.values():
            print('Could not find all environment variables')
            for key in self.APIConnDetails:
                if self.APIConnDetails[key] is None:
                    print(f'Missing {key}')
            raise SystemExit()
        
        print('Env loaded!')
    
    def Auth(self) -> None:
        """Authenticate with Reddit API"""
        client_auth = requests.auth.HTTPBasicAuth(self.APIConnDetails['CLIENT_ID'], 
                                                  self.APIConnDetails['CLIENT_SECRET'])
        post_data = {'grant_type': 'password', 
                     'username': self.APIConnDetails['REDDIT_USERNAME'], 
                     'password': self.APIConnDetails['REDDIT_PASSWORD']}
        
        headers = {'User-Agent': self.user_agent}
        
        try:
            response = requests.post('https://www.reddit.com/api/v1/access_token', 
                                 auth=client_auth, data=post_data, headers=headers)
        except requests.HTTPError as e:
            print(f"Something went wrong during Auth\n{e}\n{e.response.status_code}\n{e.response.json()}")
            raise SystemExit()
        
        self.access_token = response.json()['access_token']
        self.token_type = response.json()['token_type']
    
    def GetRequest(self, url: str) -> requests.Response:
        # Very respectful rate-limiter of 1 req/sec
        if (self.requestTimeout) > time():
            print("Sleeping for 1 second")
            sleep(1)
        
        self.requestTimeout = time() + 1
        
        try:
            response = requests.get(url, 
                                    headers={'Authorization': f'{self.token_type} {self.access_token}', 
                                             'User-Agent': self.user_agent})
        except requests.HTTPError as e:
            print(f"Something went wrong during GetRequest\n{e}\n{e.response.status_code}\n{e.response.json()}")
            raise SystemExit()
        
        return response
    
    def TestConnection(self) -> None:
        self.GetRequest('https://oauth.reddit.com/api/v1/me')
        print("TestConnection was successful!")
        
    def GetNewestPosts(self, sr: str, limit=90) -> list[Post]:
        '''Return latest Posts from specified Subreddit'''
        nextPage = ""
        posts: list[Post] = []
        
        for i in range((limit // 100) + 1):
            if limit == 0:
                break
            c = min(limit, 100)
            print(f"Sending request for {c}")
            # Use correct API
            if nextPage == "":
                response = self.GetRequest(f'https://oauth.reddit.com/r/{sr}/new/?limit={c}').json()['data']
            else:
                response = self.GetRequest(f'https://oauth.reddit.com/r/{sr}/new/?limit={c}&after={nextPage}').json()['data']
            limit = limit - c
            
            # Send response to be parsed by models.py
            nextPage = response['after']
            for child in response['children']:
                posts.append(Post(child['data']['id'], child['data']['title']))
            
        return posts
    
    def TestExample(self) -> list[Post]:
        '''Used with example.py to test parsing functions, without hammering Reddit Data API'''
        posts: list[Post] = []
        for child in example.json['data']['children']:
            posts.append(Post(child['data']['id'], child['data']['title']))
        return posts
    
    def GetNewestPostsRaw(self) -> dict:
        return self.GetRequest(f'https://oauth.reddit.com/r/borrow/new/?limit=1').json()