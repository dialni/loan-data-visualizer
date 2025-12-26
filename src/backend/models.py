from enum import Enum
from datetime import datetime
import re


class Status(Enum):
    '''Defines the type of post, e.g. if someone is requesting a loan'''
    REQ = 1
    PAID = 2
    UNPAID = 3
    LATE = 4
    INVALID = 5 # Any post deemed not fit for parsing is invalid and should be ignored.

class Currency(Enum):
    USD = 1
    EUR = 2
    GBP = 3
    CAD = 4
    XXX = 5 # Unknown currency, used instead of None for invalid posts

class Post():
    '''Data Model of Posts on Subreddits'''
    id: str
    status: Status
    title: str
    currency: Currency
    amount: int = 0       # Loan principal
    isActive: bool = None # Only relevant for [REQ] posts
    timestamp: datetime
    
    def __init__(self, id:str, title:str, timestamp:float, commentsCount: int):
        self.id = id
        self.title = title.upper()
        self.timestamp = datetime.fromtimestamp(timestamp)
        self.ParsePostType()
        self.ParseIsActive(commentsCount)
        self.ParseCurrencyType()
        self.ParseCurrencyAmount()
        # Assume amounts less than 5 or higher than 12.000 to be parsed unsuccessfully
        # This is temporary until a better parsing system has been implemented.
        if self.amount < 5 or self.amount > 12000:
            self.status = Status.INVALID

    def ParsePostType(self) -> None:
        '''Parse what type of post from title, e.g. [REQ], [PAID], etc.'''
        # Lazy parsing implementation, since only 5 valid states
        if self.title.__contains__('[REQ]'):
            self.status = Status.REQ
        elif self.title.__contains__('[PAID]'):
            self.status = Status.PAID
        elif self.title.__contains__('[UNPAID]'):
            self.status = Status.UNPAID
        elif self.title.__contains__('[LATE]'):
            self.status = Status.LATE
        else:
            self.status = Status.INVALID
            
    def ParseIsActive(self, commentCount:int) -> None:
        '''For [REQ] Posts, do a quick chekc to figure out if anyone accepted the loan. 
           For unsure [REQ] Posts, inspect Post comments later. Assume pre-arranged to be active.'''
        if self.status is not Status.REQ:
            return
        
        if self.title.__contains__('ARRANGED') and self.title.__contains__('[REQ]'):
            self.isActive = True
        
        # Automated bot always leaves 2 comments on each [REQ] Post.
        # Assume if no one else posted, then loan is not active and don't use API request.
        elif commentCount < 3:
            self.isActive = False
    
    def ParseCurrencyType(self) -> None:
        '''Parses currency from post title.'''
        if self.title.__contains__('USD'):
            self.currency = Currency.USD

        # Guess if '$' means USD or CAD, assume USD by default
        elif self.title.__contains__('$'):        
            if self.title.__contains__(', CA)') or self.title.__contains__('CANADA'):
                self.currency = Currency.CAD
            else:
                self.currency = Currency.USD
        
        # Explicit currency assignment
        elif self.title.__contains__('£') or self.title.__contains__('GBP'):
            self.currency = Currency.GBP

        elif self.title.__contains__('€') or self.title.__contains__('EUR'):
            self.currency = Currency.EUR
            
        ## If not explicit, try to guess currency based on location
        elif self.title.__contains__('USA)') or self.title.__contains__('US)'):
            self.currency = Currency.USD
        elif self.title.__contains__(', CA)') or self.title.__contains__('CANADA'):
            self.currency = Currency.CAD
            
        # If parsing fails completely, invalidate post and discard
        else: 
            self.currency = Currency.XXX
            self.status = Status.INVALID
    
    def ParseCurrencyAmount(self) -> None:
        '''Make an attempt to find the correct loan principal requested
           (or owed in case of [UNPAID] status)'''
        # TODO: Make smarter by being suspecious of non 0 or 5 values in final digit of amount
        # TODO: Add better support for dealing with thousands separators, e.g. 1,500 or 1.500
        # Remove date from entry
        regexDate = re.sub(r"(\d{1,2}/\d{1,2}/?\d{0,4}|\d{1,2}TH|\d{1,2}ND|\d{1,2}ST)", "", self.title)
        regexDate = regexDate.replace(",", "", 1)
        regexDate = regexDate.replace(".", "", 1)
        
        
        # Try to find group with currency identifier first
        # eg. GBP|EUR|USD|CAD|\$|€|£
        for group in regexDate.split(')'):
            if re.findall(r'GBP|EUR|USD|CAD|\$|€|£', group).__len__() != 0:
                try:
                    self.amount = int(re.findall(r"(\d+)", group).pop(0))
                except (IndexError, ValueError):
                    self.status = Status.INVALID
                return
            
        # If selective parsing attempt fails, use first available digit group
        regexAmounts = re.findall(r"(\d+)", regexDate)
        try:
            self.amount = int(regexAmounts.pop(0))
        except (IndexError, ValueError): 
            self.status = Status.INVALID
    
    def ParseRepayAmount(self):
        # Remove date-related entries for parsing amounts.
        # Does not work with alternatives such as 'REPAY $200 JAN 2, JAN 16'
        # This will be considered acceptable deviation for now
        raise NotImplementedError
        regexDate = re.sub(r"(\d{1,2}/\d{1,2}/?\d{0,4}|\d{1,2}TH|\d{1,2}ND|\d{1,2}ST)", "", self.title)
        regexAmounts = re.findall(r"(\d+)", regexDate)
        for i in regexAmounts:
            self.amount += int(regexAmounts.pop())
        print(self.amount)
            
    def __str__(self):
        return f'{self.id}, {self.status.name}, {self.currency.name}, {self.amount}, {self.title}'