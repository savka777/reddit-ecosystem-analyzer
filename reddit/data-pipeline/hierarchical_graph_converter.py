# hierarchical_graph_converter.py
import json
import os
from config import Config
from collections import defaultdict

def create_hierarchical_graph_data():
    """Create hierarchical graph with main themes as hubs and sub-themes as connected nodes"""
    
    # Load our trend analysis data
    filepath = os.path.join(Config.OUTPUT_DIR, 'trend_analysis_results.json')
    with open(filepath, 'r', encoding='utf-8') as f:
        trend_data = json.load(f)
    
    print(f"Creating hierarchical graph from {len(trend_data)} classified posts...")
    
    # Group sub-themes by main theme and collect problems solved
    themes = defaultdict(lambda: {
        'sub_themes': defaultdict(lambda: {
            'posts': [],
            'post_data': [],  # Store full post objects
            'problems_solved': [],
            'total_score': 0,
            'total_comments': 0,
            'sample_titles': []
        })
    })
    
    # Process each classified post
    for post in trend_data:
        main_theme = post['main_theme']
        post_score = post['score']
        post_comments = post['num_comments']
        engagement = post_score + (post_comments * 10)  # Calculate engagement
        
        # Create post data object for Reddit links
        post_data = {
            'title': post['title'],
            'url': post.get('url', ''),
            'permalink': post.get('permalink', ''),
            'subreddit': post.get('subreddit', 'SideProject'),
            'score': post_score,
            'num_comments': post_comments,
            'author': post.get('author', ''),
            'created_utc': post.get('created_utc', 0)
        }
        
        # Add to each sub-theme for this post
        for sub_theme in post['sub_themes']:
            sub_data = themes[main_theme]['sub_themes'][sub_theme]
            sub_data['posts'].append(post)
            sub_data['post_data'].append(post_data)  # Add full post data
            sub_data['problems_solved'].append(post['problem_solved'])
            sub_data['total_score'] += post_score
            sub_data['total_comments'] += post_comments
            
            # Add sample title if we don't have too many
            if len(sub_data['sample_titles']) < 3:
                sub_data['sample_titles'].append(post['title'])
    
    # Create nodes and links
    nodes = []
    links = []
    
    # Define colors for main themes
    theme_colors = {
        'Finance': '#fdcb6e',
        'Productivity': '#a29bfe',
        'AI/ML Tools': '#ff6b6b',
        'Web Development': '#4ecdc4', 
        'Mobile Apps': '#45b7d1',
        'Browser Extensions': '#96ceb4',
        'Games': '#ffeaa7',
        'Health & Fitness': '#00b894',
        'Education': '#00cec9',
        'Social/Communication': '#ff7675',
        'E-commerce': '#55a3ff',
        'Data/Analytics': '#e17055',
        'Content Creation': '#fab1a0',
        'Automation': '#6c5ce7',
        'Security/Privacy': '#2d3436',
        'Entertainment': '#fd79a8',
        'Lifestyle': '#81ecec',
        'Business Tools': '#74b9ff',
        'Developer Tools': '#e84393',
        'Other': '#ddd'
    }
    
    for theme_name, theme_data in themes.items():
        # Skip themes with very few posts
        total_theme_posts = sum(len(sub['posts']) for sub in theme_data['sub_themes'].values())
        if total_theme_posts < 2:
            continue
        
        # Calculate theme hub statistics
        total_score = sum(sub['total_score'] for sub in theme_data['sub_themes'].values())
        total_comments = sum(sub['total_comments'] for sub in theme_data['sub_themes'].values())
        avg_engagement = (total_score + (total_comments * 10)) / max(total_theme_posts, 1)
        avg_score = total_score / max(total_theme_posts, 1)
        
        # Get top sub-themes by engagement
        sub_themes_list = []
        for sub_name, sub_data in theme_data['sub_themes'].items():
            if len(sub_data['posts']) >= 1:  # At least 1 post
                sub_engagement = (sub_data['total_score'] + (sub_data['total_comments'] * 10)) / len(sub_data['posts'])
                sub_themes_list.append({
                    'name': sub_name,
                    'post_count': len(sub_data['posts']),
                    'avg_engagement': sub_engagement,
                    'avg_score': sub_data['total_score'] / len(sub_data['posts']),
                    'problems_solved': list(set(sub_data['problems_solved'])),  # Remove duplicates
                    'sample_titles': sub_data['sample_titles'],
                    'post_data': sub_data['post_data']  # Include post data
                })
        
        if len(sub_themes_list) == 0:
            continue
        
        sub_themes_list.sort(key=lambda x: x['avg_engagement'], reverse=True)
        
        # Create main theme hub node
        theme_hub = {
            'id': f"hub-{theme_name.lower().replace('/', '-').replace(' ', '-')}",
            'name': theme_name,
            'val': min(total_theme_posts, 15),  # Hub size based on total posts (capped)
            'color': theme_colors.get(theme_name, '#ddd'),
            'group': 100,  # Special group for hubs
            'category': 'hub',
            'node_type': 'category_hub',
            
            # Hub metadata
            'total_posts': total_theme_posts,
            'avg_engagement': round(avg_engagement, 1),
            'avg_score': round(avg_score, 1),
            'sub_themes_count': len(sub_themes_list),
            'top_sub_themes': sub_themes_list[:3]
        }
        
        nodes.append(theme_hub)
        
        # Create sub-theme nodes connected to this hub
        for sub_theme in sub_themes_list:
            # Skip very low engagement sub-themes to reduce clutter
            if sub_theme['avg_engagement'] < 30:
                continue
                
            sub_theme_node = {
                'id': f"{theme_name.lower().replace('/', '-').replace(' ', '-')}-{sub_theme['name'].lower().replace('/', '-').replace(' ', '-')}",
                'name': f"{theme_name}: {sub_theme['name']}",
                'val': min(sub_theme['post_count'] * 2, 8),  # Smaller than hubs
                'color': adjust_color_brightness(theme_colors.get(theme_name, '#ddd'), 0.7),
                'group': get_group_by_theme(theme_name),
                'category': theme_name,
                'node_type': 'sub_theme',
                
                # Sub-theme metadata
                'sub_theme': sub_theme['name'],
                'post_count': sub_theme['post_count'],
                'avg_engagement': sub_theme['avg_engagement'],
                'avg_score': sub_theme['avg_score'],
                'problems_solved': sub_theme['problems_solved'],
                'sample_titles': sub_theme['sample_titles'],
                'posts': sub_theme['post_data'],  # Include full post data for Reddit links
                'parent_hub': theme_hub['id']
            }
            
            nodes.append(sub_theme_node)
            
            # Create link from hub to sub-theme
            link_strength = min(sub_theme['avg_engagement'] / 200, 1.0)  # Normalize to 0-1
            
            links.append({
                'source': theme_hub['id'],
                'target': sub_theme_node['id'],
                'value': round(link_strength, 2),
                'relationship': 'theme_contains'
            })
    
    # Create cross-theme links for related sub-themes
    sub_theme_nodes = [n for n in nodes if n.get('node_type') == 'sub_theme']
    
    # Link high-engagement sub-themes across different main themes
    high_engagement_subs = [n for n in sub_theme_nodes if n.get('avg_engagement', 0) > 100]
    
    for i, node1 in enumerate(high_engagement_subs):
        for node2 in high_engagement_subs[i+1:i+3]:  # Link to next 2 high-engagement nodes
            if node1['category'] != node2['category']:
                links.append({
                    'source': node1['id'],
                    'target': node2['id'],
                    'value': 0.3,
                    'relationship': 'cross_theme_opportunity'
                })
    
    # Create inter-hub connections for related themes
    hub_connections = [
        ('AI/ML Tools', 'Web Development', 0.6),
        ('Web Development', 'Mobile Apps', 0.5),
        ('Browser Extensions', 'Web Development', 0.7),
        ('Games', 'Mobile Apps', 0.4),
        ('AI/ML Tools', 'Developer Tools', 0.5),
        ('Finance', 'Business Tools', 0.6),
        ('Productivity', 'Business Tools', 0.5),
        ('Data/Analytics', 'AI/ML Tools', 0.7)
    ]
    
    hub_lookup = {node['name']: node['id'] for node in nodes if node.get('node_type') == 'category_hub'}
    
    for theme1, theme2, strength in hub_connections:
        if theme1 in hub_lookup and theme2 in hub_lookup:
            links.append({
                'source': hub_lookup[theme1],
                'target': hub_lookup[theme2],
                'value': strength,
                'relationship': 'related_themes'
            })
    
    print(f"Created hierarchical structure:")
    print(f"Theme hubs: {len([n for n in nodes if n.get('node_type') == 'category_hub'])}")
    print(f"Sub-themes: {len([n for n in nodes if n.get('node_type') == 'sub_theme'])}")
    print(f"Total links: {len(links)}")
    
    return {
        'nodes': nodes,
        'links': links,
        'metadata': {
            'structure': 'hierarchical',
            'hub_count': len([n for n in nodes if n.get('node_type') == 'category_hub']),
            'sub_count': len([n for n in nodes if n.get('node_type') == 'sub_theme']),
            'total_posts_analyzed': len(trend_data)
        }
    }

def adjust_color_brightness(hex_color, factor):
    """Adjust color brightness (factor < 1 = darker, > 1 = lighter)"""
    if not hex_color or hex_color == '#ddd':
        return '#999'
    
    hex_color = hex_color.lstrip('#')
    
    if len(hex_color) != 6:
        return '#999'
    
    try:
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        rgb = tuple(min(255, max(0, int(c * factor))) for c in rgb)
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
    except ValueError:
        return '#999'

def get_group_by_theme(theme):
    """Assign group numbers by main theme"""
    groups = {
        'Finance': 1, 'Productivity': 2, 'AI/ML Tools': 3,
        'Web Development': 4, 'Mobile Apps': 5, 'Browser Extensions': 6,
        'Games': 7, 'Health & Fitness': 8, 'Education': 9,
        'Social/Communication': 10, 'E-commerce': 11, 'Data/Analytics': 12,
        'Content Creation': 13, 'Automation': 14, 'Security/Privacy': 15,
        'Entertainment': 16, 'Lifestyle': 17, 'Business Tools': 18,
        'Developer Tools': 19, 'Other': 20
    }
    return groups.get(theme, 21)

def save_hierarchical_data():
    """Generate and save hierarchical graph data"""
    graph_data = create_hierarchical_graph_data()
    
    # Save as JavaScript file
    output_file = os.path.join(Config.OUTPUT_DIR, 'hierarchical_graph_data.js')
    
    js_content = f"""// hierarchical_graph_data.js - Trend Analysis Hierarchical Graph
export const hierarchicalGraphData = {json.dumps(graph_data, indent=2)};"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print(f"Saved hierarchical data to: {output_file}")
    
    # Show top theme hubs
    hubs = [n for n in graph_data['nodes'] if n.get('node_type') == 'category_hub']
    hubs = sorted(hubs, key=lambda x: x['avg_engagement'], reverse=True)
    
    print(f"\nTop Theme Hubs by Engagement:")
    for hub in hubs[:5]:
        print(f"   • {hub['name']}: {hub['total_posts']} posts, {hub['avg_engagement']:.1f} avg engagement")
    
    return graph_data

if __name__ == "__main__":
    print("Creating Hierarchical Graph Structure from Trend Analysis")
    print("="*60)
    save_hierarchical_data()