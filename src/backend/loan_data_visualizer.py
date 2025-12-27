from models import *
import reddit_api
import db_api
from datetime import datetime, timedelta

# TODO: Apply exchange rates to currency calculations

def UpdateTimeframeData() -> list[dict]:
    '''Master function for compiling the data to cache for the API'''
    # Initialize everything
    timeframe = []
    api = reddit_api.APITool()
    db = db_api.Database()
    api.Auth()
    db.CreateTables()
    
    # Get data from Reddit Data API and store in database
    nextPage = ''
    for _ in range(3):
        response = api.GetNewestPosts('borrow', nextPage, 100)
        db.InsertPostList(response[0])
        nextPage = response[1]
    
    # Validate data
    NullPosts = db.GetNullActiveLoanRequests()
    i = 0
    for id in NullPosts:
        i += 1
        db.UpdateActiveOnLoan(id, api.IsPostActive('borrow', id))
        print(f"NullPost validation: {i} / {NullPosts.__len__()}")
    
    # Anonymize data
    db.AnonymizeData()
    
    # Make timeframe
    for day in range(30):
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
    print(timeframe)
    db.CloseConnection()
    
    
if __name__ == "__main__":

    # Data points to prepare:
    # - Basis data
    #  - Loans requested + Loans given over N day timeframe (2D Histogram)
    #  - Total amount requested and total amount loaned over N day timeframe (2D Histogram)
    #  - Default rate vs Paid rate (Pie-chart)
    #
    # - Summary and conclusion
    #  - Hypothetical "total expected ROI for X amount invested"
    
    UpdateTimeframeData()