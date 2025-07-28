# test_reddit.py
import praw
from config import Config

def test_reddit_connection():
    """Test Reddit API connection"""
    try:
        # Validate credentials first
        Config.validate_credentials()
        
        # Create Reddit instance
        reddit = praw.Reddit(
            client_id=Config.REDDIT_CLIENT_ID,
            client_secret=Config.REDDIT_CLIENT_SECRET,
            user_agent=Config.REDDIT_USER_AGENT
        )
        
        print("Testing Reddit API connection...")
        
        # Test connection by getting a few posts from SideProject subreddit
        subreddit = reddit.subreddit('SideProject')
        posts = list(subreddit.hot(limit=5))
        
        print(f"Successfully connected to Reddit API!")
        print(f"Test results:")
        print(f"   - Subreddit: r/SideProject")
        print(f"   - Posts retrieved: {len(posts)}")
        
        print(f"\nSample post titles:")
        for i, post in enumerate(posts, 1):
            print(f"   {i}. {post.title[:60]}{'...' if len(post.title) > 60 else ''}")
            print(f"      Score: {post.score}, Comments: {post.num_comments}")
        
        return True
        
    except ValueError as e:
        print(f"Configuration error: {e}")
        return False
    except Exception as e:
        print(f"Reddit API error: {e}")
        print("\nCommon fixes:")
        print("   - Check your .env file exists in the data-pipeline folder")
        print("   - Verify your Reddit API credentials are correct")
        print("   - Make sure you're connected to the internet")
        return False

if __name__ == "__main__":
    print("Testing Reddit API Connection")
    print("=" * 40)
    
    success = test_reddit_connection()
    
    if success:
        print("\nTest completed successfully!")
        print("You're ready to run the full scraper!")
    else:
        print("\nTest failed. Please fix the issues above.")