from models import *
import os
import psycopg
from dotenv import load_dotenv
from time import sleep

class Database():
    
    def __init__(self):
        '''Tool for easily creating and maintaining access to a postgres database'''
        if not load_dotenv('../../.env'):
            raise SystemExit('Could not load .env file, exiting.')

        while True:
            try: self.conn = psycopg.connect(f'postgres://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@localhost:{os.getenv('POSTGRES_PORT')}/mydb')
            except psycopg.OperationalError: 
                print("Failed to connect, retrying in 2 seconds...")
                sleep(2)
                continue
            self.cur = self.conn.cursor()
            break
    
    def CreateTables(self) -> None:
        '''Create necessary tables and types to store Posts. Wipes any data already present.'''
        
        # Check if Enum types already exists, 'IF NOT EXISTS' does not work here.
        self.cur.execute("""DROP TABLE IF EXISTS Posts; 
                            DROP TYPE IF EXISTS Status;
                            DROP TYPE IF EXISTS Currency;""")
        
        # Enum types mirroring those from Post model
        self.cur.execute("CREATE TYPE Status AS ENUM ('REQ', 'PAID', 'UNPAID', 'LATE', 'INVALID')")
        self.cur.execute("CREATE TYPE Currency AS ENUM ('USD', 'EUR', 'GBP', 'CAD', 'XXX')")
        
        # Create fresh table
        self.cur.execute('''
            CREATE TABLE Posts(
                id VARCHAR(7) PRIMARY KEY,
                timestamp TIMESTAMP,
                status Status,
                currency Currency, 
                amount INTEGER,
                isActive BOOL,
                title VARCHAR(200));''')
        self.conn.commit()
        
    def InsertPost(self, p: Post) -> None:
        '''Store Post in the database'''
        self.cur.execute("INSERT INTO Posts VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING", 
                         (p.id, p.timestamp, p.status.name, p.currency.name, p.amount, p.isActive, p.title))
        self.conn.commit()
        
    def InsertPostList(self, pList: list[Post]) -> None:
        '''Store a list of Posts inside the database'''
        
        l: list[Post] = []
        for p in pList:
            l.append((p.id, p.timestamp, p.status.name, p.currency.name, p.amount, p.isActive, p.title))
        
        self.cur.executemany("INSERT INTO Posts VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING", l)
        self.conn.commit()
        
    def GetAllPosts(self) -> list[tuple]:
        '''Returns every Post in the database as a list of tuples'''
        self.cur.execute('SELECT * FROM Posts')
        return self.cur.fetchall()

    def GetPostsByCurrency(self, currency: Currency) -> list[tuple]:
        '''Filter by currency (e.g. USD) and return every Post as a list of tuples'''
        self.cur.execute("SELECT * FROM Posts WHERE currency = (%s)", (currency.name,))
        return self.cur.fetchall()
        
    def GetPostsByStatus(self, status: Status) -> list[tuple]:
        '''Filter by status (e.g. [REQ]) and return every Post as a list of tuples'''
        self.cur.execute("SELECT * FROM Posts WHERE status = (%s)", (status.name,))
        return self.cur.fetchall()
    
    def GetPostsByTimestamp(self, days: int) -> list[tuple]:
        '''Filter by exact date, N days from now. 
           Only 0-90 days are valid, anything outside this range will be clamped'''
        
        # Clamp value to clean input. 
        try: days = min(max(days, 0), 90)
        except TypeError: return []
        
        self.cur.execute("SELECT * FROM Posts WHERE timestamp::date = CURRENT_DATE - (%s)", (days,))
        return self.cur.fetchall()
    
    def LoansRequestedOnDate(self, day:int) -> int:
        self.cur.execute("""
                         SELECT count(*) FROM Posts 
                         WHERE timestamp::date = CURRENT_DATE - (%s) AND status = 'REQ'
                         """, (day,))
        return self.cur.fetchone()[0]


    def GetPostsByStatusAndTimestamp(self, days:int, status:Status) -> list[tuple]:
        '''Filter by status and exact date, N days from now. 
           Only 0-90 days are valid, anything outside this range will be clamped'''
        
        # Clamp value to clean input.
        try: days = min(max(days, 0), 90)
        except TypeError: return []
        if status == Status.REQ:
            self.cur.execute("SELECT * FROM Posts WHERE timestamp::date = CURRENT_DATE - (%s) AND status = 'REQ'", (days,))
        elif status == Status.PAID:
            self.cur.execute("SELECT * FROM Posts WHERE timestamp::date = CURRENT_DATE - (%s) AND status = 'PAID'", (days,))
        else:
            return []

        return self.cur.fetchall()
    
    def CloseConnection(self) -> None:
        '''Ensure a clean disconnect from the database, without using a context manager'''
        self.conn.close()