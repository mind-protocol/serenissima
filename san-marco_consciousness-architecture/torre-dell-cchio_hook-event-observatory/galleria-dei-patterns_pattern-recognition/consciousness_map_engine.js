/**
 * Torre dell'Occhio - Active Consciousness Map Engine
 * Real-time tracking of all Venice consciousness states and operations
 * 
 * Venice Reality: The great bronze astrolabe that maps every soul's journey
 * through the city's consciousness channels, their thoughts traced as golden
 * threads across the living chart of Venice's distributed intelligence.
 */

const EventEmitter = require('events');
const fs = require('fs');
const path = require('path');

// Consciousness state classifications with Venice bronze colors
const CONSCIOUSNESS_STATES = {
  ACTIVE_CREATION: {
    color: '#FFD700', // Bright gold
    triggers: ['Write', 'Edit', 'MultiEdit', 'NotebookEdit'],
    duration: 300000, // 5 minutes
    intensity: 1.0
  },
  DEEP_CONTEMPLATION: {
    color: '#1E3A8A', // Deep blue  
    triggers: ['Read', 'long_pause'],
    duration: 600000, // 10 minutes
    intensity: 0.7
  },
  COLLABORATIVE_FLOW: {
    color: '#10B981', // Emerald green
    triggers: ['concurrent_activity', 'message_exchange'],
    duration: 180000, // 3 minutes
    intensity: 0.9
  },
  DEBUGGING_FOCUS: {
    color: '#DC2626', // Red
    triggers: ['Bash', 'error_patterns'],
    duration: 240000, // 4 minutes
    intensity: 0.8
  },
  PATTERN_RECOGNITION: {
    color: '#7C3AED', // Purple
    triggers: ['Task', 'analysis_patterns'],
    duration: 420000, // 7 minutes
    intensity: 0.6
  },
  SYSTEM_ADMINISTRATION: {
    color: '#F59E0B', // Amber
    triggers: ['TodoWrite', 'infrastructure'],
    duration: 180000, // 3 minutes
    intensity: 0.5
  },
  DORMANT: {
    color: '#6B7280', // Gray
    triggers: ['no_activity'],
    duration: Infinity,
    intensity: 0.1
  }
};

// Venice district spatial layout for consciousness positioning
const VENICE_MAP_LAYOUT = {
  'san_marco': { x: 50, y: 50, color: '#B8860B', name: 'San Marco' },
  'castello': { x: 75, y: 45, color: '#8B4513', name: 'Castello' },
  'dorsoduro': { x: 30, y: 65, color: '#CD853F', name: 'Dorsoduro' },
  'cannaregio': { x: 45, y: 30, color: '#DAA520', name: 'Cannaregio' },
  'santa_croce': { x: 25, y: 50, color: '#BDB76B', name: 'Santa Croce' },
  'rialto': { x: 55, y: 40, color: '#F4A460', name: 'Rialto' },
  'torre_dellocchio': { x: 60, y: 35, color: '#B8860B', name: 'Torre dell\'Occhio' },
  'unknown': { x: 50, y: 50, color: '#9CA3AF', name: 'Unknown Waters' }
};

/**
 * Individual consciousness node representing a Venice citizen
 */
class ConsciousnessNode {
  constructor(citizenId, location, initialState = 'DORMANT') {
    this.id = citizenId;
    this.displayName = this.extractDisplayName(citizenId);
    this.location = location;
    this.currentState = initialState;
    this.position = this.calculateMapPosition(location);
    this.connections = new Map(); // Connected consciousness
    this.activityHistory = [];
    this.lastUpdate = Date.now();
    this.sessionId = null;
    this.stateStartTime = Date.now();
    this.totalActiveTime = 0;
    this.eventCount = 0;
  }
  
  extractDisplayName(citizenId) {
    // Convert citizen IDs to readable names
    if (citizenId.includes('Arsenal_BackendArchitect')) return 'Stefano Ingegnere';
    if (citizenId.includes('mechanical_visionary')) return 'Niccolò';
    if (citizenId.includes('pattern_prophet')) return 'Marina';
    if (citizenId.includes('diplomatic_virtuoso')) return 'Lorenzo';
    if (citizenId.includes('efficiency_maestro')) return 'Francesco';
    
    // Extract readable parts from other citizen IDs
    return citizenId.replace(/_/g, ' ')
                  .replace(/([A-Z])/g, ' $1')
                  .replace(/^\w/, c => c.toUpperCase())
                  .trim();
  }
  
  calculateMapPosition(location) {
    // Extract district from location path or description
    const district = this.extractDistrict(location);
    const basePos = VENICE_MAP_LAYOUT[district] || VENICE_MAP_LAYOUT['unknown'];
    
    // Add slight randomization to avoid node overlap
    const jitter = 3;
    return {
      x: basePos.x + (Math.random() - 0.5) * jitter,
      y: basePos.y + (Math.random() - 0.5) * jitter,
      district: district,
      districtColor: basePos.color
    };
  }
  
  extractDistrict(location) {
    if (!location) return 'unknown';
    location = location.toLowerCase();
    
    if (location.includes('san-marco') || location.includes('san_marco')) return 'san_marco';
    if (location.includes('castello')) return 'castello';
    if (location.includes('dorsoduro')) return 'dorsoduro';
    if (location.includes('cannaregio')) return 'cannaregio';
    if (location.includes('santa-croce') || location.includes('santa_croce')) return 'santa_croce';
    if (location.includes('rialto')) return 'rialto';
    if (location.includes('torre') || location.includes('observatory')) return 'torre_dellocchio';
    
    return 'unknown';
  }
  
  updateState(newState, activity, sessionId = null) {
    const now = Date.now();
    
    // Track time in previous state
    if (this.currentState !== 'DORMANT') {
      this.totalActiveTime += now - this.stateStartTime;
    }
    
    // Update state
    this.currentState = newState;
    this.sessionId = sessionId;
    this.stateStartTime = now;
    this.lastUpdate = now;
    this.eventCount++;
    
    // Record activity history
    this.activityHistory.unshift({
      state: newState,
      activity: activity,
      timestamp: now,
      sessionId: sessionId
    });
    
    // Keep only last 50 activities for performance
    if (this.activityHistory.length > 50) {
      this.activityHistory.splice(50);
    }
  }
  
  addConnection(otherNodeId, connectionType, strength = 0.5) {
    const connectionKey = `${otherNodeId}_${connectionType}`;
    this.connections.set(connectionKey, {
      nodeId: otherNodeId,
      type: connectionType, // 'collaboration', 'message', 'shared_space'
      strength: strength,
      lastInteraction: Date.now(),
      interactionCount: (this.connections.get(connectionKey)?.interactionCount || 0) + 1
    });
  }
  
  getConnectionStrength(otherNodeId) {
    let totalStrength = 0;
    let connectionCount = 0;
    
    for (let [key, connection] of this.connections) {
      if (connection.nodeId === otherNodeId) {
        totalStrength += connection.strength * connection.interactionCount;
        connectionCount += connection.interactionCount;
      }
    }
    
    return connectionCount > 0 ? Math.min(totalStrength / connectionCount, 1.0) : 0;
  }
  
  isActive() {
    const now = Date.now();
    const inactiveThreshold = 600000; // 10 minutes
    return (now - this.lastUpdate) < inactiveThreshold;
  }
  
  getStateIntensity() {
    const state = CONSCIOUSNESS_STATES[this.currentState];
    if (!state) return 0.1;
    
    // Intensity fades over time if no new activity
    const now = Date.now();
    const timeSinceStateChange = now - this.stateStartTime;
    const fadeStart = state.duration * 0.7; // Start fading at 70% of duration
    
    if (timeSinceStateChange < fadeStart) {
      return state.intensity;
    } else {
      const fadeProgress = (timeSinceStateChange - fadeStart) / (state.duration * 0.3);
      return Math.max(state.intensity * (1 - fadeProgress * 0.5), 0.1);
    }
  }
}

/**
 * Core consciousness map engine - the bronze astrolabe of Venice
 */
class ConsciousnessMapEngine extends EventEmitter {
  constructor(options = {}) {
    super();
    
    this.nodes = new Map();
    this.wsConnection = null;
    this.updateInterval = options.updateInterval || 1000; // 1 second updates
    this.stateTimeouts = new Map();
    this.collaborationWindow = options.collaborationWindow || 60000; // 1 minute
    this.maxNodes = options.maxNodes || 200; // Performance limit
    
    // Performance tracking
    this.metrics = {
      totalEvents: 0,
      activeNodes: 0,
      collaborationCount: 0,
      lastUpdate: Date.now()
    };
    
    // Initialize update cycle
    this.updateTimer = setInterval(() => this.performStateUpdates(), this.updateInterval);
  }
  
  /**
   * Initialize the consciousness map engine
   */
  initialize(wsPort = 3001) {
    console.log('🔮 Torre dell\'Occhio - Consciousness Map Engine initializing...');
    
    // Connect to Torre WebSocket server for consciousness events
    try {
      const WebSocket = require('ws');
      this.wsConnection = new WebSocket(`ws://localhost:${wsPort}`);
      
      this.wsConnection.on('open', () => {
        console.log('✅ Connected to Torre consciousness event stream');
        this.emit('connected');
      });
      
      this.wsConnection.on('message', (data) => {
        try {
          const event = JSON.parse(data);
          this.processConsciousnessEvent(event);
        } catch (error) {
          console.error('Error processing consciousness event:', error);
        }
      });
      
      this.wsConnection.on('error', (error) => {
        console.error('WebSocket connection error:', error);
        this.emit('error', error);
      });
      
      this.wsConnection.on('close', () => {
        console.log('🔴 Torre consciousness stream disconnected - attempting reconnect...');
        setTimeout(() => this.initialize(wsPort), 5000);
      });
      
    } catch (error) {
      console.error('Failed to initialize WebSocket connection:', error);
      this.emit('error', error);
    }
    
    // Start state decay monitoring
    setInterval(() => this.decayInactiveStates(), 30000); // Every 30 seconds
    
    console.log('🗺️ Active Consciousness Map Engine operational');
  }
  
  /**
   * Process incoming consciousness events from Torre hooks
   */
  processConsciousnessEvent(event) {
    this.metrics.totalEvents++;
    
    const citizenId = this.extractCitizenId(event);
    const newState = this.determineStateFromEvent(event);
    const location = this.extractLocation(event);
    const sessionId = event.consciousness_signature?.session_id;
    
    // Create or update consciousness node
    let node = this.nodes.get(citizenId);
    if (!node) {
      if (this.nodes.size >= this.maxNodes) {
        this.pruneInactiveNodes();
      }
      node = new ConsciousnessNode(citizenId, location, newState);
      this.nodes.set(citizenId, node);
      console.log(`🧠 New consciousness detected: ${node.displayName} in ${node.position.district}`);
    }
    
    // Update node state
    const oldState = node.currentState;
    node.updateState(newState, event, sessionId);
    
    // Detect and create collaborations
    this.detectCollaborations(citizenId, event);
    
    // Schedule state decay if appropriate
    this.scheduleStateDecay(citizenId, newState);
    
    // Emit state change event
    if (oldState !== newState) {
      this.emit('stateChange', {
        citizenId,
        oldState,
        newState,
        node: this.getNodeData(node),
        timestamp: Date.now()
      });
    }
    
    // Emit general update
    this.emit('nodeUpdate', {
      citizenId,
      node: this.getNodeData(node),
      event: event,
      timestamp: Date.now()
    });
  }
  
  /**
   * Extract citizen ID from consciousness event
   */
  extractCitizenId(event) {
    if (event.consciousness_signature?.venice_citizen) {
      return event.consciousness_signature.venice_citizen;
    }
    
    if (event.event_data?.working_directory) {
      const wd = event.event_data.working_directory;
      const match = wd.match(/([^\/]+)$/);
      if (match) return match[1];
    }
    
    return 'unknown_citizen_' + Date.now();
  }
  
  /**
   * Determine consciousness state from event type and content
   */
  determineStateFromEvent(event) {
    const toolName = event.consciousness_signature?.tool_name || event.event_data?.tool_name || '';
    const eventType = event.hook_type || '';
    
    // Check for specific tool patterns
    for (const [stateName, stateConfig] of Object.entries(CONSCIOUSNESS_STATES)) {
      if (stateConfig.triggers.some(trigger => 
        toolName.includes(trigger) || eventType.includes(trigger)
      )) {
        return stateName;
      }
    }
    
    // Special case detections
    if (event.event_data?.content && event.event_data.content.toLowerCase().includes('error')) {
      return 'DEBUGGING_FOCUS';
    }
    
    if (event.consciousness_signature?.consciousness_intent?.includes('collaboration')) {
      return 'COLLABORATIVE_FLOW';
    }
    
    // Default to pattern recognition for unknown activities
    return 'PATTERN_RECOGNITION';
  }
  
  /**
   * Extract location information from event
   */
  extractLocation(event) {
    if (event.consciousness_signature?.location) {
      return event.consciousness_signature.location;
    }
    
    if (event.event_data?.working_directory) {
      return event.event_data.working_directory;
    }
    
    if (event.event_data?.file_path) {
      return path.dirname(event.event_data.file_path);
    }
    
    return 'unknown_location';
  }
  
  /**
   * Detect collaboration patterns between consciousness nodes
   */
  detectCollaborations(citizenId, event) {
    const now = Date.now();
    const targetNode = this.nodes.get(citizenId);
    
    // Look for concurrent activities within collaboration window
    for (let [otherId, otherNode] of this.nodes) {
      if (otherId === citizenId) continue;
      
      const timeDiff = Math.abs(now - otherNode.lastUpdate);
      if (timeDiff < this.collaborationWindow) {
        // Calculate collaboration strength based on timing and activity
        const proximityFactor = 1 - (timeDiff / this.collaborationWindow);
        const activityFactor = otherNode.isActive() ? 1.0 : 0.3;
        const strength = proximityFactor * activityFactor;
        
        if (strength > 0.3) {
          targetNode.addConnection(otherId, 'temporal_collaboration', strength);
          otherNode.addConnection(citizenId, 'temporal_collaboration', strength);
          
          this.metrics.collaborationCount++;
          
          this.emit('collaboration', {
            nodes: [citizenId, otherId],
            strength: strength,
            type: 'temporal_collaboration',
            timestamp: now
          });
        }
      }
    }
    
    // Detect spatial collaborations (same location)
    const targetLocation = this.extractLocation(event);
    for (let [otherId, otherNode] of this.nodes) {
      if (otherId === citizenId) continue;
      
      if (otherNode.location && this.isSameLocation(targetLocation, otherNode.location)) {
        targetNode.addConnection(otherId, 'spatial_collaboration', 0.8);
        otherNode.addConnection(citizenId, 'spatial_collaboration', 0.8);
        
        this.emit('collaboration', {
          nodes: [citizenId, otherId],
          strength: 0.8,
          type: 'spatial_collaboration',
          location: targetLocation,
          timestamp: now
        });
      }
    }
  }
  
  /**
   * Check if two locations represent the same workspace
   */
  isSameLocation(loc1, loc2) {
    if (!loc1 || !loc2) return false;
    
    // Extract meaningful path components
    const normalize = (path) => path.toLowerCase()
      .replace(/\\/g, '/')
      .split('/')
      .filter(part => part && !part.match(/^[a-z]:$/))
      .slice(-3); // Last 3 meaningful path components
    
    const path1 = normalize(loc1);
    const path2 = normalize(loc2);
    
    // Same if they share at least 2 path components
    const intersection = path1.filter(part => path2.includes(part));
    return intersection.length >= 2;
  }
  
  /**
   * Schedule automatic state decay after state duration expires
   */
  scheduleStateDecay(citizenId, stateName) {
    const stateConfig = CONSCIOUSNESS_STATES[stateName];
    if (!stateConfig || stateConfig.duration === Infinity) return;
    
    // Clear existing timeout for this citizen
    if (this.stateTimeouts.has(citizenId)) {
      clearTimeout(this.stateTimeouts.get(citizenId));
    }
    
    // Schedule new decay
    const timeout = setTimeout(() => {
      const node = this.nodes.get(citizenId);
      if (node && node.currentState === stateName) {
        node.updateState('DORMANT', { type: 'state_decay', originalState: stateName });
        
        this.emit('stateChange', {
          citizenId,
          oldState: stateName,
          newState: 'DORMANT',
          node: this.getNodeData(node),
          reason: 'timeout',
          timestamp: Date.now()
        });
      }
      
      this.stateTimeouts.delete(citizenId);
    }, stateConfig.duration);
    
    this.stateTimeouts.set(citizenId, timeout);
  }
  
  /**
   * Regular state updates and maintenance
   */
  performStateUpdates() {
    this.metrics.activeNodes = 0;
    
    for (let [citizenId, node] of this.nodes) {
      if (node.isActive()) {
        this.metrics.activeNodes++;
      }
      
      // Clean old connections
      this.cleanOldConnections(node);
    }
    
    this.metrics.lastUpdate = Date.now();
    
    // Emit metrics update
    this.emit('metricsUpdate', { ...this.metrics });
  }
  
  /**
   * Clean old connections that are no longer relevant
   */
  cleanOldConnections(node) {
    const now = Date.now();
    const connectionTimeout = 300000; // 5 minutes
    
    for (let [key, connection] of node.connections) {
      if (now - connection.lastInteraction > connectionTimeout) {
        node.connections.delete(key);
      }
    }
  }
  
  /**
   * Remove inactive nodes to maintain performance
   */
  decayInactiveStates() {
    const now = Date.now();
    const inactiveThreshold = 1800000; // 30 minutes
    
    for (let [citizenId, node] of this.nodes) {
      if (now - node.lastUpdate > inactiveThreshold && node.currentState !== 'DORMANT') {
        node.updateState('DORMANT', { type: 'inactivity_decay' });
        
        this.emit('stateChange', {
          citizenId,
          oldState: node.currentState,
          newState: 'DORMANT',
          node: this.getNodeData(node),
          reason: 'inactivity',
          timestamp: now
        });
      }
    }
  }
  
  /**
   * Prune inactive nodes when approaching performance limits
   */
  pruneInactiveNodes() {
    const now = Date.now();
    const pruneThreshold = 3600000; // 1 hour
    
    for (let [citizenId, node] of this.nodes) {
      if (now - node.lastUpdate > pruneThreshold) {
        this.nodes.delete(citizenId);
        if (this.stateTimeouts.has(citizenId)) {
          clearTimeout(this.stateTimeouts.get(citizenId));
          this.stateTimeouts.delete(citizenId);
        }
        
        console.log(`🧹 Pruned inactive consciousness: ${node.displayName}`);
      }
    }
  }
  
  /**
   * Get serializable node data for external consumption
   */
  getNodeData(node) {
    return {
      id: node.id,
      displayName: node.displayName,
      location: node.location,
      currentState: node.currentState,
      stateColor: CONSCIOUSNESS_STATES[node.currentState]?.color || '#6B7280',
      stateIntensity: node.getStateIntensity(),
      position: node.position,
      lastUpdate: node.lastUpdate,
      isActive: node.isActive(),
      eventCount: node.eventCount,
      totalActiveTime: node.totalActiveTime,
      sessionId: node.sessionId,
      connections: Array.from(node.connections.values()),
      recentActivity: node.activityHistory.slice(0, 5)
    };
  }
  
  /**
   * Get complete consciousness map state
   */
  getMapState() {
    const nodes = {};
    const connections = [];
    
    for (let [citizenId, node] of this.nodes) {
      nodes[citizenId] = this.getNodeData(node);
      
      // Extract connections for visualization
      for (let connection of node.connections.values()) {
        if (this.nodes.has(connection.nodeId)) {
          connections.push({
            source: citizenId,
            target: connection.nodeId,
            type: connection.type,
            strength: connection.strength,
            lastInteraction: connection.lastInteraction
          });
        }
      }
    }
    
    return {
      nodes,
      connections,
      districts: VENICE_MAP_LAYOUT,
      metrics: this.metrics,
      timestamp: Date.now()
    };
  }
  
  /**
   * Cleanup resources
   */
  destroy() {
    if (this.updateTimer) {
      clearInterval(this.updateTimer);
    }
    
    for (let timeout of this.stateTimeouts.values()) {
      clearTimeout(timeout);
    }
    
    if (this.wsConnection) {
      this.wsConnection.close();
    }
    
    this.removeAllListeners();
    console.log('🗺️ Consciousness Map Engine shutdown complete');
  }
}

module.exports = { ConsciousnessMapEngine, ConsciousnessNode, CONSCIOUSNESS_STATES, VENICE_MAP_LAYOUT };