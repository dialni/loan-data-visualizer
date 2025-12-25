from models import *
import os
import psycopg
from dotenv import load_dotenv

class Database():
    conn: psycopg.Connection
    cur: psycopg.Cursor
    
    def __init__(self):
        '''Tool for easily creating and maintaining access to a postgres database'''
        if not load_dotenv('.env'):
            raise SystemExit('Could not load .env file, exiting.')

        self.conn = psycopg.connect(f'postgres://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@localhost:{os.getenv('POSTGRES_PORT')}/mydb')
        self.cur = self.conn.cursor()
    
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
        '''Filter by timestamp by {1, 7, 30} days from now. Only 1, 7 and 30 are valid
            due to prepared statements and string literals.'''
        match days:
            case 1:
                self.cur.execute("SELECT * FROM Posts WHERE (timestamp > NOW() - INTERVAL '1 DAYS')")
            case 7:
                self.cur.execute("SELECT * FROM Posts WHERE (timestamp > NOW() - INTERVAL '7 DAYS')")
            case 30:
                self.cur.execute("SELECT * FROM Posts WHERE (timestamp > NOW() - INTERVAL '30 DAYS')")
            case _:
                return []
        return self.cur.fetchall()
    
    def CloseConnection(self) -> None:
        '''Ensure a clean disconnect from the database, without using a context manager'''
        self.conn.close()