from models import *
import reddit_api
import db_api
from datetime import datetime, timedelta
from os import getenv

# TODO: Apply exchange rates to currency calculations

class TimeframeData():
    cache = []
    
    def __init__(self):
        '''Create cache on initalization'''
        self.cache = self.UpdateTimeframeData()
        self.subreddit = getenv('TARGET_SUBREDDIT')
        if self.subreddit == None:
            raise SystemExit("No subreddit designated, terminating.")

    def GetCache(self) -> list[dict]:
        return self.cache

    def UpdateTimeframeData(self) -> list[dict]:
        '''Master function for compiling the data to cache for the API'''
        # Initialize everything
        timeframe = []
        api = reddit_api.APITool()
        db = db_api.Database()
        api.Auth()
        db.CreateTables()

        # Get data from Reddit Data API and store in database
        # Reddit limits posts from a category to a maximum of 1000, enough for two weeks consistently
        nextPage = ''
        for _ in range(10):
            response = api.GetNewestPosts(self.subreddit, nextPage, 100)
            db.InsertPostList(response[0])
            if nextPage == response[1]:
                print("No new pages detected, stopping collection ahead of time.")
                break
            nextPage = response[1]
        
        # Perform check on [REQ] Posts, if unsure about their active status
        NullPosts = db.GetNullActiveLoanRequests()
        print(f"Validating {NullPosts.__len__()} posts for loan status")
        i = 0
        for id in NullPosts:
            i += 1
            db.UpdateActiveOnLoan(id, api.IsPostActive(self.subreddit, id))
        
        # Anonymize data in accordance with Reddit's rules
        db.AnonymizeData()
        
        # Make timeframe for the past 14 days, starting from yesterday
        for day in range(1, 15):
            query = db.LoanPaidAndDefaultRate(day) # Experiment in querying data, will probably get removed later.
            result = {'date': int((datetime.today() - timedelta(day)).timestamp()),
                    'reqCount': db.LoansRequestedOnDate(day),
                    'activeCount': db.LoansGivenOnDate(day),
                    'reqAmount': db.LoanAmountRequestedOnDate(day),
                    'activeAmount': db.LoanAmountGivenOnDate(day),
                    'loansPaid': query[0],
                    'loansUnpaid': query[1]
                    }
            timeframe.append(result)
        db.CloseConnection()
        return timeframe
        
    
if __name__ == "__main__":
    timeframe = TimeframeData()
    print(timeframe.GetCache())