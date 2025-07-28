import json
import pandas as pd
from openai import OpenAI
from config import Config
import os
from dotenv import load_dotenv
from collections import defaultdict

load_dotenv()

class TrendAnalysisClassifier:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.posts_df = None
        
        # Predefined main themes for consistency
        self.main_themes = [
            "Finance", "Productivity", "AI/ML Tools", "Web Development", 
            "Mobile Apps", "Browser Extensions", "Games", "Health & Fitness",
            "Education", "Social/Communication", "E-commerce", "Data/Analytics",
            "Content Creation", "Automation", "Security/Privacy", "Entertainment",
            "Lifestyle", "Business Tools", "Developer Tools", "Other"
        ]
        
    def load_reddit_data(self):
        """Load scraped Reddit data"""
        filepath = os.path.join(Config.OUTPUT_DIR, Config.RAW_DATA_FILE)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.posts_df = pd.DataFrame(data['posts'])
        print(f"✅ Loaded {len(self.posts_df)} posts")
        return self.posts_df
    
    def classify_single_post(self, title, description, comments=""):
        """Enhanced classification with specific problem descriptions"""
        
        # Combine all text for better context
        full_text = f"{title}. {description}. {comments[:200]}"
        
        prompt = f"""
Analyze this project and extract specific, actionable insights for trend analysis.

Project: {full_text[:800]}

Create a SPECIFIC problem description that includes:
- WHO has this problem (target audience)
- WHAT exactly they struggle with (specific pain point)
- WHY it's costly/painful (time, money, effort wasted)
- HOW this solution helps (specific benefit)

GOOD EXAMPLES:
- "Small business owners spend 5+ hours weekly manually searching Reddit for customers mentioning their services, missing 80% of opportunities and losing potential $2000+ monthly revenue to competitors who respond faster"
- "Freelance designers waste 4-6 hours creating brand packages (logo, colors, fonts) for each client, delaying project delivery and reducing hourly rate from $100 to $30 due to unpaid design time"
- "Content creators lose 6+ hours weekly reformatting videos into slide presentations, missing deadlines and losing $500+ per delayed client project"

Choose ONE main theme from: {', '.join(self.main_themes)}

Respond with ONLY valid JSON:
{{
    "main_theme": "theme_name",
    "sub_themes": ["specific_sub1", "specific_sub2"],
    "problem_solved": "Detailed WHO/WHAT/WHY/HOW problem description with specific numbers/impacts",
    "target_audience": "Specific user group",
    "pain_points": ["specific pain 1", "specific pain 2"],
    "business_impact": "Revenue/time/efficiency impact",
    "solution_type": "Automation/Tool/Platform/Service",
    "trend_indicators": ["keyword1", "keyword2"],
    "confidence": 0.8
}}
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a classifier. Return only valid JSON, no markdown formatting, no explanations."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=250
            )
            
            result = response.choices[0].message.content.strip()
            
            # Clean up common JSON formatting issues
            result = result.replace('```json', '').replace('```', '').strip()
            
            # Try to parse JSON
            try:
                parsed_result = json.loads(result)
                
                # Validate required fields
                required_fields = ['main_theme', 'sub_themes', 'problem_solved', 'trend_indicators', 'confidence']
                if not all(key in parsed_result for key in required_fields):
                    # Handle missing fields gracefully
                    for field in required_fields:
                        if field not in parsed_result:
                            if field == 'target_audience':
                                parsed_result[field] = "General users"
                            elif field == 'pain_points':
                                parsed_result[field] = ["Unspecified pain point"]
                            elif field == 'business_impact':
                                parsed_result[field] = "Unknown impact"
                            elif field == 'solution_type':
                                parsed_result[field] = "Tool"
                            elif field == 'sub_themes':
                                parsed_result[field] = ["General"]
                            elif field == 'problem_solved':
                                parsed_result[field] = "Problem solving tool"
                            elif field == 'trend_indicators':
                                parsed_result[field] = []
                            elif field == 'confidence':
                                parsed_result[field] = 0.5
                
                # Ensure main_theme is in our predefined list
                if parsed_result['main_theme'] not in self.main_themes:
                    print(f"⚠️ Unknown theme '{parsed_result['main_theme']}', defaulting to 'Other'")
                    parsed_result['main_theme'] = 'Other'
                
                print(f"✅ Classified as: {parsed_result.get('main_theme')} -> {parsed_result.get('sub_themes')}")
                return parsed_result
                
            except (json.JSONDecodeError, ValueError, KeyError) as e:
                print(f"⚠️ JSON parsing failed: {e}")
                print(f"Raw response: {result[:200]}...")
                
                # Try to extract theme with regex as fallback
                return self._fallback_classification(title, description, result)
            
        except Exception as e:
            print(f"❌ API Error: {e}")
            return self._fallback_classification(title, description, f"API Error: {str(e)}")
    
    def _fallback_classification(self, title, description, raw_response=""):
        """Fallback classification using simple keyword matching"""
        text = f"{title} {description}".lower()
        
        # Simple keyword-based classification
        if any(word in text for word in ['finance', 'money', 'budget', 'invest', 'crypto', 'payment', 'bank']):
            main_theme = 'Finance'
            sub_themes = ['Personal Finance']
        elif any(word in text for word in ['ai', 'ml', 'gpt', 'chatbot', 'llm', 'neural']):
            main_theme = 'AI/ML Tools'
            sub_themes = ['AI Assistant']
        elif any(word in text for word in ['web', 'website', 'html', 'css', 'javascript', 'react']):
            main_theme = 'Web Development'
            sub_themes = ['Web Apps']
        elif any(word in text for word in ['mobile', 'app', 'ios', 'android', 'flutter']):
            main_theme = 'Mobile Apps'
            sub_themes = ['Mobile Development']
        elif any(word in text for word in ['chrome', 'extension', 'browser', 'firefox']):
            main_theme = 'Browser Extensions'
            sub_themes = ['Browser Tools']
        elif any(word in text for word in ['game', 'gaming', 'play', 'puzzle']):
            main_theme = 'Games'
            sub_themes = ['Entertainment Games']
        elif any(word in text for word in ['productivity', 'task', 'todo', 'organize', 'manage']):
            main_theme = 'Productivity'
            sub_themes = ['Task Management']
        else:
            main_theme = 'Other'
            sub_themes = ['Miscellaneous']
        
        return {
            "main_theme": main_theme,
            "sub_themes": sub_themes,
            "problem_solved": f"{main_theme} solution addressing common workflow challenges",
            "target_audience": "General users",
            "pain_points": ["Efficiency challenges"],
            "business_impact": "Time savings",
            "solution_type": "Tool",
            "trend_indicators": [],
            "confidence": 0.3,
            "fallback_used": True,
            "raw_response": raw_response
        }
    
    def classify_batch(self, limit=None):
        """Classify posts and save structured results for trend analysis"""
        if limit:
            posts_to_process = self.posts_df.head(limit)
        else:
            posts_to_process = self.posts_df
            
        print(f"🤖 Classifying {len(posts_to_process)} posts for trend analysis...")
        
        results = []
        theme_stats = defaultdict(lambda: {"count": 0, "total_score": 0, "sub_themes": defaultdict(int)})
        
        for idx, row in posts_to_process.iterrows():
            print(f"\nProcessing {idx+1}/{len(posts_to_process)}: {row['title'][:50]}...")
            
            classification = self.classify_single_post(
                row['title'], 
                row.get('selftext', '') or row.get('text_content', ''),
                row.get('comments_text', '')
            )
            
            # Build comprehensive result
            result = {
                'post_id': row['id'],
                'title': row['title'],
                'score': int(row['score']),
                'num_comments': int(row['num_comments']),
                'upvote_ratio': float(row['upvote_ratio']),
                'created_utc': row.get('created_utc', 0),
                'subreddit': row.get('subreddit', ''),
                'author': row.get('author', ''),
                'url': row.get('url', ''),           
                'permalink': row.get('permalink', ''),
                
                'main_theme': classification['main_theme'],
                'sub_themes': classification['sub_themes'],
                'problem_solved': classification['problem_solved'],
                'target_audience': classification.get('target_audience', 'General users'),
                'pain_points': classification.get('pain_points', []),
                'business_impact': classification.get('business_impact', 'Unknown impact'),
                'solution_type': classification.get('solution_type', 'Tool'),
                'trend_indicators': classification['trend_indicators'],
                'confidence': classification['confidence']
            }
            
            results.append(result)
            
            # Update statistics for trend analysis
            main_theme = classification['main_theme']
            theme_stats[main_theme]["count"] += 1
            theme_stats[main_theme]["total_score"] += int(row['score'])
            
            for sub_theme in classification['sub_themes']:
                theme_stats[main_theme]["sub_themes"][sub_theme] += 1
            
            # Be nice to the API
            import time
            time.sleep(0.5)
        
        # Save detailed results
        output_file = os.path.join(Config.OUTPUT_DIR, 'trend_analysis_results.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        # Generate trend summary for easy graphing
        trend_summary = self.generate_trend_summary(theme_stats, results)
        
        summary_file = os.path.join(Config.OUTPUT_DIR, 'trend_summary.json')
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(trend_summary, f, indent=2, ensure_ascii=False)
        
        # Generate CSV for easy graphing
        self.generate_csv_for_graphing(results)
        
        print(f"\nResults saved to: {output_file}")
        print(f"Trend summary saved to: {summary_file}")
        print(f"CSV for graphing saved to: trend_data.csv")
        
        return results, trend_summary
    
    def generate_trend_summary(self, theme_stats, results):
        """Generate summary data perfect for trend visualization"""
        
        # Main themes summary
        themes_summary = []
        for theme, stats in theme_stats.items():
            avg_score = stats["total_score"] / stats["count"] if stats["count"] > 0 else 0
            
            # Get top sub-themes
            top_sub_themes = sorted(stats["sub_themes"].items(), 
                                  key=lambda x: x[1], reverse=True)[:5]
            
            themes_summary.append({
                "main_theme": theme,
                "post_count": stats["count"],
                "total_score": stats["total_score"],
                "avg_score": round(avg_score, 2),
                "percentage": round((stats["count"] / len(results)) * 100, 2),
                "top_sub_themes": [{"name": name, "count": count} for name, count in top_sub_themes]
            })
        
        # Sort by post count
        themes_summary.sort(key=lambda x: x["post_count"], reverse=True)
        
        # Sub-themes global ranking
        all_sub_themes = defaultdict(int)
        for result in results:
            for sub_theme in result['sub_themes']:
                all_sub_themes[sub_theme] += 1
        
        top_global_sub_themes = sorted(all_sub_themes.items(), 
                                     key=lambda x: x[1], reverse=True)[:20]
        
        # Trend indicators analysis
        all_trend_indicators = defaultdict(int)
        for result in results:
            for indicator in result['trend_indicators']:
                all_trend_indicators[indicator] += 1
        
        top_trend_indicators = sorted(all_trend_indicators.items(), 
                                    key=lambda x: x[1], reverse=True)[:15]
        
        return {
            "summary_stats": {
                "total_posts": len(results),
                "unique_main_themes": len(theme_stats),
                "unique_sub_themes": len(all_sub_themes),
                "avg_score_all_posts": round(sum(r['score'] for r in results) / len(results), 2)
            },
            "main_themes_ranking": themes_summary,
            "top_sub_themes_global": [{"name": name, "count": count} for name, count in top_global_sub_themes],
            "top_trend_indicators": [{"indicator": name, "count": count} for name, count in top_trend_indicators]
        }
    
    def generate_csv_for_graphing(self, results):
        """Generate CSV files optimized for graphing"""
        
        # Main CSV with all data
        df = pd.DataFrame(results)
        csv_file = os.path.join(Config.OUTPUT_DIR, 'trend_data.csv')
        df.to_csv(csv_file, index=False)
        
        # Theme counts for pie/bar charts
        theme_counts = df['main_theme'].value_counts()
        theme_df = pd.DataFrame({
            'theme': theme_counts.index,
            'count': theme_counts.values,
            'percentage': (theme_counts.values / len(df) * 100).round(2)
        })
        
        theme_csv = os.path.join(Config.OUTPUT_DIR, 'theme_counts.csv')
        theme_df.to_csv(theme_csv, index=False)
        
        # Sub-themes data
        sub_themes_data = []
        for _, row in df.iterrows():
            for sub_theme in row['sub_themes']:
                sub_themes_data.append({
                    'main_theme': row['main_theme'],
                    'sub_theme': sub_theme,
                    'score': row['score'],
                    'comments': row['num_comments']
                })
        
        sub_themes_df = pd.DataFrame(sub_themes_data)
        sub_csv = os.path.join(Config.OUTPUT_DIR, 'sub_themes_data.csv')
        sub_themes_df.to_csv(sub_csv, index=False)
        
        print(f"Generated CSV files for graphing:")
        print(f"   - Main data: trend_data.csv")
        print(f"   - Theme counts: theme_counts.csv") 
        print(f"   - Sub-themes: sub_themes_data.csv")
    
    def enhance_existing_results(self, input_file='trend_analysis_results.json'):
        """Enhance existing results with better problem descriptions"""
        filepath = os.path.join(Config.OUTPUT_DIR, input_file)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            results = json.load(f)
        
        print(f"Enhancing {len(results)} existing results with better problem descriptions...")
        
        enhanced_results = []
        
        for i, result in enumerate(results):
            print(f"Enhancing {i+1}/{len(results)}: {result['title'][:50]}...")
            
            # Create enhanced problem description
            enhanced_prompt = f"""
Based on this project, create a specific problem description that includes WHO, WHAT, WHY, and HOW with concrete numbers.

Title: {result['title']}
Current Description: {result.get('problem_solved', 'No description')}
Theme: {result['main_theme']} -> {result['sub_themes']}

Create a problem description following this format:
"TARGET_AUDIENCE struggle with SPECIFIC_PROBLEM, wasting TIME_AMOUNT/MONEY_AMOUNT because REASON, so this solution SPECIFIC_BENEFIT"

Examples:
- "E-commerce store owners waste 10+ hours weekly manually tracking competitor prices across 50+ products, losing $5000+ monthly to competitors with better pricing, so this tool automatically monitors prices and suggests optimal pricing in real-time"
- "Social media managers spend 15+ hours weekly creating content calendars manually, missing posting deadlines and losing 30% audience engagement, so this platform auto-generates content schedules based on optimal engagement times"

Return only the enhanced problem description (no quotes, no extra text):
"""

            try:
                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": enhanced_prompt}],
                    temperature=0.2,
                    max_tokens=200
                )
                
                enhanced_problem = response.choices[0].message.content.strip()
                result['enhanced_problem'] = enhanced_problem
                
            except Exception as e:
                print(f"Enhancement failed: {e}")
                result['enhanced_problem'] = result.get('problem_solved', 'Problem description unavailable')
            
            enhanced_results.append(result)
            
            # Rate limiting
            import time
            time.sleep(0.3)
        
        # Save enhanced results
        enhanced_file = os.path.join(Config.OUTPUT_DIR, 'enhanced_trend_results.json')
        with open(enhanced_file, 'w', encoding='utf-8') as f:
            json.dump(enhanced_results, f, indent=2, ensure_ascii=False)
        
        print(f"Enhanced results saved to: {enhanced_file}")
        return enhanced_results

def main():
    """Run trend analysis classification"""
    classifier = TrendAnalysisClassifier()
    classifier.load_reddit_data()
    results, summary = classifier.classify_batch()
    
    print("\nTREND ANALYSIS COMPLETE!")
    print(f"Found {len(summary['main_themes_ranking'])} main themes")
    print(f"Top 3 themes:")
    for i, theme in enumerate(summary['main_themes_ranking'][:3], 1):
        print(f"   {i}. {theme['main_theme']}: {theme['post_count']} posts ({theme['percentage']}%)")
    
    # Ask if user wants to enhance existing results
    enhance_choice = input("\n🔧 Enhance existing results with better problem descriptions? (y/n): ").lower().strip()
    if enhance_choice == 'y':
        classifier.enhance_existing_results()

def enhance_only():
    """Just enhance existing results without re-classifying"""
    classifier = TrendAnalysisClassifier()
    enhanced = classifier.enhance_existing_results()
    print(f"\nEnhanced {len(enhanced)} results with better problem descriptions!")

if __name__ == "__main__":
    main()