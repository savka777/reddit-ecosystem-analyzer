'use client';

import { useEffect, useRef, useState, useCallback, useMemo } from 'react';
import dynamic from 'next/dynamic';
import SpriteText from 'three-spritetext';
import { hierarchicalGraphData } from '../data/hierarchical_graph_data.js';

// Dynamically import to avoid SSR issues
const ForceGraph3D = dynamic(() => import('react-force-graph-3d'), {
  ssr: false,
  loading: () => <div>Loading 3D Graph...</div>
});

const MyForceGraph = ({ onNodeClick }) => {
  const fgRef = useRef();
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });

  // Memoize graph data to prevent unnecessary re-renders
  const memoizedGraphData = useMemo(() => {
    return hierarchicalGraphData;
  }, []);

  useEffect(() => {
    if (fgRef.current) {
      fgRef.current.d3Force('charge').strength(-250);
      fgRef.current.d3Force('link').distance(50);
      fgRef.current.d3Force('center').strength(0.05);
      fgRef.current.numDimensions(3);
    }
    setGraphData(memoizedGraphData);
  }, [memoizedGraphData]);

  // Memoized click handler
  const handleNodeClick = useCallback((node) => {
    console.log('Clicked node:', node);
    if (onNodeClick) {
      onNodeClick(node);
    }
  }, [onNodeClick]);

  // Memoized hover handler with simple tooltip
  const handleNodeHover = useCallback((node, prevNode) => {
    document.body.style.cursor = node ? 'pointer' : 'default';
  }, []);

  // Simple tooltip function
  const getNodeTooltip = useCallback((node) => {
    if (node.node_type === 'category_hub') {
      return `${node.name} - ${node.total_posts} projects`;
    } else if (node.node_type === 'sub_theme') {
      return `${node.sub_theme} - ${node.post_count} projects (Click for details)`;
    }
    return node.name;
  }, []);

  // Memoized color functions
  const getLinkColor = useCallback((link) => {
    switch(link.relationship) {
      case 'theme_contains': return '#333333';
      case 'related_themes': return '#666666';
      case 'cross_theme_opportunity': return '#ff9999';
      default: return '#000000';
    }
  }, []);

  const getLinkWidth = useCallback((link) => {
    switch(link.relationship) {
      case 'theme_contains': return 2;
      case 'related_themes': return 1;
      default: return 0.5;
    }
  }, []);

  // Optimized 3D text object creation - only for main theme hubs
  const createNodeObject = useCallback((node) => {
    // Only show text labels for main theme hubs
    if (node.node_type === 'category_hub') {
      const sprite = new SpriteText(node.name);
      sprite.color = node.color;
      sprite.textHeight = 8;
      sprite.fontWeight = 'bold';
      sprite.center.y = -0.8; // Position text above the node
      sprite.backgroundColor = 'rgba(0,0,0,0.15)'; // Slightly darker background for main themes
      sprite.padding = 3;
      sprite.borderRadius = 4;
      return sprite;
    }
    
    // Return null for sub-themes - no text label
    return null;
  }, []);

  return (
    <div style={{ width: '100%', height: '100vh' }}>
      <ForceGraph3D
        ref={fgRef}
        graphData={graphData}
        
        // Simple tooltip on hover
        nodeLabel={getNodeTooltip}
        
        // Basic node styling
        nodeVal="val"
        nodeColor="color"
        nodeOpacity={0.8}
        
        // 3D text labels above nodes (optimized)
        nodeThreeObject={createNodeObject}
        nodeThreeObjectExtend={true}
        
        // Link styling (memoized functions)
        linkColor={getLinkColor}
        linkWidth={getLinkWidth}
        linkOpacity={0.5}
        
        // Background
        backgroundColor="#f8f9fa"
        
        // Interaction handlers (memoized)
        onNodeClick={handleNodeClick}
        onNodeHover={handleNodeHover}
        
        // Balanced performance settings
        enableNodeDrag={true} // Re-enabled dragging for interactivity
        enableNavigationControls={true}
        controlType="orbit" // Keep orbit for better performance
        
        // Moderate rendering quality
        rendererConfig={{
          antialias: true,  // Re-enabled for better text quality
          alpha: true,      // Re-enabled for transparency
          powerPreference: "high-performance"
        }}
        
        // Show some UI elements
        showNavInfo={false}
        
        // Warmup period to let forces settle
        cooldownTime={5000}
        cooldownTicks={100}
      />
    </div>
  );
};

export default MyForceGraph;