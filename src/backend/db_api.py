from models import *
import os
import psycopg
import sqlite3
from tempfile import gettempdir
from dotenv import load_dotenv

class Database():
    # TODO: Clean up / Refactor SQL statements
    def __init__(self):
        '''Tool for easily creating and maintaining access to a postgres database'''
        if not load_dotenv('.env'):
            raise SystemExit('DB: Could not load .env file, exiting.')
        
        # Is database context postgres (pg)?
        self.isPG = True
        try: self.conn = psycopg.connect(f'postgres://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@localhost:{os.getenv('POSTGRES_PORT')}/mydb')
        except psycopg.OperationalError:
            print("Connection could not be made, using temporary SQLite3 instead.")
            open(f'{gettempdir()}/loan-db', 'a')
            self.conn = sqlite3.connect(f'{gettempdir()}/loan-db')
            self.isPG = False
            
        self.cur = self.conn.cursor()
    
    # Initialize methods
    def CreateTables(self) -> None:
        '''Create necessary tables and types to store Posts. Wipes any data already present.'''
        
        # Check if Enum types already exists, 'IF NOT EXISTS' does not work here.
        self.cur.execute("DROP TABLE IF EXISTS Posts;")
        
        # Use Enums for Postgres
        if self.isPG:
            self.cur.execute("""DROP TYPE IF EXISTS Status;
                                DROP TYPE IF EXISTS Currency;""")

            # Enum types mirroring those from Post model
            self.cur.execute("CREATE TYPE Status AS ENUM ('REQ', 'PAID', 'UNPAID', 'LATE', 'INVALID')")
            self.cur.execute("CREATE TYPE Currency AS ENUM ('USD', 'EUR', 'GBP', 'CAD', 'XXX')")
        
        # Create fresh table, uses ternary statements to apply correct SQL dialect
        self.cur.execute(f'''
            CREATE TABLE Posts(
                id VARCHAR(7) PRIMARY KEY,
                timestamp TIMESTAMP,
                status {'Status' if self.isPG else 'VARCHAR(7)'},
                currency {'Currency' if self.isPG else 'VARCHAR(3)'}, 
                amount INTEGER,
                isActive BOOL,
                title VARCHAR(200));''')
        self.conn.commit()
    
    # CRUD methods
    def InsertPost(self, p: Post) -> None:
        '''Store Post in the database'''
        self.cur.execute(f"""INSERT INTO Posts 
                                VALUES {'(%s, %s, %s, %s, %s, %s, %s)' if self.isPG 
                                        else '(?, ?, ?, ?, ?, ?, ?)'}
                                ON CONFLICT DO NOTHING""",
                         (p.id, p.timestamp, p.status.name, p.currency.name, p.amount, p.isActive, p.title))
        self.conn.commit()
        
    def InsertPostList(self, pList: list[Post]) -> None:
        '''Store a list of Posts inside the database'''
        
        l: list[Post] = []
        for p in pList:
            l.append((p.id, p.timestamp, p.status.name, p.currency.name, p.amount, p.isActive, p.title))
        
        self.cur.executemany(f"""INSERT INTO Posts 
                             VALUES {'(%s, %s, %s, %s, %s, %s, %s)' if self.isPG 
                                    else '(?, ?, ?, ?, ?, ?, ?)'}
                             ON CONFLICT DO NOTHING""", l)
        self.conn.commit()
        
    def GetAllPosts(self) -> list[tuple]:
        '''Returns every Post in the database as a list of tuples'''
        self.cur.execute('SELECT * FROM Posts')
        return self.cur.fetchall()

    def GetPostsByCurrency(self, currency: Currency) -> list[tuple]:
        '''Filter by currency (e.g. USD) and return every Post as a list of tuples'''
        self.cur.execute(f"SELECT * FROM Posts WHERE currency = {'(%s)' if self.isPG else '(?)'}", 
                         (currency.name,))
        return self.cur.fetchall()
        
    def GetPostsByStatus(self, status: Status) -> list[tuple]:
        '''Filter by status (e.g. [REQ]) and return every Post as a list of tuples'''
        self.cur.execute(f"SELECT * FROM Posts WHERE status = {'(%s)' if self.isPG else '(?)'}", 
                         (status.name,))
        return self.cur.fetchall()

# Currently unused, not implemented for this update
#    def GetPostsByTimestamp(self, days: int) -> list[tuple]:
#        '''Filter by exact date, N days from now. 
#           Only 0-90 days are valid, anything outside this range will be clamped'''
#        
#        # Clamp value to clean input. 
#        try: days = min(max(days, 0), 90)
#        except TypeError: return []
#        
#        self.cur.execute("SELECT * FROM Posts WHERE timestamp::date = CURRENT_DATE - (%s)", (days,))
#        return self.cur.fetchall()
#    
#    def GetPostsByStatusAndTimestamp(self, days:int, status:Status) -> list[tuple]:
#        '''Filter by status and exact date, N days from now. 
#           Only 0-90 days are valid, anything outside this range will be clamped'''
#        
#        # Clamp value to clean input.
#        try: days = min(max(days, 0), 90)
#        except TypeError: return []
#        if status == Status.REQ:
#            self.cur.execute("SELECT * FROM Posts WHERE timestamp::date = CURRENT_DATE - (%s) AND status = 'REQ'", (days,))
#        elif status == Status.PAID:
#            self.cur.execute("SELECT * FROM Posts WHERE timestamp::date = CURRENT_DATE - (%s) AND status = 'PAID'", (days,))
#        else:
#            return []
#
#        return self.cur.fetchall()
    
    def GetNullActiveLoanRequests(self) -> list[str]:
        '''[REQ] Posts should either be active or not. 
        A quick predicate check is done beforehand, but not all are directly visible without comments.'''
        self.cur.execute("SELECT id FROM Posts WHERE status = 'REQ' AND isactive IS NULL")
        NullPosts = []
        for id in self.cur.fetchall():
            NullPosts.append(id[0])
        
        return NullPosts
    
    def UpdateActiveOnLoan(self, id:str, active:bool) -> None:
        '''Update the IsActive field of a Post'''
        self.cur.execute(f"""UPDATE Posts 
                            SET isactive = {'(%s)' if self.isPG else '(?)'} 
                            WHERE id = {'(%s)' if self.isPG else '(?)'}""", 
                            (active,id))
        self.conn.commit()
        
    def AnonymizeData(self) -> None:
        '''Change Post ID to incrementing index and remove title data.'''
        self.cur.execute("SELECT id FROM Posts")
        idx = 1
        for p in self.cur.fetchall():
            self.cur.execute(f"""UPDATE Posts SET id = {'(%s)' if self.isPG else '(?)'}, 
                                title = NULL 
                                WHERE id = {'(%s)' if self.isPG else '(?)'};""", 
                                (str(idx), p[0]))
            idx += 1
        
        # Postgres supports converting table type from str to int, SQLite3 does not.
        # This does not serve any other practical purpose other than house-cleaning right now.
        if self.isPG:
            self.cur.execute("ALTER TABLE Posts ALTER COLUMN id TYPE INTEGER USING id::INTEGER;")
        self.conn.commit()
        
    # Data points
    def LoansRequestedOnDate(self, day:int) -> int:
        if self.isPG:
            self.cur.execute("""
                            SELECT count(*) FROM Posts 
                            WHERE timestamp::date = CURRENT_DATE - (%s) AND status = 'REQ'
                            """, (day,))
        else:
            # Confirm that day is a number
            try: int(day)
            except ValueError:
                return 0
            
            self.cur.execute(f"""
                            SELECT count(*) FROM Posts 
                            WHERE date(timestamp) = date('now', '-{day} days') AND status = 'REQ'
                            """)
        return self.cur.fetchone()[0]
    
    def LoansGivenOnDate(self, day:int) -> int:
        if self.isPG:
            self.cur.execute("""
                            SELECT count(*) FROM Posts 
                            WHERE timestamp::date = CURRENT_DATE - (%s) 
                            AND status = 'REQ' AND isactive = true
                            """, (day,))
        else:
            try: int(day)
            except ValueError:
                return 0
            
            self.cur.execute(f"""
                            SELECT count(*) FROM Posts 
                            WHERE date(timestamp) = date('now', '-{day} days') 
                            AND status = 'REQ' AND isactive = true
                            """)
        return self.cur.fetchone()[0]
    
    def LoanAmountRequestedOnDate(self, day:int) -> int:
        # TODO: Apply exchange rate to USD
        if self.isPG:
            self.cur.execute("""
                            SELECT sum(amount) FROM Posts 
                            WHERE timestamp::date = CURRENT_DATE - (%s) AND status = 'REQ'
                            """, (day,))
        else:
            try: int(day)
            except ValueError:
                return 0
            
            self.cur.execute(f"""
                            SELECT sum(amount) FROM Posts 
                            WHERE date(timestamp) = date('now', '-{day} days') AND status = 'REQ'
                            """)
        amount = self.cur.fetchone()[0]
        if amount == None:
            amount = 0
        return amount
    
    def LoanAmountGivenOnDate(self, day:int) -> int:
        # TODO: Apply exchange rate to USD
        if self.isPG:
            self.cur.execute("""
                            SELECT sum(amount) FROM Posts 
                            WHERE timestamp::date = CURRENT_DATE - (%s) 
                            AND status = 'REQ' AND isactive = true
                            """, (day,))
        else:
            try: int(day)
            except ValueError:
                return 0
            
            self.cur.execute(f"""
                            SELECT sum(amount) FROM Posts 
                            WHERE date(timestamp) = date('now', '-{day} days') 
                            AND status = 'REQ' and isactive = true
                            """)
        amount = self.cur.fetchone()[0]
        if amount == None: amount = 0
        return amount
    
    def LoanPaidAndDefaultRate(self, day:int) -> tuple[int, int]:
        '''More experimental query in returning multiple datapoints in one call'''
        if self.isPG:
            self.cur.execute("""
                            WITH paid AS (
                                SELECT COUNT(*) as paid FROM Posts 
                                WHERE timestamp::date = CURRENT_DATE - (%s) 
                                AND status = 'PAID'
                            ), unpaid AS (
                                SELECT COUNT(*) as unpaid FROM Posts 
                                WHERE timestamp::date = CURRENT_DATE - (%s) 
                                AND status = 'UNPAID'
                            )
                            
                            SELECT * FROM paid, unpaid;
                            """, (day,day))
        else:
            try: int(day)
            except ValueError:
                return 0
            
            self.cur.execute(f"""
                         WITH paid AS (
                             SELECT COUNT(*) as paid FROM Posts 
                             WHERE date(timestamp) = date('now', '-{day} days') 
                             AND status = 'PAID'
                         ), unpaid AS (
                             SELECT COUNT(*) as unpaid FROM Posts 
                             WHERE date(timestamp) = date('now', '-{day} days') 
                             AND status = 'UNPAID'
                         )
                         
                         SELECT * FROM paid, unpaid;
                         """)
        
        return self.cur.fetchone()

    def CloseConnection(self) -> None:
        '''Ensure a clean disconnect from the database, without using a context manager'''
        self.conn.close()