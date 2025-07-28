'use client';

import React from 'react';
import { X, Target, TrendingUp, Users, MessageSquare, ExternalLink } from 'lucide-react';

const ProblemsPanel = ({ isOpen, onClose, selectedNode }) => {
  if (!selectedNode) return null;

  const { sub_theme, category, problems_solved, post_count, avg_engagement, sample_titles, posts } = selectedNode;

  return (
    <div 
      className={`fixed left-0 top-0 h-full bg-white shadow-2xl z-50 transition-transform duration-300 ease-in-out border-r border-gray-200 flex flex-col ${
        isOpen ? 'translate-x-0' : '-translate-x-full'
      }`}
      style={{ width: '350px' }}
    >
      <div className="bg-white text-gray-800 p-4 border-b border-gray-200">
        <div className="flex justify-between items-start">
          <div>
            <h2 className="text-lg font-bold text-gray-800">{sub_theme}</h2>
            <p className="text-gray-600 text-sm">{category}</p>
          </div>
          <button 
            onClick={onClose}
            className="text-gray-600 hover:text-gray-800 transition-colors"
          >
            <X size={24} />
          </button>
        </div>
        
        <div className="grid grid-cols-2 gap-4 mt-4">
          <div className="bg-gray-50 rounded-lg p-2 border border-gray-200">
            <div className="flex items-center space-x-2">
              <Users size={16} className="text-blue-600" />
              <span className="text-sm text-gray-800">{post_count} Posts</span>
            </div>
          </div>
          <div className="bg-gray-50 rounded-lg p-2 border border-gray-200">
            <div className="flex items-center space-x-2">
              <TrendingUp size={16} className="text-blue-600" />
              <span className="text-sm text-gray-800">{Math.round(avg_engagement)} Engagement</span>
            </div>
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto problems-panel-content">
        <div className="p-4">
          <div className="mb-6">
            <div className="flex items-center space-x-2 mb-3">
              <Target className="text-blue-600" size={20} />
              <h3 className="text-lg font-semibold text-gray-800">Problems Solved</h3>
            </div>
            
            {problems_solved && problems_solved.length > 0 ? (
              <div className="space-y-3">
                {problems_solved.map((problem, index) => (
                  <div key={index} className="bg-blue-50 border-l-4 border-blue-500 p-3 rounded-r-lg border border-blue-200">
                    <p className="text-gray-700 text-sm leading-relaxed">{problem}</p>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500 italic">No specific problems identified for this theme.</p>
            )}
          </div>
          {sample_titles && sample_titles.length > 0 && (
            <div className="mb-6">
              <div className="flex items-center space-x-2 mb-3">
                <MessageSquare className="text-green-600" size={20} />
                <h3 className="text-lg font-semibold text-gray-800">Example Projects</h3>
              </div>
              
              <div className="space-y-2">
                {sample_titles.slice(0, 5).map((title, index) => (
                  <div key={index} className="bg-green-50 border border-green-200 rounded-lg p-3">
                    <p className="text-gray-700 text-sm font-medium">{title}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
          {posts && posts.length > 0 && (
            <div className="mb-6">
              <div className="flex items-center space-x-2 mb-3">
                <ExternalLink className="text-orange-600" size={20} />
                <h3 className="text-lg font-semibold text-gray-800">Reddit Sources</h3>
              </div>
              
              <div className="space-y-2">
                {posts.slice(0, 6).map((post, index) => {
                  let redditUrl = '#';
                  if (post.permalink && post.permalink.startsWith('https://reddit.com')) {
                    redditUrl = post.permalink;
                  } else if (post.permalink && post.permalink.startsWith('/r/')) {
                    redditUrl = `https://reddit.com${post.permalink}`;
                  } else if (post.url && post.url.includes('reddit.com/r/')) {
                    redditUrl = post.url;
                  }
                  
                  return (
                    <div key={index} className="bg-orange-50 border border-orange-200 rounded-lg p-3">
                      <div className="flex items-start justify-between space-x-3">
                        <div className="flex-1">
                          <p className="text-gray-700 text-sm font-medium line-clamp-2 mb-1">
                            {post.title}
                          </p>
                          <div className="flex items-center space-x-3 text-xs text-gray-500">
                            <span>r/{post.subreddit || 'SideProject'}</span>
                            <span>•</span>
                            <span>{post.score} upvotes</span>
                            <span>•</span>
                            <span>{post.num_comments} comments</span>
                          </div>
                        </div>
                        <a
                          href={redditUrl}
                          target="_blank"
                          rel="noopener noreferrer"
                          className={`flex-shrink-0 transition-colors ${
                            redditUrl === '#' 
                              ? 'text-gray-400 cursor-not-allowed' 
                              : 'text-orange-600 hover:text-orange-800'
                          }`}
                          title={redditUrl === '#' ? 'No link available' : 'View on Reddit'}
                        >
                          <ExternalLink size={16} />
                        </a>
                      </div>
                    </div>
                  );
                })}
              </div>
              
              {posts.length > 6 && (
                <p className="text-xs text-gray-500 italic mt-2">
                  Showing 6 of {posts.length} related posts
                </p>
              )}
            </div>
          )}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h3 className="text-lg font-semibold text-gray-800 mb-2">💡 Insights</h3>
            <ul className="text-sm text-gray-600 space-y-1">
              <li>• This sub-theme appears in <strong className="text-gray-800">{post_count}</strong> projects</li>
              <li>• Average engagement: <strong className="text-gray-800">{Math.round(avg_engagement)}</strong> points</li>
              <li>• <strong className="text-gray-800">{problems_solved?.length || 0}</strong> unique problems identified</li>
              <li>• Part of the <strong className="text-gray-800">{category}</strong> ecosystem</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProblemsPanel;