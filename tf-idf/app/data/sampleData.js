// sampleData.js - Large sample dataset for ForceGraph3D
export const sampleGraphData = {
  nodes: [
    // Technology Hub
    { id: 'tech_hub', name: 'Technology Hub', val: 8, color: '#ff6b6b', group: 1, category: 'central' },
    { id: 'ai_research', name: 'AI Research', val: 6, color: '#4ecdc4', group: 2, category: 'tech' },
    { id: 'machine_learning', name: 'Machine Learning', val: 5, color: '#45b7d1', group: 2, category: 'tech' },
    { id: 'data_science', name: 'Data Science', val: 5, color: '#96ceb4', group: 2, category: 'tech' },
    { id: 'web_dev', name: 'Web Development', val: 4, color: '#ffeaa7', group: 2, category: 'tech' },
    
    // Business Sector
    { id: 'business_hub', name: 'Business Hub', val: 7, color: '#fd79a8', group: 3, category: 'central' },
    { id: 'startups', name: 'Startups', val: 4, color: '#fdcb6e', group: 4, category: 'business' },
    { id: 'venture_capital', name: 'Venture Capital', val: 5, color: '#e17055', group: 4, category: 'business' },
    { id: 'marketing', name: 'Marketing', val: 3, color: '#a29bfe', group: 4, category: 'business' },
    { id: 'sales', name: 'Sales', val: 3, color: '#fd79a8', group: 4, category: 'business' },
    
    // Education Network
    { id: 'education_hub', name: 'Education Hub', val: 6, color: '#00b894', group: 5, category: 'central' },
    { id: 'universities', name: 'Universities', val: 4, color: '#00cec9', group: 6, category: 'education' },
    { id: 'online_courses', name: 'Online Courses', val: 3, color: '#55a3ff', group: 6, category: 'education' },
    { id: 'research_papers', name: 'Research Papers', val: 2, color: '#a29bfe', group: 6, category: 'education' },
    { id: 'certifications', name: 'Certifications', val: 2, color: '#fd79a8', group: 6, category: 'education' },
    
    // Innovation Cluster
    { id: 'innovation_lab', name: 'Innovation Lab', val: 5, color: '#e84393', group: 7, category: 'innovation' },
    { id: 'blockchain', name: 'Blockchain', val: 4, color: '#0984e3', group: 7, category: 'innovation' },
    { id: 'iot_devices', name: 'IoT Devices', val: 3, color: '#00b894', group: 7, category: 'innovation' },
    { id: 'robotics', name: 'Robotics', val: 4, color: '#e17055', group: 7, category: 'innovation' },
    { id: 'quantum_computing', name: 'Quantum Computing', val: 3, color: '#6c5ce7', group: 7, category: 'innovation' },
    
    // Community & Social
    { id: 'community_hub', name: 'Community Hub', val: 5, color: '#fab1a0', group: 8, category: 'social' },
    { id: 'social_media', name: 'Social Media', val: 4, color: '#ff7675', group: 8, category: 'social' },
    { id: 'forums', name: 'Forums', val: 2, color: '#fdcb6e', group: 8, category: 'social' },
    { id: 'networking_events', name: 'Networking Events', val: 3, color: '#e17055', group: 8, category: 'social' },
    { id: 'conferences', name: 'Conferences', val: 3, color: '#a29bfe', group: 8, category: 'social' }
  ],
  
  links: [
    // Technology Hub connections
    { source: 'tech_hub', target: 'ai_research', value: 0.9, relationship: 'primary' },
    { source: 'tech_hub', target: 'machine_learning', value: 0.8, relationship: 'primary' },
    { source: 'tech_hub', target: 'data_science', value: 0.7, relationship: 'primary' },
    { source: 'tech_hub', target: 'web_dev', value: 0.6, relationship: 'secondary' },
    
    // AI Research sub-network
    { source: 'ai_research', target: 'machine_learning', value: 0.9, relationship: 'closely_related' },
    { source: 'ai_research', target: 'data_science', value: 0.8, relationship: 'closely_related' },
    { source: 'ai_research', target: 'quantum_computing', value: 0.6, relationship: 'emerging' },
    { source: 'machine_learning', target: 'data_science', value: 0.9, relationship: 'closely_related' },
    
    // Business Hub connections
    { source: 'business_hub', target: 'startups', value: 0.8, relationship: 'primary' },
    { source: 'business_hub', target: 'venture_capital', value: 0.9, relationship: 'primary' },
    { source: 'business_hub', target: 'marketing', value: 0.7, relationship: 'secondary' },
    { source: 'business_hub', target: 'sales', value: 0.7, relationship: 'secondary' },
    
    // Business sub-network
    { source: 'startups', target: 'venture_capital', value: 0.9, relationship: 'funding' },
    { source: 'startups', target: 'marketing', value: 0.6, relationship: 'growth' },
    { source: 'marketing', target: 'sales', value: 0.8, relationship: 'workflow' },
    { source: 'venture_capital', target: 'innovation_lab', value: 0.5, relationship: 'investment' },
    
    // Education Hub connections
    { source: 'education_hub', target: 'universities', value: 0.9, relationship: 'institutional' },
    { source: 'education_hub', target: 'online_courses', value: 0.7, relationship: 'modern' },
    { source: 'education_hub', target: 'research_papers', value: 0.8, relationship: 'academic' },
    { source: 'education_hub', target: 'certifications', value: 0.6, relationship: 'professional' },
    
    // Education sub-network
    { source: 'universities', target: 'research_papers', value: 0.9, relationship: 'research' },
    { source: 'universities', target: 'ai_research', value: 0.7, relationship: 'collaboration' },
    { source: 'online_courses', target: 'certifications', value: 0.8, relationship: 'pathway' },
    { source: 'research_papers', target: 'ai_research', value: 0.6, relationship: 'knowledge' },
    
    // Innovation Lab connections
    { source: 'innovation_lab', target: 'blockchain', value: 0.8, relationship: 'development' },
    { source: 'innovation_lab', target: 'iot_devices', value: 0.7, relationship: 'development' },
    { source: 'innovation_lab', target: 'robotics', value: 0.8, relationship: 'development' },
    { source: 'innovation_lab', target: 'quantum_computing', value: 0.6, relationship: 'research' },
    
    // Innovation sub-network
    { source: 'blockchain', target: 'startups', value: 0.5, relationship: 'application' },
    { source: 'iot_devices', target: 'data_science', value: 0.6, relationship: 'data_source' },
    { source: 'robotics', target: 'ai_research', value: 0.7, relationship: 'integration' },
    { source: 'quantum_computing', target: 'universities', value: 0.5, relationship: 'research' },
    
    // Community Hub connections
    { source: 'community_hub', target: 'social_media', value: 0.9, relationship: 'platform' },
    { source: 'community_hub', target: 'forums', value: 0.7, relationship: 'discussion' },
    { source: 'community_hub', target: 'networking_events', value: 0.8, relationship: 'events' },
    { source: 'community_hub', target: 'conferences', value: 0.8, relationship: 'events' },
    
    // Community sub-network
    { source: 'networking_events', target: 'conferences', value: 0.7, relationship: 'similar' },
    { source: 'conferences', target: 'universities', value: 0.6, relationship: 'academic' },
    { source: 'social_media', target: 'marketing', value: 0.8, relationship: 'channel' },
    { source: 'forums', target: 'online_courses', value: 0.5, relationship: 'learning' },
    
    // Cross-hub connections
    { source: 'tech_hub', target: 'business_hub', value: 0.6, relationship: 'collaboration' },
    { source: 'tech_hub', target: 'education_hub', value: 0.7, relationship: 'knowledge_transfer' },
    { source: 'tech_hub', target: 'innovation_lab', value: 0.8, relationship: 'development' },
    { source: 'business_hub', target: 'community_hub', value: 0.5, relationship: 'networking' },
    { source: 'education_hub', target: 'innovation_lab', value: 0.6, relationship: 'research' },
    { source: 'innovation_lab', target: 'community_hub', value: 0.4, relationship: 'outreach' },
    
    // Additional cross-connections for network density
    { source: 'web_dev', target: 'startups', value: 0.7, relationship: 'skill_demand' },
    { source: 'data_science', target: 'venture_capital', value: 0.4, relationship: 'analytics' },
    { source: 'certifications', target: 'startups', value: 0.5, relationship: 'hiring' },
    { source: 'blockchain', target: 'conferences', value: 0.3, relationship: 'presentation' },
    { source: 'robotics', target: 'venture_capital', value: 0.4, relationship: 'funding' }
  ]
};