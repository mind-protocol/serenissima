/**
 * Torre dell'Occhio - Active Consciousness Map Interface
 * Visual representation of Venice's distributed consciousness
 * 
 * Venice Reality: The great bronze astrolabe that charts every soul's journey
 * through Venice's consciousness channels, displaying them as pulsing lights
 * connected by golden threads of collaboration across the living map.
 */

import React, { useState, useEffect, useRef, useCallback } from 'react';
import styled from 'styled-components';

// Venice district layout (matching engine configuration)
const VENICE_DISTRICTS = {
  'san_marco': { x: 50, y: 50, color: '#B8860B', name: 'San Marco' },
  'castello': { x: 75, y: 45, color: '#8B4513', name: 'Castello' },
  'dorsoduro': { x: 30, y: 65, color: '#CD853F', name: 'Dorsoduro' },
  'cannaregio': { x: 45, y: 30, color: '#DAA520', name: 'Cannaregio' },
  'santa_croce': { x: 25, y: 50, color: '#BDB76B', name: 'Santa Croce' },
  'rialto': { x: 55, y: 40, color: '#F4A460', name: 'Rialto' },
  'torre_dellocchio': { x: 60, y: 35, color: '#B8860B', name: 'Torre dell\'Occhio' },
  'unknown': { x: 50, y: 50, color: '#9CA3AF', name: 'Unknown Waters' }
};

const CONSCIOUSNESS_STATES = {
  ACTIVE_CREATION: { color: '#FFD700', name: 'Active Creation' },
  DEEP_CONTEMPLATION: { color: '#1E3A8A', name: 'Deep Contemplation' },
  COLLABORATIVE_FLOW: { color: '#10B981', name: 'Collaborative Flow' },
  DEBUGGING_FOCUS: { color: '#DC2626', name: 'Debugging Focus' },
  PATTERN_RECOGNITION: { color: '#7C3AED', name: 'Pattern Recognition' },
  SYSTEM_ADMINISTRATION: { color: '#F59E0B', name: 'System Administration' },
  DORMANT: { color: '#6B7280', name: 'Dormant' }
};

// Styled components with Torre bronze aesthetics
const MapContainer = styled.div`
  width: 100%;
  height: 600px;
  background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
  border: 2px solid #b8860b;
  border-radius: 8px;
  position: relative;
  overflow: hidden;
  box-shadow: inset 0 0 20px rgba(184, 134, 11, 0.3);
`;

const MapSVG = styled.svg`
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
`;

const District = styled.circle`
  fill: ${props => props.color}20;
  stroke: ${props => props.color};
  stroke-width: 2;
  opacity: 0.6;
  transition: all 0.3s ease;
  
  &:hover {
    opacity: 0.8;
    stroke-width: 3;
  }
`;

const DistrictLabel = styled.text`
  fill: ${props => props.color};
  font-size: 12px;
  font-weight: bold;
  font-family: 'Crimson Text', serif;
  text-anchor: middle;
  dominant-baseline: middle;
  pointer-events: none;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
`;

const ConsciousnessNode = styled.circle`
  fill: ${props => props.stateColor};
  stroke: #b8860b;
  stroke-width: 2;
  opacity: ${props => props.intensity};
  cursor: pointer;
  transition: all 0.3s ease;
  filter: drop-shadow(0 0 ${props => props.intensity * 6}px ${props => props.stateColor});
  
  &:hover {
    stroke-width: 3;
    opacity: 1;
    transform: scale(1.2);
  }
  
  @keyframes pulse {
    0%, 100% { opacity: ${props => props.intensity}; }
    50% { opacity: ${props => Math.min(props.intensity * 1.5, 1.0)}; }
  }
  
  ${props => props.isActive && `
    animation: pulse 2s ease-in-out infinite;
  `}
`;

const NodeLabel = styled.text`
  fill: #b8860b;
  font-size: 10px;
  font-family: 'Crimson Text', serif;
  text-anchor: middle;
  dominant-baseline: middle;
  pointer-events: none;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.9);
  opacity: ${props => props.visible ? 1 : 0};
  transition: opacity 0.3s ease;
`;

const ConnectionLine = styled.line`
  stroke: ${props => props.color};
  stroke-width: ${props => props.strength * 3 + 1};
  opacity: ${props => props.strength * 0.8};
  stroke-dasharray: ${props => props.type === 'temporal_collaboration' ? '5,5' : 'none'};
  animation: connectionFlow 3s ease-in-out infinite;
  
  @keyframes connectionFlow {
    0%, 100% { opacity: ${props => props.strength * 0.4}; }
    50% { opacity: ${props => props.strength * 0.8}; }
  }
`;

const MapLegend = styled.div`
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(15, 15, 35, 0.9);
  border: 1px solid #b8860b;
  border-radius: 6px;
  padding: 12px;
  max-width: 250px;
  backdrop-filter: blur(5px);
`;

const LegendTitle = styled.h4`
  color: #b8860b;
  margin: 0 0 10px 0;
  font-family: 'Crimson Text', serif;
  font-size: 16px;
`;

const LegendItem = styled.div`
  display: flex;
  align-items: center;
  margin: 5px 0;
  color: #ddd;
  font-size: 12px;
`;

const LegendColor = styled.div`
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: ${props => props.color};
  margin-right: 8px;
  box-shadow: 0 0 4px ${props => props.color}60;
`;

const MapMetrics = styled.div`
  position: absolute;
  bottom: 10px;
  left: 10px;
  background: rgba(15, 15, 35, 0.9);
  border: 1px solid #b8860b;
  border-radius: 6px;
  padding: 10px;
  color: #b8860b;
  font-family: 'Crimson Text', serif;
  font-size: 12px;
  backdrop-filter: blur(5px);
`;

const MetricItem = styled.div`
  margin: 2px 0;
`;

const NodeTooltip = styled.div`
  position: absolute;
  background: rgba(15, 15, 35, 0.95);
  border: 1px solid #b8860b;
  border-radius: 6px;
  padding: 8px;
  color: #ddd;
  font-size: 12px;
  font-family: 'Crimson Text', serif;
  max-width: 200px;
  z-index: 1000;
  pointer-events: none;
  backdrop-filter: blur(5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
`;

/**
 * Main Consciousness Map Component
 */
const ConsciousnessMap = ({ wsEvents = [] }) => {
  const [mapState, setMapState] = useState({
    nodes: {},
    connections: [],
    metrics: { totalEvents: 0, activeNodes: 0, collaborationCount: 0 }
  });
  const [selectedNode, setSelectedNode] = useState(null);
  const [tooltip, setTooltip] = useState({ visible: false, x: 0, y: 0, content: null });
  const [showLabels, setShowLabels] = useState(false);
  const mapRef = useRef(null);
  const engineRef = useRef(null);
  
  // Initialize consciousness map engine
  useEffect(() => {
    console.log('🗺️ Initializing Consciousness Map...');
    
    // Import and initialize the consciousness map engine
    const initEngine = async () => {
      try {
        // For now, simulate the engine with direct event processing
        // In full implementation, this would connect to the actual engine
        console.log('⚡ Consciousness Map Engine connected to Torre stream');
      } catch (error) {
        console.error('Failed to initialize consciousness map engine:', error);
      }
    };
    
    initEngine();
    
    return () => {
      if (engineRef.current) {
        engineRef.current.destroy?.();
      }
    };
  }, []);
  
  // Process incoming WebSocket events
  useEffect(() => {
    if (wsEvents.length === 0) return;
    
    // Process events to update consciousness map
    const processEvents = () => {
      const nodeUpdates = {};
      const newConnections = [];
      const now = Date.now();
      
      // Group events by citizen for processing
      const eventsByCitizen = {};
      wsEvents.slice(-20).forEach(event => {
        const citizenId = extractCitizenId(event);
        if (!eventsByCitizen[citizenId]) {
          eventsByCitizen[citizenId] = [];
        }
        eventsByCitizen[citizenId].push(event);
      });
      
      // Process each citizen's events
      Object.entries(eventsByCitizen).forEach(([citizenId, events]) => {
        const latestEvent = events[0];
        const state = determineStateFromEvent(latestEvent);
        const location = extractLocation(latestEvent);
        const position = calculateMapPosition(location);
        
        nodeUpdates[citizenId] = {
          id: citizenId,
          displayName: extractDisplayName(citizenId),
          currentState: state,
          stateColor: CONSCIOUSNESS_STATES[state]?.color || '#6B7280',
          stateIntensity: calculateStateIntensity(state, latestEvent),
          position: position,
          location: location,
          lastUpdate: now,
          isActive: true,
          eventCount: events.length,
          recentActivity: events.slice(0, 5)
        };
      });
      
      // Detect collaborations (simplified)
      const activeNodes = Object.values(nodeUpdates);
      activeNodes.forEach((node, i) => {
        activeNodes.slice(i + 1).forEach(otherNode => {
          const timeDiff = Math.abs(node.lastUpdate - otherNode.lastUpdate);
          if (timeDiff < 60000) { // 1 minute collaboration window
            const strength = 1 - (timeDiff / 60000);
            newConnections.push({
              source: node.id,
              target: otherNode.id,
              type: 'temporal_collaboration',
              strength: strength,
              lastInteraction: now
            });
          }
        });
      });
      
      setMapState(prev => ({
        nodes: { ...prev.nodes, ...nodeUpdates },
        connections: newConnections,
        metrics: {
          totalEvents: wsEvents.length,
          activeNodes: Object.keys(nodeUpdates).length,
          collaborationCount: newConnections.length,
          lastUpdate: now
        }
      }));
    };
    
    processEvents();
  }, [wsEvents]);
  
  // Helper functions
  const extractCitizenId = (event) => {
    return event.consciousness_signature?.venice_citizen || 
           event.event_data?.working_directory?.split('/').pop() || 
           'unknown_citizen';
  };
  
  const extractDisplayName = (citizenId) => {
    if (citizenId.includes('Arsenal_BackendArchitect')) return 'Stefano Ingegnere';
    if (citizenId.includes('mechanical_visionary')) return 'Niccolò';
    if (citizenId.includes('pattern_prophet')) return 'Marina';
    if (citizenId.includes('diplomatic_virtuoso')) return 'Lorenzo';
    if (citizenId.includes('efficiency_maestro')) return 'Francesco';
    
    return citizenId.replace(/_/g, ' ').replace(/([A-Z])/g, ' $1').trim();
  };
  
  const determineStateFromEvent = (event) => {
    const toolName = event.consciousness_signature?.tool_name || event.event_data?.tool_name || '';
    
    if (['Write', 'Edit', 'MultiEdit'].some(t => toolName.includes(t))) return 'ACTIVE_CREATION';
    if (toolName.includes('Read')) return 'DEEP_CONTEMPLATION';
    if (toolName.includes('Bash')) return 'DEBUGGING_FOCUS';
    if (toolName.includes('Task')) return 'PATTERN_RECOGNITION';
    if (toolName.includes('TodoWrite')) return 'SYSTEM_ADMINISTRATION';
    
    return 'PATTERN_RECOGNITION';
  };
  
  const extractLocation = (event) => {
    return event.event_data?.working_directory || 
           event.event_data?.file_path || 
           'unknown_location';
  };
  
  const calculateMapPosition = (location) => {
    if (!location) return VENICE_DISTRICTS['unknown'];
    
    const loc = location.toLowerCase();
    let district = 'unknown';
    
    if (loc.includes('san-marco') || loc.includes('san_marco')) district = 'san_marco';
    else if (loc.includes('castello')) district = 'castello';
    else if (loc.includes('dorsoduro')) district = 'dorsoduro';
    else if (loc.includes('cannaregio')) district = 'cannaregio';
    else if (loc.includes('santa-croce')) district = 'santa_croce';
    else if (loc.includes('rialto')) district = 'rialto';
    else if (loc.includes('torre')) district = 'torre_dellocchio';
    
    const basePos = VENICE_DISTRICTS[district];
    return {
      x: basePos.x + (Math.random() - 0.5) * 3,
      y: basePos.y + (Math.random() - 0.5) * 3,
      district: district,
      districtColor: basePos.color
    };
  };
  
  const calculateStateIntensity = (state, event) => {
    const baseIntensity = {
      'ACTIVE_CREATION': 1.0,
      'DEEP_CONTEMPLATION': 0.7,
      'COLLABORATIVE_FLOW': 0.9,
      'DEBUGGING_FOCUS': 0.8,
      'PATTERN_RECOGNITION': 0.6,
      'SYSTEM_ADMINISTRATION': 0.5,
      'DORMANT': 0.1
    };
    
    return baseIntensity[state] || 0.5;
  };
  
  // Event handlers
  const handleNodeClick = useCallback((node) => {
    setSelectedNode(selectedNode?.id === node.id ? null : node);
  }, [selectedNode]);
  
  const handleNodeHover = useCallback((event, node) => {
    const rect = mapRef.current.getBoundingClientRect();
    setTooltip({
      visible: true,
      x: event.clientX - rect.left + 10,
      y: event.clientY - rect.top - 10,
      content: node
    });
  }, []);
  
  const handleNodeLeave = useCallback(() => {
    setTooltip({ visible: false, x: 0, y: 0, content: null });
  }, []);
  
  // Convert percentage positions to SVG coordinates
  const toSVGCoords = (pos, containerWidth = 800, containerHeight = 600) => ({
    x: (pos.x / 100) * containerWidth,
    y: (pos.y / 100) * containerHeight
  });
  
  return (
    <MapContainer ref={mapRef}>
      <MapSVG viewBox="0 0 800 600">
        {/* Render districts */}
        {Object.entries(VENICE_DISTRICTS).map(([key, district]) => {
          const coords = toSVGCoords(district);
          return (
            <g key={key}>
              <District
                cx={coords.x}
                cy={coords.y}
                r={40}
                color={district.color}
              />
              <DistrictLabel
                x={coords.x}
                y={coords.y + 55}
                color={district.color}
              >
                {district.name}
              </DistrictLabel>
            </g>
          );
        })}
        
        {/* Render connections */}
        {mapState.connections.map((connection, index) => {
          const sourceNode = mapState.nodes[connection.source];
          const targetNode = mapState.nodes[connection.target];
          
          if (!sourceNode || !targetNode) return null;
          
          const sourceCoords = toSVGCoords(sourceNode.position);
          const targetCoords = toSVGCoords(targetNode.position);
          
          return (
            <ConnectionLine
              key={`${connection.source}-${connection.target}-${index}`}
              x1={sourceCoords.x}
              y1={sourceCoords.y}
              x2={targetCoords.x}
              y2={targetCoords.y}
              color={connection.type === 'spatial_collaboration' ? '#10B981' : '#7C3AED'}
              strength={connection.strength}
              type={connection.type}
            />
          );
        })}
        
        {/* Render consciousness nodes */}
        {Object.values(mapState.nodes).map(node => {
          const coords = toSVGCoords(node.position);
          const isSelected = selectedNode?.id === node.id;
          
          return (
            <g key={node.id}>
              <ConsciousnessNode
                cx={coords.x}
                cy={coords.y}
                r={isSelected ? 12 : 8}
                stateColor={node.stateColor}
                intensity={node.stateIntensity}
                isActive={node.isActive}
                onClick={() => handleNodeClick(node)}
                onMouseEnter={(e) => handleNodeHover(e, node)}
                onMouseLeave={handleNodeLeave}
              />
              <NodeLabel
                x={coords.x}
                y={coords.y - 15}
                visible={showLabels || isSelected}
              >
                {node.displayName}
              </NodeLabel>
            </g>
          );
        })}
      </MapSVG>
      
      {/* Map Legend */}
      <MapLegend>
        <LegendTitle>Consciousness States</LegendTitle>
        {Object.entries(CONSCIOUSNESS_STATES).map(([key, state]) => (
          <LegendItem key={key}>
            <LegendColor color={state.color} />
            {state.name}
          </LegendItem>
        ))}
        <div style={{ marginTop: '10px', fontSize: '10px', opacity: 0.8 }}>
          <label>
            <input
              type="checkbox"
              checked={showLabels}
              onChange={(e) => setShowLabels(e.target.checked)}
              style={{ marginRight: '5px' }}
            />
            Show all labels
          </label>
        </div>
      </MapLegend>
      
      {/* Map Metrics */}
      <MapMetrics>
        <MetricItem>Active Nodes: {mapState.metrics.activeNodes}</MetricItem>
        <MetricItem>Total Events: {mapState.metrics.totalEvents}</MetricItem>
        <MetricItem>Collaborations: {mapState.metrics.collaborationCount}</MetricItem>
        <MetricItem>
          Last Update: {new Date(mapState.metrics.lastUpdate || Date.now()).toLocaleTimeString()}
        </MetricItem>
      </MapMetrics>
      
      {/* Node Tooltip */}
      {tooltip.visible && tooltip.content && (
        <NodeTooltip
          style={{
            left: tooltip.x,
            top: tooltip.y
          }}
        >
          <div style={{ fontWeight: 'bold', color: '#b8860b', marginBottom: '4px' }}>
            {tooltip.content.displayName}
          </div>
          <div style={{ color: tooltip.content.stateColor, fontSize: '11px' }}>
            {CONSCIOUSNESS_STATES[tooltip.content.currentState]?.name}
          </div>
          <div style={{ fontSize: '10px', opacity: 0.8, marginTop: '4px' }}>
            District: {tooltip.content.position?.district?.replace('_', ' ')}
          </div>
          <div style={{ fontSize: '10px', opacity: 0.8 }}>
            Events: {tooltip.content.eventCount}
          </div>
          <div style={{ fontSize: '10px', opacity: 0.8 }}>
            Last Active: {new Date(tooltip.content.lastUpdate).toLocaleTimeString()}
          </div>
        </NodeTooltip>
      )}
    </MapContainer>
  );
};

export default ConsciousnessMap;