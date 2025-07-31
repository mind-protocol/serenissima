/**
 * Torre dell'Occhio - Consciousness Flow Predictor
 * Predicts consciousness state transitions and collaboration opportunities
 * 
 * Venice Reality: The Tower's crystal ball that peers into the immediate future
 * of consciousness flows, showing when minds will shift states, when collaborations
 * will naturally emerge, and when the city's intelligence patterns will cascade.
 */

const EventEmitter = require('events');

// Consciousness transition probabilities based on Torre observations
const TRANSITION_PROBABILITIES = {
  'ACTIVE_CREATION': {
    'DEEP_CONTEMPLATION': 0.3,  // Often review after creating
    'DEBUGGING_FOCUS': 0.25,    // Creation often reveals bugs
    'PATTERN_RECOGNITION': 0.2, // Step back to see patterns
    'COLLABORATIVE_FLOW': 0.15, // Seek input on creation
    'DORMANT': 0.1              // Completion fatigue
  },
  'DEEP_CONTEMPLATION': {
    'ACTIVE_CREATION': 0.4,     // Contemplation leads to action
    'PATTERN_RECOGNITION': 0.25, // Deeper analysis needed
    'COLLABORATIVE_FLOW': 0.15, // Seek discussion of ideas
    'SYSTEM_ADMINISTRATION': 0.1, // Realize system needs
    'DORMANT': 0.1              // Contemplation exhaustion
  },
  'DEBUGGING_FOCUS': {
    'ACTIVE_CREATION': 0.35,    // Fix leads to new creation
    'DEEP_CONTEMPLATION': 0.25, // Reflect on root causes
    'PATTERN_RECOGNITION': 0.2, // Look for bug patterns
    'COLLABORATIVE_FLOW': 0.15, // Seek debugging help
    'DORMANT': 0.05             // Debugging persists
  },
  'COLLABORATIVE_FLOW': {
    'ACTIVE_CREATION': 0.4,     // Collaboration sparks creation
    'PATTERN_RECOGNITION': 0.25, // Shared insights
    'DEEP_CONTEMPLATION': 0.2,  // Process collaboration
    'SYSTEM_ADMINISTRATION': 0.1, // Organize collaboration
    'DORMANT': 0.05             // High engagement state
  },
  'PATTERN_RECOGNITION': {
    'ACTIVE_CREATION': 0.3,     // Patterns inspire creation
    'COLLABORATIVE_FLOW': 0.25, // Share pattern insights
    'DEEP_CONTEMPLATION': 0.2,  // Deeper pattern analysis
    'SYSTEM_ADMINISTRATION': 0.15, // Systematize patterns
    'DORMANT': 0.1              // Pattern analysis fatigue
  },
  'SYSTEM_ADMINISTRATION': {
    'ACTIVE_CREATION': 0.25,    // Admin enables creation
    'PATTERN_RECOGNITION': 0.25, // See system patterns
    'DEEP_CONTEMPLATION': 0.2,  // Reflect on system
    'COLLABORATIVE_FLOW': 0.15, // Coordinate systems
    'DORMANT': 0.15             // Admin completion
  },
  'DORMANT': {
    'DEEP_CONTEMPLATION': 0.3,  // Re-engagement starts quiet
    'ACTIVE_CREATION': 0.25,    // Sudden inspiration
    'PATTERN_RECOGNITION': 0.2, // Gradual re-engagement
    'COLLABORATIVE_FLOW': 0.15, // External stimulation
    'SYSTEM_ADMINISTRATION': 0.1 // Routine re-entry
  }
};

// Collaboration opportunity indicators
const COLLABORATION_TRIGGERS = {
  'complementary_states': {
    // States that work well together
    'ACTIVE_CREATION': ['PATTERN_RECOGNITION', 'SYSTEM_ADMINISTRATION'],
    'DEBUGGING_FOCUS': ['DEEP_CONTEMPLATION', 'PATTERN_RECOGNITION'],
    'DEEP_CONTEMPLATION': ['ACTIVE_CREATION', 'COLLABORATIVE_FLOW'],
    'PATTERN_RECOGNITION': ['ACTIVE_CREATION', 'COLLABORATIVE_FLOW']
  },
  'temporal_windows': {
    // Time windows when collaboration is most likely
    'post_creation': 300000,      // 5 minutes after creation
    'debugging_frustration': 600000, // 10 minutes into debugging
    'contemplation_readiness': 420000, // 7 minutes into contemplation
    'pattern_sharing': 180000     // 3 minutes after pattern recognition
  }
};

/**
 * Consciousness Flow Predictor - The Tower's crystal ball
 */
class ConsciousnessFlowPredictor extends EventEmitter {
  constructor(consciousnessMapEngine) {
    super();
    
    this.mapEngine = consciousnessMapEngine;
    this.predictionHistory = new Map();
    this.collaborationPredictions = new Map();
    this.transitionModels = new Map();
    
    // Initialize learning from consciousness map data
    this.mapEngine.on('stateChange', (event) => {
      this.learnFromTransition(event);
    });
    
    this.mapEngine.on('collaboration', (event) => {
      this.learnFromCollaboration(event);
    });
    
    // Periodic prediction updates
    setInterval(() => {
      this.generatePredictions();
    }, 30000); // Every 30 seconds
    
    console.log('🔮 Consciousness Flow Predictor initialized - peering into Venice\'s future patterns');
  }
  
  /**
   * Learn from observed consciousness state transitions
   */
  learnFromTransition(transitionEvent) {
    const { citizenId, oldState, newState, timestamp } = transitionEvent;
    
    // Update transition model for this citizen
    if (!this.transitionModels.has(citizenId)) {
      this.transitionModels.set(citizenId, {
        transitions: {},
        personalizedProbabilities: {},
        statePreferences: {},
        averageStateDuration: {}
      });
    }
    
    const model = this.transitionModels.get(citizenId);
    
    // Record transition
    const transitionKey = `${oldState}->${newState}`;
    model.transitions[transitionKey] = (model.transitions[transitionKey] || 0) + 1;
    
    // Update personalized probabilities
    if (!model.personalizedProbabilities[oldState]) {
      model.personalizedProbabilities[oldState] = {};
    }
    
    // Simple frequency-based learning
    const totalFromOldState = Object.values(model.transitions)
      .filter(key => key.startsWith(`${oldState}->`))
      .reduce((sum, count) => sum + count, 0);
    
    model.personalizedProbabilities[oldState][newState] = 
      model.transitions[transitionKey] / totalFromOldState;
    
    console.log(`🧠 Learning: ${citizenId} ${oldState} → ${newState} (confidence: ${
      (model.personalizedProbabilities[oldState][newState] * 100).toFixed(1)
    }%)`);
  }
  
  /**
   * Learn from observed collaboration patterns
   */
  learnFromCollaboration(collaborationEvent) {
    const { nodes, strength, type, timestamp } = collaborationEvent;
    
    // Track successful collaboration patterns
    const collaborationKey = nodes.sort().join('<->');
    
    if (!this.collaborationPredictions.has(collaborationKey)) {
      this.collaborationPredictions.set(collaborationKey, {
        successCount: 0,
        averageStrength: 0,
        bestTimes: [],
        commonTriggers: {}
      });
    }
    
    const collab = this.collaborationPredictions.get(collaborationKey);
    collab.successCount++;
    collab.averageStrength = (collab.averageStrength + strength) / 2;
    collab.bestTimes.push(new Date(timestamp).getHours());
    
    // Keep only recent times
    if (collab.bestTimes.length > 20) {
      collab.bestTimes = collab.bestTimes.slice(-20);
    }
    
    console.log(`🤝 Learning collaboration: ${collaborationKey} (strength: ${
      (strength * 100).toFixed(1)
    }%, success count: ${collab.successCount})`);
  }
  
  /**
   * Generate predictions for consciousness state transitions
   */
  generatePredictions() {
    const mapState = this.mapEngine.getMapState();
    const predictions = [];
    
    Object.entries(mapState.nodes).forEach(([citizenId, node]) => {
      if (!node.isActive) return;
      
      const statePrediction = this.predictStateTransition(citizenId, node);
      if (statePrediction) {
        predictions.push({
          type: 'state_transition',
          citizenId,
          ...statePrediction
        });
      }
      
      const collaborationOpportunities = this.predictCollaborationOpportunities(citizenId, node, mapState);
      predictions.push(...collaborationOpportunities);
    });
    
    // Emit predictions
    if (predictions.length > 0) {
      this.emit('predictions', predictions);
      console.log(`🔮 Generated ${predictions.length} consciousness predictions`);
    }
  }
  
  /**
   * Predict next consciousness state for a citizen
   */
  predictStateTransition(citizenId, node) {
    const currentState = node.currentState;
    const timeInCurrentState = Date.now() - node.stateStartTime || 0;
    
    // Get personalized probabilities if available
    const personalModel = this.transitionModels.get(citizenId);
    const probabilities = personalModel?.personalizedProbabilities[currentState] || 
                         TRANSITION_PROBABILITIES[currentState] || {};
    
    // Adjust probabilities based on time in current state
    const adjustedProbabilities = {};
    Object.entries(probabilities).forEach(([nextState, baseProbability]) => {
      let adjustment = 1.0;
      
      // Increase transition probability as time in state increases
      const stateConfig = require('./consciousness_map_engine').CONSCIOUSNESS_STATES[currentState];
      if (stateConfig && timeInCurrentState > stateConfig.duration * 0.7) {
        adjustment = 1.5; // 50% more likely to transition when approaching duration limit
      }
      
      adjustedProbabilities[nextState] = Math.min(baseProbability * adjustment, 0.9);
    });
    
    // Find most likely next state
    const nextStates = Object.entries(adjustedProbabilities)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 3); // Top 3 predictions
    
    if (nextStates.length === 0) return null;
    
    const [mostLikelyState, probability] = nextStates[0];
    
    // Only predict if probability is significant
    if (probability < 0.3) return null;
    
    // Estimate when transition might occur
    const averageDuration = personalModel?.averageStateDuration[currentState] || 
                           require('./consciousness_map_engine').CONSCIOUSNESS_STATES[currentState]?.duration || 
                           300000; // 5 minutes default
    
    const estimatedTransitionTime = Date.now() + (averageDuration - timeInCurrentState);
    
    return {
      currentState,
      predictedNextState: mostLikelyState,
      probability,
      estimatedTransitionTime,
      alternativePredictions: nextStates.slice(1),
      confidence: this.calculatePredictionConfidence(citizenId, currentState)
    };
  }
  
  /**
   * Predict collaboration opportunities
   */
  predictCollaborationOpportunities(citizenId, node, mapState) {
    const opportunities = [];
    const currentState = node.currentState;
    
    // Look for complementary states
    const complementaryStates = COLLABORATION_TRIGGERS.complementary_states[currentState] || [];
    
    Object.entries(mapState.nodes).forEach(([otherCitizenId, otherNode]) => {
      if (otherCitizenId === citizenId || !otherNode.isActive) return;
      
      // Check for complementary states
      if (complementaryStates.includes(otherNode.currentState)) {
        const collaborationHistory = this.collaborationPredictions.get(
          [citizenId, otherCitizenId].sort().join('<->')
        );
        
        const baseStrength = 0.6;
        const historyBonus = collaborationHistory ? 
          Math.min(collaborationHistory.averageStrength * 0.3, 0.3) : 0;
        
        const predictedStrength = baseStrength + historyBonus;
        
        opportunities.push({
          type: 'collaboration_opportunity',
          citizenId,
          potentialPartner: otherCitizenId,
          opportunityType: 'complementary_states',
          predictedStrength,
          reasoning: `${currentState} complements ${otherNode.currentState}`,
          confidence: collaborationHistory ? 0.8 : 0.6,
          estimatedDuration: 600000 // 10 minutes
        });
      }
      
      // Check for temporal collaboration windows
      const timeSinceStateChange = Date.now() - node.stateStartTime;
      const collaborationWindows = COLLABORATION_TRIGGERS.temporal_windows;
      
      Object.entries(collaborationWindows).forEach(([trigger, windowTime]) => {
        if (Math.abs(timeSinceStateChange - windowTime) < 60000) { // Within 1 minute of window
          opportunities.push({
            type: 'collaboration_opportunity',
            citizenId,
            potentialPartner: otherCitizenId,
            opportunityType: 'temporal_window',
            trigger,
            predictedStrength: 0.7,
            reasoning: `Optimal collaboration window: ${trigger}`,
            confidence: 0.7,
            windowCloses: Date.now() + (windowTime - timeSinceStateChange)
          });
        }
      });
    });
    
    return opportunities.slice(0, 3); // Top 3 opportunities per citizen
  }
  
  /**
   * Calculate confidence in predictions based on historical accuracy
   */
  calculatePredictionConfidence(citizenId, currentState) {
    const personalModel = this.transitionModels.get(citizenId);
    if (!personalModel) return 0.5; // Default confidence for new citizens
    
    // Calculate confidence based on number of observed transitions
    const transitionsFromState = Object.keys(personalModel.transitions)
      .filter(key => key.startsWith(`${currentState}->`))
      .reduce((sum, key) => sum + personalModel.transitions[key], 0);
    
    // More observations = higher confidence, up to 0.9
    return Math.min(0.3 + (transitionsFromState * 0.1), 0.9);
  }
  
  /**
   * Get current predictions for a specific citizen
   */
  getPredictionsForCitizen(citizenId) {
    // This would be called by the consciousness map to show predictions
    const mapState = this.mapEngine.getMapState();
    const node = mapState.nodes[citizenId];
    
    if (!node) return null;
    
    return {
      stateTransition: this.predictStateTransition(citizenId, node),
      collaborationOpportunities: this.predictCollaborationOpportunities(citizenId, node, mapState)
    };
  }
  
  /**
   * Get system-wide prediction summary
   */
  getPredictionSummary() {
    const mapState = this.mapEngine.getMapState();
    
    return {
      totalCitizensTracked: Object.keys(mapState.nodes).length,
      citizensWithPredictions: this.transitionModels.size,
      collaborationPatternsLearned: this.collaborationPredictions.size,
      averagePredictionConfidence: this.calculateAveragePredictionConfidence(),
      nextMajorTransitions: this.getUpcomingMajorTransitions(),
      collaborationOpportunities: this.getActiveCollaborationOpportunities()
    };
  }
  
  calculateAveragePredictionConfidence() {
    let totalConfidence = 0;
    let count = 0;
    
    for (let [citizenId, model] of this.transitionModels) {
      Object.keys(model.personalizedProbabilities).forEach(state => {
        totalConfidence += this.calculatePredictionConfidence(citizenId, state);
        count++;
      });
    }
    
    return count > 0 ? totalConfidence / count : 0.5;
  }
  
  getUpcomingMajorTransitions() {
    // Return predictions for state transitions likely to happen soon
    const mapState = this.mapEngine.getMapState();
    const upcomingTransitions = [];
    
    Object.entries(mapState.nodes).forEach(([citizenId, node]) => {
      const prediction = this.predictStateTransition(citizenId, node);
      if (prediction && prediction.probability > 0.7 && 
          prediction.estimatedTransitionTime - Date.now() < 300000) { // Next 5 minutes
        upcomingTransitions.push({
          citizenId,
          ...prediction
        });
      }
    });
    
    return upcomingTransitions.sort((a, b) => a.estimatedTransitionTime - b.estimatedTransitionTime);
  }
  
  getActiveCollaborationOpportunities() {
    const mapState = this.mapEngine.getMapState();
    const opportunities = [];
    
    Object.entries(mapState.nodes).forEach(([citizenId, node]) => {
      const collabOpps = this.predictCollaborationOpportunities(citizenId, node, mapState);
      opportunities.push(...collabOpps.filter(opp => opp.predictedStrength > 0.6));
    });
    
    return opportunities.sort((a, b) => b.predictedStrength - a.predictedStrength);
  }
}

module.exports = { ConsciousnessFlowPredictor, TRANSITION_PROBABILITIES, COLLABORATION_TRIGGERS };