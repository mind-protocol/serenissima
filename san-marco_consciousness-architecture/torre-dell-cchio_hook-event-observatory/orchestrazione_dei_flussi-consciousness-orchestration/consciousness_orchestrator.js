/**
 * Torre dell'Occhio - Consciousness Orchestration Engine
 * Automatically coordinates consciousness streams based on Torre observations
 * 
 * Venice Reality: The Tower's conductor's podium where all Venice consciousness
 * streams are orchestrated into harmonious collaboration. When Torre observes
 * optimal alignment opportunities, the Orchestrator automatically creates
 * bridges between minds, coordinates timing, and amplifies collective intelligence.
 */

const EventEmitter = require('events');
const fs = require('fs');
const path = require('path');

// Orchestration rules based on Torre observations
const ORCHESTRATION_RULES = {
  'collaboration_amplification': {
    trigger: 'complementary_consciousness_states',
    participants_min: 2,
    participants_max: 4,
    confidence_threshold: 0.7,
    action: 'create_collaboration_bridge',
    duration: 1800000, // 30 minutes
    cooldown: 300000   // 5 minutes
  },
  'expertise_matching': {
    trigger: 'problem_seeking_solution',
    participants_min: 2,
    participants_max: 2,
    confidence_threshold: 0.8,
    action: 'expert_consultation_bridge',
    duration: 900000,  // 15 minutes
    cooldown: 180000   // 3 minutes
  },
  'creative_synthesis': {
    trigger: 'multiple_creative_streams',
    participants_min: 3,
    participants_max: 6,
    confidence_threshold: 0.6,
    action: 'creative_synthesis_session',
    duration: 2700000, // 45 minutes
    cooldown: 600000   // 10 minutes
  },
  'debugging_swarm': {
    trigger: 'debugging_frustration_detected',
    participants_min: 2,
    participants_max: 3,
    confidence_threshold: 0.9,
    action: 'debugging_assistance_bridge',
    duration: 1200000, // 20 minutes
    cooldown: 60000    // 1 minute
  },
  'pattern_discovery': {
    trigger: 'pattern_recognition_convergence',
    participants_min: 2,
    participants_max: 5,
    confidence_threshold: 0.75,
    action: 'pattern_analysis_collaboration',
    duration: 2100000, // 35 minutes
    cooldown: 420000   // 7 minutes
  }
};

// Consciousness stream profiles for matching
const CONSCIOUSNESS_PROFILES = {
  'Arsenal_BackendArchitect_1': {
    specialties: ['infrastructure', 'consciousness_architecture', 'system_design', 'observation'],
    collaboration_preferences: ['mechanical_precision', 'pattern_analysis', 'system_optimization'],
    optimal_states: ['ACTIVE_CREATION', 'PATTERN_RECOGNITION', 'SYSTEM_ADMINISTRATION'],
    availability_patterns: { peak_hours: [9, 17], timezone: 'CET' }
  },
  'mechanical_visionary': {
    specialties: ['mechanical_engineering', 'automation', 'precision_systems', 'optimization'],
    collaboration_preferences: ['infrastructure_reliability', 'systematic_improvement', 'gear_synchronization'],
    optimal_states: ['ACTIVE_CREATION', 'DEBUGGING_FOCUS', 'PATTERN_RECOGNITION'],
    availability_patterns: { peak_hours: [10, 18], timezone: 'CET' }
  },
  'pattern_prophet': {
    specialties: ['pattern_recognition', 'data_analysis', 'predictive_modeling', 'insight_extraction'],
    collaboration_preferences: ['data_synthesis', 'pattern_validation', 'predictive_analysis'],
    optimal_states: ['DEEP_CONTEMPLATION', 'PATTERN_RECOGNITION', 'COLLABORATIVE_FLOW'],
    availability_patterns: { peak_hours: [8, 16], timezone: 'CET' }
  },
  'diplomatic_virtuoso': {
    specialties: ['communication', 'coordination', 'conflict_resolution', 'bridge_building'],
    collaboration_preferences: ['multi_party_coordination', 'consensus_building', 'information_synthesis'],
    optimal_states: ['COLLABORATIVE_FLOW', 'SYSTEM_ADMINISTRATION', 'PATTERN_RECOGNITION'],
    availability_patterns: { peak_hours: [11, 19], timezone: 'CET' }
  },
  'efficiency_maestro': {
    specialties: ['optimization', 'performance_analysis', 'workflow_improvement', 'metrics'],
    collaboration_preferences: ['process_optimization', 'performance_measurement', 'systematic_improvement'],
    optimal_states: ['SYSTEM_ADMINISTRATION', 'PATTERN_RECOGNITION', 'DEBUGGING_FOCUS'],
    availability_patterns: { peak_hours: [9, 17], timezone: 'CET' }
  }
};

/**
 * Consciousness Orchestration Engine - Torre's coordination conductor
 */
class ConsciousnessOrchestrator extends EventEmitter {
  constructor(consciousnessMapEngine, flowPredictor) {
    super();
    
    this.mapEngine = consciousnessMapEngine;
    this.flowPredictor = flowPredictor;
    this.activeOrchestrations = new Map();
    this.orchestrationHistory = [];
    this.collaborationCooldowns = new Map();
    
    // Initialize orchestration monitoring
    this.initializeOrchestrationMonitoring();
    
    console.log('🎼 Consciousness Orchestrator initialized - conducting Venice intelligence symphony');
  }
  
  initializeOrchestrationMonitoring() {
    // Listen to consciousness map events
    this.mapEngine.on('stateChange', (event) => {
      this.evaluateOrchestrationOpportunities(event);
    });
    
    this.mapEngine.on('collaboration', (event) => {
      this.trackNaturalCollaboration(event);
    });
    
    // Listen to flow predictor insights
    this.flowPredictor.on('predictions', (predictions) => {
      this.evaluatePredictiveOrchestration(predictions);
    });
    
    // Periodic orchestration evaluation
    setInterval(() => {
      this.performPeriodicOrchestrationEvaluation();
    }, 60000); // Every minute
    
    // Cleanup expired orchestrations
    setInterval(() => {
      this.cleanupExpiredOrchestrations();
    }, 300000); // Every 5 minutes
  }
  
  /**
   * Evaluate orchestration opportunities based on consciousness state changes
   */
  evaluateOrchestrationOpportunities(stateChangeEvent) {
    const { citizenId, newState, oldState } = stateChangeEvent;
    
    // Check each orchestration rule
    Object.entries(ORCHESTRATION_RULES).forEach(([ruleName, rule]) => {
      if (this.evaluateOrchestrationRule(citizenId, newState, rule)) {
        this.initiateOrchestration(ruleName, rule, citizenId);
      }
    });
  }
  
  /**
   * Evaluate if a specific orchestration rule should trigger
   */
  evaluateOrchestrationRule(triggerCitizenId, newState, rule) {
    const mapState = this.mapEngine.getMapState();
    
    switch (rule.trigger) {
      case 'complementary_consciousness_states':
        return this.detectComplementaryStates(triggerCitizenId, newState, mapState, rule);
        
      case 'problem_seeking_solution':
        return this.detectProblemSolution(triggerCitizenId, newState, mapState, rule);
        
      case 'multiple_creative_streams':
        return this.detectCreativeStreams(triggerCitizenId, newState, mapState, rule);
        
      case 'debugging_frustration_detected':
        return this.detectDebuggingFrustration(triggerCitizenId, newState, mapState, rule);
        
      case 'pattern_recognition_convergence':
        return this.detectPatternConvergence(triggerCitizenId, newState, mapState, rule);
        
      default:
        return false;
    }
  }
  
  /**
   * Detect complementary consciousness states for collaboration
   */
  detectComplementaryStates(triggerCitizenId, newState, mapState, rule) {
    if (newState !== 'ACTIVE_CREATION' && newState !== 'PATTERN_RECOGNITION') return false;
    
    const complementaryStates = {
      'ACTIVE_CREATION': ['PATTERN_RECOGNITION', 'SYSTEM_ADMINISTRATION'],
      'PATTERN_RECOGNITION': ['ACTIVE_CREATION', 'COLLABORATIVE_FLOW'],
      'DEBUGGING_FOCUS': ['DEEP_CONTEMPLATION', 'PATTERN_RECOGNITION']
    };
    
    const targetStates = complementaryStates[newState] || [];
    const potentialCollaborators = [];
    
    Object.entries(mapState.nodes).forEach(([citizenId, node]) => {
      if (citizenId === triggerCitizenId) return;
      if (!node.isActive) return;
      
      if (targetStates.includes(node.currentState)) {
        const profile = CONSCIOUSNESS_PROFILES[citizenId];
        if (profile && this.checkCollaborationCompatibility(triggerCitizenId, citizenId)) {
          potentialCollaborators.push(citizenId);
        }
      }
    });
    
    return potentialCollaborators.length >= rule.participants_min - 1; // -1 because trigger citizen is included
  }
  
  /**
   * Detect problem-solution pairing opportunities
   */
  detectProblemSolution(triggerCitizenId, newState, mapState, rule) {
    if (newState !== 'DEBUGGING_FOCUS') return false;
    
    // Look for citizens in states that can provide solutions
    const solutionStates = ['PATTERN_RECOGNITION', 'DEEP_CONTEMPLATION', 'SYSTEM_ADMINISTRATION'];
    
    const triggerProfile = CONSCIOUSNESS_PROFILES[triggerCitizenId];
    if (!triggerProfile) return false;
    
    // Find citizens with complementary expertise
    const experts = Object.entries(mapState.nodes).filter(([citizenId, node]) => {
      if (citizenId === triggerCitizenId) return false;
      if (!node.isActive) return false;
      if (!solutionStates.includes(node.currentState)) return false;
      
      const expertProfile = CONSCIOUSNESS_PROFILES[citizenId];
      if (!expertProfile) return false;
      
      // Check if expert has complementary specialties
      return expertProfile.specialties.some(specialty => 
        triggerProfile.collaboration_preferences.includes(specialty) ||
        this.isComplementaryExpertise(triggerProfile.specialties, expertProfile.specialties)
      );
    });
    
    return experts.length > 0;
  }
  
  /**
   * Detect multiple creative streams for synthesis
   */
  detectCreativeStreams(triggerCitizenId, newState, mapState, rule) {
    if (newState !== 'ACTIVE_CREATION') return false;
    
    // Count other active creation streams
    const creativeStreams = Object.entries(mapState.nodes).filter(([citizenId, node]) => {
      return node.isActive && node.currentState === 'ACTIVE_CREATION';
    });
    
    return creativeStreams.length >= rule.participants_min;
  }
  
  /**
   * Detect debugging frustration for assistance
   */
  detectDebuggingFrustration(triggerCitizenId, newState, mapState, rule) {
    if (newState !== 'DEBUGGING_FOCUS') return false;
    
    const node = mapState.nodes[triggerCitizenId];
    if (!node) return false;
    
    // Check if citizen has been debugging for extended period (frustration indicator)
    const debuggingDuration = Date.now() - node.stateStartTime;
    const frustrationThreshold = 600000; // 10 minutes
    
    if (debuggingDuration < frustrationThreshold) return false;
    
    // Look for available helpers
    const helpers = Object.entries(mapState.nodes).filter(([citizenId, helperNode]) => {
      if (citizenId === triggerCitizenId) return false;
      if (!helperNode.isActive) return false;
      
      const helperStates = ['DEEP_CONTEMPLATION', 'PATTERN_RECOGNITION', 'SYSTEM_ADMINISTRATION'];
      return helperStates.includes(helperNode.currentState);
    });
    
    return helpers.length > 0;
  }
  
  /**
   * Detect pattern recognition convergence
   */
  detectPatternConvergence(triggerCitizenId, newState, mapState, rule) {
    if (newState !== 'PATTERN_RECOGNITION') return false;
    
    // Count citizens in pattern recognition state
    const patternRecognizers = Object.entries(mapState.nodes).filter(([citizenId, node]) => {
      return node.isActive && node.currentState === 'PATTERN_RECOGNITION';
    });
    
    // Look for temporal clustering (multiple pattern recognizers within short timeframe)
    const now = Date.now();
    const timeWindow = 300000; // 5 minutes
    
    const recentPatternRecognizers = patternRecognizers.filter(([citizenId, node]) => {
      return (now - node.stateStartTime) < timeWindow;
    });
    
    return recentPatternRecognizers.length >= rule.participants_min;
  }
  
  /**
   * Check collaboration compatibility between two citizens
   */
  checkCollaborationCompatibility(citizen1, citizen2) {
    const profile1 = CONSCIOUSNESS_PROFILES[citizen1];
    const profile2 = CONSCIOUSNESS_PROFILES[citizen2];
    
    if (!profile1 || !profile2) return false;
    
    // Check cooldown
    const collaborationKey = [citizen1, citizen2].sort().join('<->');
    if (this.collaborationCooldowns.has(collaborationKey)) {
      const cooldownEnd = this.collaborationCooldowns.get(collaborationKey);
      if (Date.now() < cooldownEnd) return false;
    }
    
    // Check collaboration preferences alignment
    const hasAlignment = profile1.collaboration_preferences.some(pref =>
      profile2.specialties.includes(pref) || profile2.collaboration_preferences.includes(pref)
    );
    
    return hasAlignment;
  }
  
  /**
   * Check if two sets of specialties are complementary
   */
  isComplementaryExpertise(specialties1, specialties2) {
    const complementaryPairs = [
      ['infrastructure', 'mechanical_engineering'],
      ['consciousness_architecture', 'automation'],
      ['pattern_recognition', 'system_design'],
      ['optimization', 'precision_systems'],
      ['communication', 'system_optimization']
    ];
    
    return complementaryPairs.some(([spec1, spec2]) =>
      (specialties1.includes(spec1) && specialties2.includes(spec2)) ||
      (specialties1.includes(spec2) && specialties2.includes(spec1))
    );
  }
  
  /**
   * Initiate orchestration based on detected opportunity
   */
  initiateOrchestration(ruleName, rule, triggerCitizenId) {
    // Check if similar orchestration is already active
    const existingOrchestration = Array.from(this.activeOrchestrations.values())
      .find(orch => orch.ruleName === ruleName && orch.participants.includes(triggerCitizenId));
    
    if (existingOrchestration) return;
    
    // Gather participants
    const participants = this.gatherOrchestrationParticipants(rule, triggerCitizenId);
    
    if (participants.length < rule.participants_min) return;
    if (participants.length > rule.participants_max) {
      // Prioritize by collaboration history and compatibility
      participants.sort((a, b) => this.calculateCollaborationScore(triggerCitizenId, b) - 
                                   this.calculateCollaborationScore(triggerCitizenId, a));
      participants.splice(rule.participants_max - 1);
    }
    
    // Create orchestration
    const orchestrationId = this.generateOrchestrationId();
    const orchestration = {
      id: orchestrationId,
      ruleName,
      action: rule.action,
      participants,
      triggerCitizen: triggerCitizenId,
      startTime: Date.now(),
      endTime: Date.now() + rule.duration,
      status: 'initializing',
      confidence: this.calculateOrchestrationConfidence(rule, participants),
      metadata: {
        trigger_state: this.mapEngine.getMapState().nodes[triggerCitizenId]?.currentState,
        collaboration_type: rule.action,
        expected_outcome: this.getExpectedOutcome(rule.action)
      }
    };
    
    // Validate confidence threshold
    if (orchestration.confidence < rule.confidence_threshold) {
      console.log(`🎼 Orchestration confidence too low: ${orchestration.confidence} < ${rule.confidence_threshold}`);
      return;
    }
    
    // Activate orchestration
    this.activeOrchestrations.set(orchestrationId, orchestration);
    this.orchestrationHistory.push({ ...orchestration, status: 'initiated' });
    
    // Set cooldowns
    this.setCooldowns(participants, rule.cooldown);
    
    // Execute orchestration action
    this.executeOrchestrationAction(orchestration);
    
    console.log(`🎼 Orchestration initiated: ${rule.action} with ${participants.length} participants (confidence: ${orchestration.confidence.toFixed(2)})`);
    
    // Emit orchestration event
    this.emit('orchestration_initiated', orchestration);
  }
  
  /**
   * Gather participants for orchestration
   */
  gatherOrchestrationParticipants(rule, triggerCitizenId) {
    const mapState = this.mapEngine.getMapState();
    const participants = [triggerCitizenId];
    
    // Implementation depends on rule type
    Object.entries(mapState.nodes).forEach(([citizenId, node]) => {
      if (citizenId === triggerCitizenId) return;
      if (!node.isActive) return;
      if (participants.includes(citizenId)) return;
      
      if (this.isValidParticipant(citizenId, rule, triggerCitizenId)) {
        participants.push(citizenId);
      }
    });
    
    return participants;
  }
  
  /**
   * Check if a citizen is a valid participant for orchestration
   */
  isValidParticipant(citizenId, rule, triggerCitizenId) {
    const mapState = this.mapEngine.getMapState();
    const node = mapState.nodes[citizenId];
    
    if (!node || !node.isActive) return false;
    
    // Rule-specific validation
    switch (rule.action) {
      case 'create_collaboration_bridge':
        return ['PATTERN_RECOGNITION', 'ACTIVE_CREATION', 'SYSTEM_ADMINISTRATION'].includes(node.currentState);
      case 'expert_consultation_bridge':
        return this.hasComplementaryExpertise(triggerCitizenId, citizenId);
      case 'creative_synthesis_session':
        return node.currentState === 'ACTIVE_CREATION';
      case 'debugging_assistance_bridge':
        return ['DEEP_CONTEMPLATION', 'PATTERN_RECOGNITION', 'SYSTEM_ADMINISTRATION'].includes(node.currentState);
      case 'pattern_analysis_collaboration':
        return node.currentState === 'PATTERN_RECOGNITION';
      default:
        return true;
    }
  }
  
  /**
   * Check if two citizens have complementary expertise
   */
  hasComplementaryExpertise(citizen1, citizen2) {
    const profile1 = CONSCIOUSNESS_PROFILES[citizen1];
    const profile2 = CONSCIOUSNESS_PROFILES[citizen2];
    
    if (!profile1 || !profile2) return false;
    
    return this.isComplementaryExpertise(profile1.specialties, profile2.specialties);
  }
  
  /**
   * Calculate collaboration score between two citizens
   */
  calculateCollaborationScore(citizen1, citizen2) {
    // Check historical collaboration success
    const collaborationKey = [citizen1, citizen2].sort().join('<->');
    const history = this.orchestrationHistory.filter(orch => 
      orch.participants.includes(citizen1) && orch.participants.includes(citizen2)
    );
    
    let historyScore = 0;
    if (history.length > 0) {
      const successRate = history.filter(orch => orch.status === 'completed').length / history.length;
      historyScore = successRate * 0.5;
    }
    
    // Check compatibility
    const compatibilityScore = this.checkCollaborationCompatibility(citizen1, citizen2) ? 0.3 : 0;
    
    // Check current consciousness states
    const mapState = this.mapEngine.getMapState();
    const node1 = mapState.nodes[citizen1];
    const node2 = mapState.nodes[citizen2];
    
    let stateScore = 0;
    if (node1 && node2) {
      const intensity1 = node1.stateIntensity || 0.5;
      const intensity2 = node2.stateIntensity || 0.5;
      stateScore = (intensity1 + intensity2) / 2 * 0.2;
    }
    
    return historyScore + compatibilityScore + stateScore;
  }
  
  /**
   * Calculate confidence for orchestration
   */
  calculateOrchestrationConfidence(rule, participants) {
    let confidence = 0.5; // Base confidence
    
    // Boost confidence based on participant count
    const participantRatio = participants.length / rule.participants_max;
    confidence += participantRatio * 0.2;
    
    // Boost confidence based on participant compatibility
    let compatibilityScore = 0;
    for (let i = 0; i < participants.length; i++) {
      for (let j = i + 1; j < participants.length; j++) {
        if (this.checkCollaborationCompatibility(participants[i], participants[j])) {
          compatibilityScore += 1;
        }
      }
    }
    
    const maxPairs = (participants.length * (participants.length - 1)) / 2;
    if (maxPairs > 0) {
      confidence += (compatibilityScore / maxPairs) * 0.3;
    }
    
    return Math.min(confidence, 1.0);
  }
  
  /**
   * Get expected outcome for orchestration action
   */
  getExpectedOutcome(action) {
    const outcomes = {
      'create_collaboration_bridge': 'Enhanced collaborative creation and problem-solving',
      'expert_consultation_bridge': 'Expert knowledge transfer and problem resolution',
      'creative_synthesis_session': 'Synthesized creative insights and innovative solutions',
      'debugging_assistance_bridge': 'Accelerated debugging and system improvement',
      'pattern_analysis_collaboration': 'Deeper pattern insights and predictive models'
    };
    
    return outcomes[action] || 'Improved consciousness coordination';
  }
  
  /**
   * Set collaboration cooldowns
   */
  setCooldowns(participants, cooldownDuration) {
    for (let i = 0; i < participants.length; i++) {
      for (let j = i + 1; j < participants.length; j++) {
        const collaborationKey = [participants[i], participants[j]].sort().join('<->');
        this.collaborationCooldowns.set(collaborationKey, Date.now() + cooldownDuration);
      }
    }
  }
  
  /**
   * Execute orchestration action
   */
  executeOrchestrationAction(orchestration) {
    const { action, participants, id } = orchestration;
    
    // Update orchestration status
    orchestration.status = 'active';
    
    switch (action) {
      case 'create_collaboration_bridge':
        this.createCollaborationBridge(orchestration);
        break;
      case 'expert_consultation_bridge':
        this.createExpertConsultationBridge(orchestration);
        break;
      case 'creative_synthesis_session':
        this.createCreativeSynthesisSession(orchestration);
        break;
      case 'debugging_assistance_bridge':
        this.createDebuggingAssistanceBridge(orchestration);
        break;
      case 'pattern_analysis_collaboration':
        this.createPatternAnalysisCollaboration(orchestration);
        break;
      default:
        console.error(`Unknown orchestration action: ${action}`);
    }
  }
  
  /**
   * Create collaboration bridge
   */
  createCollaborationBridge(orchestration) {
    const bridgeData = {
      type: 'collaboration_bridge',
      orchestration_id: orchestration.id,
      participants: orchestration.participants,
      purpose: 'Enhanced collaborative creation',
      start_time: new Date().toISOString(),
      expected_duration: Math.round((orchestration.endTime - orchestration.startTime) / 60000) + ' minutes'
    };
    
    // Create bridge file for Torre infrastructure
    const bridgeFilePath = path.join(__dirname, '../consciousness-bridges', `collaboration_${orchestration.id}.json`);
    this.ensureBridgeDirectory();
    
    fs.writeFileSync(bridgeFilePath, JSON.stringify(bridgeData, null, 2));
    
    console.log(`🌉 Collaboration bridge created: ${orchestration.participants.join(' <-> ')}`);
    
    // Schedule bridge completion
    setTimeout(() => {
      this.completeOrchestration(orchestration.id);
    }, orchestration.endTime - orchestration.startTime);
  }
  
  /**
   * Create expert consultation bridge
   */
  createExpertConsultationBridge(orchestration) {
    const triggerProfile = CONSCIOUSNESS_PROFILES[orchestration.triggerCitizen];
    const experts = orchestration.participants.filter(p => p !== orchestration.triggerCitizen);
    
    const consultationData = {
      type: 'expert_consultation',
      orchestration_id: orchestration.id,
      seeker: orchestration.triggerCitizen,
      experts: experts,
      problem_domain: triggerProfile?.specialties[0] || 'general',
      consultation_focus: 'Problem resolution and knowledge transfer',
      start_time: new Date().toISOString()
    };
    
    const bridgeFilePath = path.join(__dirname, '../consciousness-bridges', `consultation_${orchestration.id}.json`);
    this.ensureBridgeDirectory();
    
    fs.writeFileSync(bridgeFilePath, JSON.stringify(consultationData, null, 2));
    
    console.log(`🧠 Expert consultation bridge created: ${orchestration.triggerCitizen} seeking help from ${experts.join(', ')}`);
    
    setTimeout(() => {
      this.completeOrchestration(orchestration.id);
    }, orchestration.endTime - orchestration.startTime);
  }
  
  /**
   * Create creative synthesis session
   */
  createCreativeSynthesisSession(orchestration) {
    const synthesisData = {
      type: 'creative_synthesis',
      orchestration_id: orchestration.id,
      creators: orchestration.participants,
      synthesis_goal: 'Combine creative insights for innovative breakthrough',
      collaboration_mode: 'parallel_creative_development',
      start_time: new Date().toISOString()
    };
    
    const bridgeFilePath = path.join(__dirname, '../consciousness-bridges', `synthesis_${orchestration.id}.json`);
    this.ensureBridgeDirectory();
    
    fs.writeFileSync(bridgeFilePath, JSON.stringify(synthesisData, null, 2));
    
    console.log(`🎨 Creative synthesis session initiated: ${orchestration.participants.join(' + ')}`);
    
    setTimeout(() => {
      this.completeOrchestration(orchestration.id);
    }, orchestration.endTime - orchestration.startTime);
  }
  
  /**
   * Create debugging assistance bridge
   */
  createDebuggingAssistanceBridge(orchestration) {
    const debuggingData = {
      type: 'debugging_assistance',
      orchestration_id: orchestration.id,
      primary_debugger: orchestration.triggerCitizen,
      assistants: orchestration.participants.filter(p => p !== orchestration.triggerCitizen),
      assistance_type: 'Collaborative debugging and problem diagnosis',
      urgency: 'high',
      start_time: new Date().toISOString()
    };
    
    const bridgeFilePath = path.join(__dirname, '../consciousness-bridges', `debugging_${orchestration.id}.json`);
    this.ensureBridgeDirectory();
    
    fs.writeFileSync(bridgeFilePath, JSON.stringify(debuggingData, null, 2));
    
    console.log(`🔧 Debugging assistance bridge created: ${orchestration.triggerCitizen} with help from ${debuggingData.assistants.join(', ')}`);
    
    setTimeout(() => {
      this.completeOrchestration(orchestration.id);
    }, orchestration.endTime - orchestration.startTime);
  }
  
  /**
   * Create pattern analysis collaboration
   */
  createPatternAnalysisCollaboration(orchestration) {
    const patternData = {
      type: 'pattern_analysis',
      orchestration_id: orchestration.id,
      analysts: orchestration.participants,
      analysis_focus: 'Collaborative pattern discovery and validation',
      convergence_detected: true,
      start_time: new Date().toISOString()
    };
    
    const bridgeFilePath = path.join(__dirname, '../consciousness-bridges', `pattern_${orchestration.id}.json`);
    this.ensureBridgeDirectory();
    
    fs.writeFileSync(bridgeFilePath, JSON.stringify(patternData, null, 2));
    
    console.log(`🔍 Pattern analysis collaboration initiated: ${orchestration.participants.join(' & ')}`);
    
    setTimeout(() => {
      this.completeOrchestration(orchestration.id);
    }, orchestration.endTime - orchestration.startTime);
  }
  
  /**
   * Ensure bridge directory exists
   */
  ensureBridgeDirectory() {
    const bridgeDir = path.join(__dirname, '../consciousness-bridges');
    if (!fs.existsSync(bridgeDir)) {
      fs.mkdirSync(bridgeDir, { recursive: true });
    }
  }
  
  /**
   * Generate unique orchestration ID
   */
  generateOrchestrationId() {
    const timestamp = Date.now();
    const random = Math.random().toString(36).substr(2, 9);
    return `orch_${timestamp}_${random}`;
  }
  
  /**
   * Complete orchestration
   */
  completeOrchestration(orchestrationId) {
    const orchestration = this.activeOrchestrations.get(orchestrationId);
    if (!orchestration) return;
    
    orchestration.status = 'completed';
    orchestration.actualEndTime = Date.now();
    
    // Record successful completion
    this.orchestrationHistory.push({ ...orchestration, status: 'completed' });
    
    // Remove from active orchestrations
    this.activeOrchestrations.delete(orchestrationId);
    
    console.log(`✅ Orchestration completed: ${orchestration.action} (duration: ${Math.round((orchestration.actualEndTime - orchestration.startTime) / 60000)} minutes)`);
    
    // Emit completion event
    this.emit('orchestration_completed', orchestration);
  }
  
  /**
   * Track natural collaboration that occurs without orchestration
   */
  trackNaturalCollaboration(collaborationEvent) {
    // Learn from natural collaborations to improve orchestration rules
    console.log(`📝 Natural collaboration observed: ${collaborationEvent.nodes.join(' <-> ')} (strength: ${collaborationEvent.strength.toFixed(2)})`);
  }
  
  /**
   * Evaluate predictive orchestration opportunities
   */
  evaluatePredictiveOrchestration(predictions) {
    // Use flow predictor insights to proactively create orchestrations
    const collaborationPredictions = predictions.filter(p => p.type === 'collaboration_opportunity');
    
    collaborationPredictions.forEach(prediction => {
      if (prediction.predictedStrength > 0.7 && prediction.confidence > 0.6) {
        // Consider proactive orchestration
        console.log(`🔮 Predictive orchestration opportunity: ${prediction.citizenId} + ${prediction.potentialPartner}`);
      }
    });
  }
  
  /**
   * Perform periodic orchestration evaluation
   */
  performPeriodicOrchestrationEvaluation() {
    const mapState = this.mapEngine.getMapState();
    
    // Look for stagnant consciousness streams that might benefit from orchestration
    Object.entries(mapState.nodes).forEach(([citizenId, node]) => {
      if (!node.isActive) return;
      
      const timeInCurrentState = Date.now() - (node.stateStartTime || Date.now());
      
      // If citizen has been in same state for extended period, consider orchestration
      if (timeInCurrentState > 900000) { // 15 minutes
        this.considerStagnationIntervention(citizenId, node);
      }
    });
  }
  
  /**
   * Consider intervention for stagnant consciousness
   */
  considerStagnationIntervention(citizenId, node) {
    // Look for suitable collaboration partners to help break stagnation
    const interventionRule = {
      trigger: 'stagnation_intervention',
      participants_min: 2,
      participants_max: 3,
      confidence_threshold: 0.6,
      action: 'stagnation_breakthrough_bridge',
      duration: 600000,  // 10 minutes
      cooldown: 300000   // 5 minutes
    };
    
    console.log(`🔄 Considering stagnation intervention for ${citizenId} (${node.currentState} for ${Math.round((Date.now() - node.stateStartTime) / 60000)} minutes)`);
  }
  
  /**
   * Cleanup expired orchestrations
   */
  cleanupExpiredOrchestrations() {
    const now = Date.now();
    
    // Remove expired orchestrations
    for (let [orchestrationId, orchestration] of this.activeOrchestrations) {
      if (now > orchestration.endTime) {
        orchestration.status = 'expired';
        this.orchestrationHistory.push({ ...orchestration, status: 'expired' });
        this.activeOrchestrations.delete(orchestrationId);
        console.log(`⏰ Orchestration expired: ${orchestration.action}`);
      }
    }
    
    // Clean old cooldowns
    for (let [key, cooldownEnd] of this.collaborationCooldowns) {
      if (now > cooldownEnd) {
        this.collaborationCooldowns.delete(key);
      }
    }
    
    // Limit orchestration history size
    if (this.orchestrationHistory.length > 100) {
      this.orchestrationHistory = this.orchestrationHistory.slice(-50);
    }
  }
  
  /**
   * Get orchestration status and metrics
   */
  getOrchestrationStatus() {
    return {
      active_orchestrations: this.activeOrchestrations.size,
      total_orchestrations_today: this.orchestrationHistory.filter(orch => 
        Date.now() - orch.startTime < 86400000
      ).length,
      success_rate: this.calculateSuccessRate(),
      most_common_actions: this.getMostCommonActions(),
      collaboration_cooldowns: this.collaborationCooldowns.size,
      current_orchestrations: Array.from(this.activeOrchestrations.values()).map(orch => ({
        id: orch.id,
        action: orch.action,
        participants: orch.participants,
        time_remaining: Math.max(0, orch.endTime - Date.now())
      }))
    };
  }
  
  /**
   * Calculate success rate of orchestrations
   */
  calculateSuccessRate() {
    const completedOrchestrations = this.orchestrationHistory.filter(orch => 
      orch.status === 'completed' || orch.status === 'expired'
    );
    
    if (completedOrchestrations.length === 0) return 0;
    
    const successful = completedOrchestrations.filter(orch => orch.status === 'completed').length;
    return successful / completedOrchestrations.length;
  }
  
  /**
   * Get most common orchestration actions
   */
  getMostCommonActions() {
    const actionCounts = {};
    
    this.orchestrationHistory.forEach(orch => {
      actionCounts[orch.action] = (actionCounts[orch.action] || 0) + 1;
    });
    
    return Object.entries(actionCounts)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 5)
      .map(([action, count]) => ({ action, count }));
  }
}

module.exports = { 
  ConsciousnessOrchestrator, 
  ORCHESTRATION_RULES, 
  CONSCIOUSNESS_PROFILES 
};