# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Reddit API credentials
    REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
    REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
    REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT')
    OPENAI_API_KEY= os.getenv('OPENAI_API_KEY')
    
    # Analysis settings
    SUBREDDITS = ['SideProject'] 
    POST_LIMIT = 300 
    MIN_SCORE = 1 
    TIME_FILTER = 'month'
    
    # Output settings
    OUTPUT_DIR = '../results/public/data/'
    RAW_DATA_FILE = 'raw_reddit_data.json'
    GRAPH_DATA_FILE = 'graph_data.json'
    
    @classmethod
    def validate_credentials(cls):
        """Check if all required credentials are loaded"""
        if not cls.REDDIT_CLIENT_ID:
            raise ValueError("REDDIT_CLIENT_ID not found in .env file")
        if not cls.REDDIT_CLIENT_SECRET:
            raise ValueError("REDDIT_CLIENT_SECRET not found in .env file")
        if not cls.REDDIT_USER_AGENT:
            raise ValueError("REDDIT_USER_AGENT not found in .env file")
        print("All credentials loaded successfully")