'use client';

import React, { useState, useMemo } from 'react';
import { ChevronDown, ChevronRight, Circle, Layers, Target } from 'lucide-react';

const ThemeNavigator = ({ graphData, onSubThemeClick }) => {
  const [expandedThemes, setExpandedThemes] = useState({});

  // Process graph data to create theme hierarchy
  const themeHierarchy = useMemo(() => {
    if (!graphData || !graphData.nodes) return {};

    const hierarchy = {};

    // Get all main theme hubs
    const mainThemes = graphData.nodes.filter(node => node.node_type === 'category_hub');
    
    // Get all sub-themes
    const subThemes = graphData.nodes.filter(node => node.node_type === 'sub_theme');

    // Organize sub-themes under their parent themes
    mainThemes.forEach(theme => {
      const relatedSubThemes = subThemes.filter(sub => sub.parent_hub === theme.id);
      
      hierarchy[theme.name] = {
        ...theme,
        subThemes: relatedSubThemes.sort((a, b) => b.avg_engagement - a.avg_engagement) // Sort by engagement
      };
    });

    return hierarchy;
  }, [graphData]);

  const toggleTheme = (themeName) => {
    setExpandedThemes(prev => ({
      ...prev,
      [themeName]: !prev[themeName]
    }));
  };

  const handleSubThemeClick = (subTheme) => {
    if (onSubThemeClick) {
      onSubThemeClick(subTheme);
    }
  };

  const getEngagementColor = (engagement) => {
    if (engagement >= 300) return 'text-red-600';
    if (engagement >= 200) return 'text-orange-600';
    if (engagement >= 150) return 'text-yellow-600';
    if (engagement >= 100) return 'text-green-600';
    return 'text-gray-500';
  };

  const sortedThemes = Object.entries(themeHierarchy).sort(([,a], [,b]) => 
    b.avg_engagement - a.avg_engagement
  );

  return (
    <div className="fixed right-4 top-4 bottom-4 w-80 bg-white shadow-2xl rounded-lg border border-gray-200 overflow-hidden z-40 flex flex-col">
      <div className="bg-white text-gray-800 p-4 border-b border-gray-200 flex-shrink-0">
        <div className="flex items-center space-x-2">
          <Layers size={18} className="text-blue-600" />
          <h3 className="text-sm font-semibold">Theme Explorer</h3>
        </div>
        <p className="text-gray-600 text-xs mt-1">Click themes to explore, sub-themes for details</p>
      </div>

      <div className="overflow-y-auto flex-1 theme-navigator">
        {sortedThemes.map(([themeName, themeData]) => (
          <div key={themeName} className="border-b border-gray-100 last:border-b-0">
            <button
              onClick={() => toggleTheme(themeName)}
              className="w-full px-4 py-3 flex items-center justify-between hover:bg-gray-50 transition-colors text-left"
            >
              <div className="flex items-center space-x-3">
                <div className="flex items-center space-x-2">
                  {expandedThemes[themeName] ? 
                    <ChevronDown size={16} className="text-gray-600" /> : 
                    <ChevronRight size={16} className="text-gray-600" />
                  }
                  <div 
                    className="w-3 h-3 rounded-full border border-gray-300"
                    style={{ backgroundColor: themeData.color }}
                  />
                </div>
                <div>
                  <p className="font-medium text-gray-800 text-sm">{themeName}</p>
                  <p className="text-xs text-gray-500">
                    {themeData.total_posts} projects • {Math.round(themeData.avg_engagement)} avg engagement
                  </p>
                </div>
              </div>
              
              <div className="text-right">
                <span className={`text-xs font-medium ${getEngagementColor(themeData.avg_engagement)}`}>
                  {Math.round(themeData.avg_engagement)}
                </span>
                <p className="text-xs text-gray-400">{themeData.subThemes.length} sub-themes</p>
              </div>
            </button>

            {expandedThemes[themeName] && (
              <div className="bg-blue-50 border-t border-gray-100">
                {themeData.subThemes.length > 0 ? (
                  themeData.subThemes.map((subTheme) => (
                    <button
                      key={subTheme.id}
                      onClick={() => handleSubThemeClick(subTheme)}
                      className="w-full px-6 py-2 flex items-center justify-between hover:bg-blue-100 transition-colors text-left group"
                    >
                      <div className="flex items-center space-x-3">
                        <Target size={12} className="text-gray-500 group-hover:text-blue-600" />
                        <div>
                          <p className="text-sm text-gray-700 group-hover:text-blue-800 font-medium">
                            {subTheme.sub_theme}
                          </p>
                          <p className="text-xs text-gray-500">
                            {subTheme.post_count} projects
                          </p>
                        </div>
                      </div>
                      
                      <div className="text-right">
                        <span className={`text-xs font-medium ${getEngagementColor(subTheme.avg_engagement)}`}>
                          {Math.round(subTheme.avg_engagement)}
                        </span>
                        <p className="text-xs text-gray-400">Click for details</p>
                      </div>
                    </button>
                  ))
                ) : (
                  <div className="px-6 py-3 text-xs text-gray-500 italic">
                    No sub-themes available
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="bg-gray-50 px-4 py-2 border-t border-gray-200 flex-shrink-0">
        <div className="flex justify-between text-xs text-gray-600">
          <span>{sortedThemes.length} main themes</span>
          <span>{sortedThemes.reduce((acc, [,theme]) => acc + theme.subThemes.length, 0)} sub-themes</span>
        </div>
      </div>
    </div>
  );
};

export default ThemeNavigator;