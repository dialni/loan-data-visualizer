import requests
import os
from dotenv import load_dotenv
from time import time, sleep
from models import Post

# Register apps at https://www.reddit.com/prefs/apps

class APITool():
    '''Tool for easily creating and maintaining access to Reddit's API'''
    # Config
    loadEnvFromFile = True
    requestTimeout = time()

    # Auth
    user_agent = "python:loan-data-visualizer:v1.0.0 (by /u/OverallSoup)"
    
    def __init__(self):
        self.GetEnv()
        
    def GetEnv(self) -> None:
        '''Get relevant enviornment variables for connecting to '''
        
        # Optionally, load from .env file instead.
        if self.loadEnvFromFile:
            if not load_dotenv('.env'):
                raise SystemExit('RedditAPI: Could not load .env file, exiting.')
                
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
        '''GET request with self-imposed rate-limit'''
        
        # Very respectful rate-limiter of 1 req/sec
        if (self.requestTimeout) > time():
            #print("Sleeping for 1 second")
            sleep(1)
        
        self.requestTimeout = time() + 1
        
        try: response = requests.get(url, 
                                     headers={'Authorization': f'{self.token_type} {self.access_token}', 
                                              'User-Agent': self.user_agent})
        except requests.HTTPError as e:
            raise SystemExit(f"Something went wrong during GetRequest\n{e}\n{e.response.status_code}\n{e.response.json()}")
        print(f"x-ratelimit-remaining: {float(response.headers['x-ratelimit-remaining'])} ", end="")
        # This should not be possible with current rate-limiter of 1 req/sec
        if float(response.headers['x-ratelimit-remaining']) < 5.0:
            print(f"Rate-limit somehow exceeded, sleeping for {response.headers['x-ratelimit-reset'] + 4} seconds.")
            self.requestTimeout = time() + 4.0 + float(response.headers['x-ratelimit-reset'])

        return response
    
    def TestConnection(self) -> None:
        '''A small test to see if authentication worked.'''
        self.GetRequest('https://oauth.reddit.com/api/v1/me')
        print("TestConnection was successful!")
        
    def GetNewestPosts(self, sr:str, nextPage="", limit=100) -> tuple[list[Post], str]:
        '''Return latest Posts from specified Subreddit, and the key for the next page'''
        posts: list[Post] = []
        
        # Limit to 100 posts, which is enforced by Reddit Data API
        c = min(limit, 100)
        print(f"Sending request for {c}")
        
        # Use correct API
        if nextPage == "":
            response = self.GetRequest(f'https://oauth.reddit.com/r/{sr}/new/?limit={c}').json()['data']
        else:
            response = self.GetRequest(f'https://oauth.reddit.com/r/{sr}/new/?limit={c}&after={nextPage}').json()['data']
        
        nextPage = response['after']
        
        for child in response['children']:
            # In accordance with Reddit Data API policy, deleted users are disregarded.
            if child['data']['author'] != '[deleted]':
                posts.append(Post(child['data']['id'], 
                                  child['data']['title'], 
                                  child['data']['created'],
                                  child['data']['num_comments']))
        
        return (posts, nextPage)

    def GetNewestPostsRaw(self) -> dict:
        '''Used for testing purposes, not for production code'''
        return self.GetRequest(f'https://oauth.reddit.com/r/borrow/new/?limit=1').json()
    
    def GetCommentsOnPostRaw(self, sr:str, id:str) -> dict:
        '''Used for testing purposes, not for production code'''
        return self.GetRequest(f"https://oauth.reddit.com/r/{sr}/comments/{id}").json()
    
    def IsPostActive(self, sr:str, id:str) -> bool:
        response = self.GetRequest(f"https://oauth.reddit.com/r/{sr}/comments/{id}").json()
        for i in response[1]['data']['children']:
            if str(i['data']['body']).upper().__contains__('$LOAN'):
                return True
            
        return False