import reddit_api

if __name__ == "__main__":
    api = reddit_api.APITool()
    
    #api.Auth()
    #api.TestConnection()
    #posts = api.GetNewestPosts("borrow", 50)
    posts = api.TestExample()
    i = 0
    for p in posts:
        print(p)
        i += 1
        
    print(f"\n\nTotal posts: {i}")