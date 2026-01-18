from models import *
import reddit_api
import db_api
from datetime import datetime, timedelta

# TODO: Apply exchange rates to currency calculations

class TimeframeData():
    cache = []
    
    def __init__(self):
        '''Create cache on initalization'''
        self.cache = self.UpdateTimeframeData()

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
        for _ in range(1):
            response = api.GetNewestPosts('borrow', nextPage, 1)
            db.InsertPostList(response[0])
            if nextPage == response[1]:
                print("No new pages detected, stopping collection ahead of time.")
                break
            nextPage = response[1]
        
        # Validate data
        NullPosts = db.GetNullActiveLoanRequests()
        print(f"Validating {NullPosts.__len__()} posts for loan status")
        i = 0
        for id in NullPosts:
            i += 1
            db.UpdateActiveOnLoan(id, api.IsPostActive('borrow', id))
            #print(f"NullPost validation: {i} / {NullPosts.__len__()}")
        
        # Anonymize data
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
        #print(timeframe)
        db.CloseConnection()
        return timeframe
        
    
if __name__ == "__main__":

    # Data points to prepare:
    # - Basis data
    #  - Loans requested + Loans given over N day timeframe (2D Histogram)
    #  - Total amount requested and total amount loaned over N day timeframe (2D Histogram)
    #  - Default rate vs Paid rate (Pie-chart)
    #
    # - Summary and conclusion
    #  - Hypothetical "total expected ROI for X amount invested"
    
    timeframe = TimeframeData()
    print(timeframe.GetCache())