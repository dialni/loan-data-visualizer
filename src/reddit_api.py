import requests
import os
from dotenv import load_dotenv

class APITool():
    '''Tool for easily creating and maintaining access to Reddit's API'''
    loadEnvFromFile = True
    APIConnDetails = {}

    def __init__(self):
        self.getEnv()
        
    def getEnv(self) -> None:
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
    
    def auth(self) -> None:
        """Authenticate with Reddit API"""
        
        pass

    