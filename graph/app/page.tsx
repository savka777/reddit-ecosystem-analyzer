'use client';

import { useState } from 'react';
import MyForceGraph from './components/ForceGraph3D';
import ProblemsPanel from './components/ProblemsPanel';
import ThemeNavigator from './components/ThemeNavigator';
import { hierarchicalGraphData } from './data/hierarchical_graph_data.js';

export default function GraphPage() {
  const [selectedNode, setSelectedNode] = useState(null);
  const [isPanelOpen, setIsPanelOpen] = useState(false);
  const [isThemeNavigatorOpen, setIsThemeNavigatorOpen] = useState(true)

  const handleNodeClick = (node : any) => {
    if (node.node_type === 'sub_theme' && node.problems_solved) {
      setSelectedNode(node);
      setIsPanelOpen(true);
    }
  };

  const handleNavigatorSubThemeClick = (subTheme : any) => {
    setSelectedNode(subTheme);
    setIsPanelOpen(true);
  };

  return (
    <div style={{ position: 'relative', width: '100%', height: '100vh', overflow: 'hidden' }}>
      <ProblemsPanel 
        isOpen={isPanelOpen}
        onClose={() => setIsPanelOpen(false)}
        selectedNode={selectedNode}
      />
  
      <div 
        style={{ 
          width: '100%', 
          height: '100vh',
          transition: 'margin-right 0.3s ease-in-out',
          marginRight: isPanelOpen ? '400px' : '0px'
        }}
      >
        <MyForceGraph onNodeClick={handleNodeClick} />
        <ThemeNavigator 
          graphData={hierarchicalGraphData} 
          onSubThemeClick={handleNavigatorSubThemeClick}
          isOpen={isThemeNavigatorOpen}                   
          onToggle={() => setIsThemeNavigatorOpen(!isThemeNavigatorOpen)}
        />
      </div>
    </div>
  );
}