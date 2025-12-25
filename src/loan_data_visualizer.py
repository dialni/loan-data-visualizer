from models import *
import reddit_api
import db_api

if __name__ == "__main__":
    api = reddit_api.APITool()
    db = db_api.Database()
    
    api.Auth()    
    db.CreateTables()
    
    posts = api.TestExample()
    db.InsertPostList(posts)
    
    db_posts = db.GetPostsByTimestamp(7)
    for p in db_posts:
        print(p)
    
    db.CloseConnection()