# reddit_scraper.py
import praw
import json
import pandas as pd
from datetime import datetime
from config import Config
import os

class RedditScraper:
    def __init__(self):
        """Initialize Reddit API connection"""
        Config.validate_credentials()
        
        self.reddit = praw.Reddit(
            client_id=Config.REDDIT_CLIENT_ID,
            client_secret=Config.REDDIT_CLIENT_SECRET,
            user_agent=Config.REDDIT_USER_AGENT
        )
        print(f"Connected to Reddit API")
    
    def scrape_subreddit(self, subreddit_name, limit=100, time_filter='month'):
        """Scrape posts from a single subreddit"""
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            posts_data = []
            
            print(f"Scraping r/{subreddit_name} (limit: {limit}, time_filter: {time_filter})...")
            
            # Get top posts from the subreddit
            posts = subreddit.top(time_filter=time_filter, limit=limit)
            
            for post in posts:
                # Skip posts with low score
                if post.score < Config.MIN_SCORE:
                    continue
                
                # Combine title and selftext for analysis
                text_content = post.title
                if post.selftext and len(post.selftext.strip()) > 0:
                    text_content += " " + post.selftext
                
                # Skip posts with very little text content
                if len(text_content.strip()) < 50:
                    continue
                
                # Collect top comments
                print(f"Processing post: {post.title[:50]}...")
                post.comments.replace_more(limit=0)  # Don't load "more comments"
                
                comments_text = ""
                comment_count = 0
                for comment in post.comments[:5]:  # Top 5 comments only
                    if hasattr(comment, 'body') and len(comment.body.strip()) > 10:
                        comments_text += " " + comment.body
                        comment_count += 1
                
                # Combine post text + comments for TF-IDF analysis
                full_text_content = text_content
                if comments_text.strip():
                    full_text_content += " " + comments_text
                
                post_data = {
                    'id': post.id,
                    'title': post.title,
                    'selftext': post.selftext,
                    'text_content': text_content,  # Post text only
                    'comments_text': comments_text.strip(),  # Comments only
                    'full_text_content': full_text_content,  # Combined for TF-IDF
                    'score': post.score,
                    'num_comments': post.num_comments,
                    'scraped_comments': comment_count,
                    'created_utc': post.created_utc,
                    'subreddit': subreddit_name,
                    'author': str(post.author) if post.author else '[deleted]',
                    'url': post.url,
                    'upvote_ratio': post.upvote_ratio,
                    'is_self': post.is_self,
                    'flair': post.link_flair_text,
                    'permalink': f"https://reddit.com{post.permalink}",
                    'text_length': len(full_text_content)
                }
                
                posts_data.append(post_data)
            
            print(f"Scraped {len(posts_data)} valid posts from r/{subreddit_name}")
            return posts_data
            
        except Exception as e:
            print(f"Error scraping r/{subreddit_name}: {str(e)}")
            return []
    
    def scrape_multiple_subreddits(self, subreddits=None, limit=None, time_filter=None):
        """Scrape posts from multiple subreddits"""
        if subreddits is None:
            subreddits = Config.SUBREDDITS
        if limit is None:
            limit = Config.POST_LIMIT
        if time_filter is None:
            time_filter = Config.TIME_FILTER
            
        all_posts = []
        
        print(f"Starting scrape of {len(subreddits)} subreddits")
        print(f"Settings: {limit} posts per subreddit, time_filter='{time_filter}', min_score={Config.MIN_SCORE}")
        
        for subreddit_name in subreddits:
            posts = self.scrape_subreddit(subreddit_name, limit, time_filter)
            all_posts.extend(posts)
        
        print(f"Total valid posts scraped: {len(all_posts)}")
        return all_posts
    
    def save_raw_data(self, posts_data, filename=None):
        """Save raw scraped data to JSON file"""
        if filename is None:
            filename = Config.RAW_DATA_FILE
        
        # Create output directory if it doesn't exist
        os.makedirs(Config.OUTPUT_DIR, exist_ok=True)
        
        filepath = os.path.join(Config.OUTPUT_DIR, filename)
        
        # Add metadata
        output_data = {
            'metadata': {
                'scraped_at': datetime.now().isoformat(),
                'total_posts': len(posts_data),
                'subreddits': list(set([post['subreddit'] for post in posts_data])),
                'config': {
                    'post_limit': Config.POST_LIMIT,
                    'min_score': Config.MIN_SCORE,
                    'time_filter': Config.TIME_FILTER
                }
            },
            'posts': posts_data
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"Raw data saved to: {filepath}")
        return filepath

def main():
    """Main function to run the scraper"""
    print("Reddit Data Scraper for TF-IDF Analysis")
    print("=" * 50)
    
    scraper = RedditScraper()
    
    # Scrape data
    posts = scraper.scrape_multiple_subreddits()
    
    # Save raw data
    if posts:
        scraper.save_raw_data(posts)
        print("\nScraping completed successfully!")
        
        # Print summary statistics
        df = pd.DataFrame(posts)
        print("\nSummary Statistics:")
        print(f"Total posts: {len(df)}")
        print(f"Subreddits: {', '.join(df['subreddit'].unique())}")
        print(f"Score range: {df['score'].min()} - {df['score'].max()}")
        print(f"Average score: {df['score'].mean():.1f}")
        print(f"Text length range: {df['text_length'].min()} - {df['text_length'].max()}")
        print(f"Average text length: {df['text_length'].mean():.0f} characters")
        
        if len(df['subreddit'].unique()) > 1:
            print(f"\nPosts by subreddit:")
            print(df['subreddit'].value_counts())
        
        print(f"\nSample posts:")
        for i, row in df.head(3).iterrows():
            print(f"{i+1}. {row['title'][:60]}{'...' if len(row['title']) > 60 else ''}")
            print(f"   Score: {row['score']}, Text length: {row['text_length']} chars")
            
    else:
        print("No posts were scraped!")

if __name__ == "__main__":
    main()