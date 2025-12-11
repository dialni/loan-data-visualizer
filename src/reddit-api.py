import requests
import os
from dotenv import load_dotenv

class APITool():
    '''Tool for easily creating and maintaining access to Reddit's API'''
    loadEnvFromFile = True
    APIConnDetails = {}

    def __init__(self):
        pass

    def getEnv(self):
        '''Get relevant enviornment variables for connecting to '''
        if self.loadEnvFromFile:
            try:
                load_dotenv('../.env')
            except:
                raise SystemExit('Could not load .env file, exiting.')
                
        self.APIConnDetails = {'REDDIT_USERNAME': os.getenv('REDDIT_USERNAME'),
                      'REDDIT_PASSWORD': os.getenv('REDDIT_PASSWORD'),
                      'CLIENT_ID': os.getenv('CLIENT_ID'),
                      'CLIENT_SECRET': os.getenv('CLIENT_SECRET')}
        
    
    def auth(self) -> None:
        """Authenticate with Reddit API"""
        
        pass

    