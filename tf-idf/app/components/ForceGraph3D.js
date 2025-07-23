// components/ForceGraph3D.js
'use client';

import { useEffect, useRef, useState } from 'react';
import dynamic from 'next/dynamic';
import SpriteText from 'three-spritetext';
import {sampleGraphData} from '../data/sampleData';

// Dynamically import to avoid SSR issues
const ForceGraph3D = dynamic(() => import('react-force-graph-3d'), {
  ssr: false,
  loading: () => <div>Loading 3D Graph...</div>
});

const MyForceGraph = () => {
  const fgRef = useRef();
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });

  useEffect(() => {
    // Sample Data for now, TODO: Get scrapped data, format for nodes and links

    setGraphData(sampleGraphData);
  }, []);

  return (
    <div style={{ width: '100%', height: '600px' }}>
      <ForceGraph3D
        ref={fgRef}
        graphData={graphData}
        
        // Node styling
        nodeLabel="name"
        nodeVal="val"
        nodeColor="color"
        // nodeOpacity={0.8}
        
        // 3D Text nodes with spheres
        nodeThreeObjectExtend={true} 
        nodeThreeObject={(node) => {
          const sprite = new SpriteText(node.name);
          sprite.color = node.color;
          sprite.textHeight = 8;
          sprite.center.y = -0.6; // shift above node
          return sprite;
        }}
        
        // Link styling
        linkColor={() => '#000000'}
        // linkOpacity={0.6}
        linkWidth={0.5}
        
        // Background
        backgroundColor="#e6e6e6"
        
        // Interaction handlers
        onNodeClick={(node) => {
          console.log('Clicked node:', node);
        }}
        
        onNodeHover={(node) => {
          document.body.style.cursor = node ? 'pointer' : 'default';
        }}
        
        // Camera controls
        controlType="trackball"
        enableNavigationControls={true}
      />
    </div>
  );
};

export default MyForceGraph;