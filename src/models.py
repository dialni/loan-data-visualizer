from enum import Enum
import re

class Status(Enum):
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
    '''DTO model of Posts on Subreddits'''
    id: str
    status: Status
    title: str
    currency: Currency = None
    amount: float = 0.0
    
    def __init__(self, id:str, title:str):
        self.id = id
        self.title = title.upper()
        self.ParsePostType()
        self.ParseCurrencyType()
        self.ParseCurrencyAmount()
        # if (self.ParsePostType() or self.ParseCurrencyType()) == Status.INVALID:
                
    def ParsePostType(self) -> Status:
        '''
        Parse what type of post from title, e.g. [REQ], [PAID], etc.
        
        :return: Status enum of this post
        :rtype: Status
        '''
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
    
    def ParseCurrencyType(self) -> Status | None:
        '''
        Parses currency from post title.
        
        :return: Returns status on invalid posts.
        :rtype: Status | None
        '''
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
        elif self.title.__contains__('USA)'):
            self.currency = Currency.USD
        elif self.title.__contains__(', CA)') or self.title.__contains__('CANADA'):
            self.currency = Currency.CAD
            
        # If parsing fails completely, invalidate post and discard
        else: 
            self.currency = Currency.XXX
            self.Status = Status.INVALID
    
    def ParseCurrencyAmount(self):
        '''Make an attempt to find the correct initial amount borrowed (or owed in case of [UNPAID] status)'''
        # TODO: Make smarter by being suspecious of non 0 or 5 values in final digit of amount
        
        # Remove date from entry
        regexDate = re.sub(r"(\d{1,2}/\d{1,2}/?\d{0,4}|\d{1,2}TH|\d{1,2}ND|\d{1,2}ST)", "", self.title)
        
        # Try to find group with currency identifier first
        # eg. GBP|EUR|USD|CAD|\$|€|£
        for group in regexDate.split('('):
            if re.findall(r'GBP|EUR|USD|CAD|\$|€|£', group).__len__() != 0:
                try:
                    self.amount = re.findall(r"(\d+)", group).pop(0)
                except IndexError:
                    self.status = Status.INVALID
                return
            
        # If selective parsing attempt fails, use first available digit group
        regexAmounts = re.findall(r"(\d+)", regexDate)
        try:
            self.amount = regexAmounts.pop(0)
        except IndexError:
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