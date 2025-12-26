from models import *
import reddit_api
import db_api
from datetime import datetime, timedelta

def LoanAmountsTimeframe() -> list[dict]:
    '''How many loans were requested and given over 90 days'''
    # TODO: Finish function for finding out if loan is active
    timeframe = []
    for day in range(2):
        result = {'date': int((datetime.today() - timedelta(day)).timestamp()),
                  'reqCount': db.LoansRequestedOnDate(day)}
        timeframe.append(result)
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
    
    # Initalize everything
    api = reddit_api.APITool()
    db = db_api.Database()
    
    print(LoanAmountsTimeframe())
    
    db.CloseConnection()