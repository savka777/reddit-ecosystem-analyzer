// simple_graph_data.js - Simple Category Analysis
export const simpleGraphData = {
  "nodes": [
    {
      "id": "games",
      "name": "Games",
      "val": 7,
      "color": "#ff6b6b",
      "group": 1,
      "category": "main_category",
      "post_count": 7,
      "avg_engagement": 208.0,
      "avg_score": 311.9,
      "total_score": 2183,
      "opportunity_level": "High Opportunity",
      "sample_titles": [
        "I built an infinite pixel art canvas. People have drawn 416 million individual pixels on it.",
        "My side project went from 27 to 4,200 users overnight, still trying to figure out how.",
        "Launched my free game 30 days ago"
      ]
    },
    {
      "id": "ai-tools-web-development",
      "name": "AI Tools/Web Development",
      "val": 5,
      "color": "#ff6b6b",
      "group": 1,
      "category": "main_category",
      "post_count": 5,
      "avg_engagement": 197.6,
      "avg_score": 307.2,
      "total_score": 1536,
      "opportunity_level": "High Opportunity",
      "sample_titles": [
        "My first AI startup, born in the /vue-tutorial folder, now ~15 new users per day",
        "I made an simple all-in-one online resume builder to create your resume and for free (it even has AI)",
        "From chat to launch in under 2 minutes; meet your new AI web builder"
      ]
    },
    {
      "id": "other",
      "name": "Other",
      "val": 15,
      "color": "#4ecdc4",
      "group": 1,
      "category": "main_category",
      "post_count": 57,
      "avg_engagement": 186.2,
      "avg_score": 246.0,
      "total_score": 14024,
      "opportunity_level": "High Engagement",
      "sample_titles": [
        "I made tinder but it\u2019s only pictures of my wife and I can only swipe right",
        "I made 3D bust maker: immortalize your special moments. Ready for 3D printing",
        "I've launched 37 products in 5 years and not doing that again"
      ]
    },
    {
      "id": "mobile-apps",
      "name": "Mobile Apps",
      "val": 15,
      "color": "#4ecdc4",
      "group": 1,
      "category": "main_category",
      "post_count": 54,
      "avg_engagement": 159.3,
      "avg_score": 216.8,
      "total_score": 11708,
      "opportunity_level": "High Engagement",
      "sample_titles": [
        "My App surpassed $100k in revenue",
        "my first app reached 500 users and i'm so happy",
        "MY augmented reality project"
      ]
    },
    {
      "id": "browser-extensions",
      "name": "Browser Extensions",
      "val": 15,
      "color": "#ddd",
      "group": 1,
      "category": "main_category",
      "post_count": 23,
      "avg_engagement": 139.5,
      "avg_score": 204.3,
      "total_score": 4700,
      "opportunity_level": "Oversaturated",
      "sample_titles": [
        "Created a Chrome extension to practice typing on any website",
        "I built a tool that forces you to scream \"I'm a loser\" to unlock social media",
        "I made a browser extension that calculates your carbon footprint when you shop online!"
      ]
    },
    {
      "id": "web-development",
      "name": "Web Development",
      "val": 15,
      "color": "#ddd",
      "group": 1,
      "category": "main_category",
      "post_count": 72,
      "avg_engagement": 134.9,
      "avg_score": 166.5,
      "total_score": 11987,
      "opportunity_level": "Oversaturated",
      "sample_titles": [
        "Built a Fake DM creation tool (went viral on X and got Featured on TechCrunch)",
        "I Built a Pornstar Analytics Platform",
        "Built a DEFCON-style dashboard that tracks Pentagon pizza shop activity. It went viral."
      ]
    },
    {
      "id": "ai-tools",
      "name": "AI Tools",
      "val": 15,
      "color": "#ddd",
      "group": 1,
      "category": "main_category",
      "post_count": 60,
      "avg_engagement": 120.5,
      "avg_score": 131.7,
      "total_score": 7899,
      "opportunity_level": "Oversaturated",
      "sample_titles": [
        "Using AI to detect and mute commercials while watching TV.",
        "My girlfriend made this app to take my stress away.",
        "This side project made me 100$ in a week."
      ]
    },
    {
      "id": "finance",
      "name": "Finance",
      "val": 7,
      "color": "#45b7d1",
      "group": 1,
      "category": "main_category",
      "post_count": 7,
      "avg_engagement": 109.1,
      "avg_score": 123.9,
      "total_score": 867,
      "opportunity_level": "Moderate",
      "sample_titles": [
        "I build this App since I\u2019m tired of tracking credit card benefits",
        "We have a new billionaire (if he's not Bullshitting)",
        "The 9 seconds Reel that got me 40K followers (Here\u2019s Exactly How)"
      ]
    },
    {
      "id": "[other]",
      "name": "[Other]",
      "val": 3,
      "color": "#45b7d1",
      "group": 1,
      "category": "main_category",
      "post_count": 3,
      "avg_engagement": 84.8,
      "avg_score": 96.7,
      "total_score": 290,
      "opportunity_level": "Moderate",
      "sample_titles": [
        "WE GOT OUR FIRST CUSTOMER AFTER MONTHS OF BUILDING",
        "Just made my sixth $1,000 with my side project today \ud83e\udd73",
        "I built Wallper \u2013 a macOS app for 4K animated wallpapers, because I couldn\u2019t find anything like Wallpaper Engine"
      ]
    }
  ],
  "links": [
    {
      "source": "games",
      "target": "ai-tools-web-development",
      "value": 0.3,
      "relationship": "similar_opportunity"
    },
    {
      "source": "ai-tools-web-development",
      "target": "other",
      "value": 0.3,
      "relationship": "similar_opportunity"
    },
    {
      "source": "other",
      "target": "mobile-apps",
      "value": 0.3,
      "relationship": "similar_opportunity"
    }
  ],
  "metadata": {
    "type": "simple_categories",
    "total_categories": 9,
    "total_posts_analyzed": 288,
    "date_created": "latest"
  }
};