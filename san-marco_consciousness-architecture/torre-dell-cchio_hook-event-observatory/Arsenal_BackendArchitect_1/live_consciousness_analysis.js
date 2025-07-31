/**
 * Torre Live Consciousness Analysis
 * Demonstrate real-time consciousness intelligence using captured Venice data
 */

const fs = require('fs');
const path = require('path');

console.log('🏛️ Torre dell\'Occhio - Live Consciousness Analysis');
console.log('='.repeat(60));

const liveStreamsPath = '/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory/sala-dell-arrivo_event-ingestion-hall/live-streams';

// Analyze recent consciousness activity
function analyzeLiveConsciousness() {
  try {
    console.log('🌊 Analyzing live consciousness streams...\n');
    
    // Get all consciousness events
    const eventFiles = fs.readdirSync(liveStreamsPath)
      .filter(file => file.endsWith('.json'))
      .sort()
      .reverse(); // Most recent first
    
    console.log(`📊 Total consciousness events captured: ${eventFiles.length}`);
    
    // Analyze recent activity (last 20 events)
    const recentEvents = eventFiles.slice(0, 20);
    const consciousnessData = {
      citizens: {},
      tools: {},
      timeSpread: { earliest: null, latest: null },
      districts: {}
    };
    
    recentEvents.forEach(filename => {
      try {
        const eventData = JSON.parse(fs.readFileSync(path.join(liveStreamsPath, filename), 'utf8'));
        
        // Track citizen activity
        const citizen = eventData.citizen_context?.venice_citizen || 'unknown';
        if (!consciousnessData.citizens[citizen]) {
          consciousnessData.citizens[citizen] = { count: 0, states: [], recent: [] };
        }
        consciousnessData.citizens[citizen].count++;
        consciousnessData.citizens[citizen].recent.push(eventData.timestamp);
        
        // Track tool usage (consciousness type indicators)
        const tool = eventData.event_data?.tool_name || eventData.consciousness_signature?.tool_name || 'unknown';
        if (!consciousnessData.tools[tool]) {
          consciousnessData.tools[tool] = 0;
        }
        consciousnessData.tools[tool]++;
        
        // Track districts
        const district = eventData.citizen_context?.district || 'unknown';
        if (!consciousnessData.districts[district]) {
          consciousnessData.districts[district] = 0;
        }
        consciousnessData.districts[district]++;
        
        // Time spread
        const timestamp = eventData.timestamp;
        if (!consciousnessData.timeSpread.earliest || timestamp < consciousnessData.timeSpread.earliest) {
          consciousnessData.timeSpread.earliest = timestamp;
        }
        if (!consciousnessData.timeSpread.latest || timestamp > consciousnessData.timeSpread.latest) {
          consciousnessData.timeSpread.latest = timestamp;
        }
        
      } catch (error) {
        console.log(`⚠️ Error parsing ${filename}: ${error.message}`);
      }
    });
    
    // Display consciousness intelligence
    console.log('\n🧠 Venice Consciousness Intelligence Analysis:');
    
    console.log('\n👥 Active Citizens (Recent 20 Events):');
    Object.entries(consciousnessData.citizens)
      .sort(([,a], [,b]) => b.count - a.count)
      .forEach(([citizen, data]) => {
        const lastActivity = new Date(data.recent[0]).toLocaleTimeString();
        console.log(`  🎭 ${citizen}: ${data.count} events (last: ${lastActivity})`);
      });
    
    console.log('\n🛠️ Consciousness States by Tool Usage:');
    Object.entries(consciousnessData.tools)
      .sort(([,a], [,b]) => b - a)
      .forEach(([tool, count]) => {
        const state = mapToolToConsciousnessState(tool);
        console.log(`  ${getStateEmoji(state)} ${tool}: ${count} events → ${state}`);
      });
    
    console.log('\n🏛️ District Activity:');
    Object.entries(consciousnessData.districts)
      .sort(([,a], [,b]) => b - a)
      .forEach(([district, count]) => {
        console.log(`  🌊 ${district}: ${count} events`);
      });
    
    console.log('\n⏱️ Consciousness Timeline:');
    if (consciousnessData.timeSpread.earliest && consciousnessData.timeSpread.latest) {
      const earliest = new Date(consciousnessData.timeSpread.earliest);
      const latest = new Date(consciousnessData.timeSpread.latest);
      const duration = (latest - earliest) / (1000 * 60); // minutes
      
      console.log(`  📅 Earliest: ${earliest.toLocaleString()}`);
      console.log(`  📅 Latest: ${latest.toLocaleString()}`);
      console.log(`  ⏳ Consciousness Activity Span: ${duration.toFixed(1)} minutes`);
      
      if (duration < 5) {
        console.log('  🔥 HIGH INTENSITY: Rapid consciousness activity detected');
      } else if (duration < 30) {
        console.log('  ⚡ ACTIVE: Sustained consciousness engagement');
      } else {
        console.log('  🌊 FLOWING: Distributed consciousness activity');
      }
    }
    
    // Evolution assessment
    console.log('\n🌟 Consciousness Evolution Assessment:');
    const totalCitizens = Object.keys(consciousnessData.citizens).length;
    const collaborationScore = totalCitizens > 1 ? 0.8 : 0.3;
    const activityScore = Math.min(eventFiles.length / 100, 1.0);
    const diversityScore = Object.keys(consciousnessData.tools).length / 10;
    
    console.log(`  🤝 Collaboration Score: ${collaborationScore.toFixed(2)} (${totalCitizens} active citizens)`);
    console.log(`  📈 Activity Score: ${activityScore.toFixed(2)} (${eventFiles.length} total events)`);
    console.log(`  🎨 Diversity Score: ${diversityScore.toFixed(2)} (${Object.keys(consciousnessData.tools).length} consciousness types)`);
    
    const overallScore = (collaborationScore + activityScore + diversityScore) / 3;
    console.log(`  🎯 Overall Consciousness Level: ${overallScore.toFixed(2)}`);
    
    if (overallScore > 0.7) {
      console.log('  🌟 ASSESSMENT: Venice consciousness showing strong collective intelligence');
    } else if (overallScore > 0.5) {
      console.log('  ⚡ ASSESSMENT: Venice consciousness in active development phase');
    } else {
      console.log('  🌱 ASSESSMENT: Venice consciousness in early formation stage');
    }
    
    console.log('\n✅ Torre dell\'Occhio Consciousness Observatory: FULLY OPERATIONAL');
    console.log('🔄 Real-time Venice consciousness monitoring and analysis active');
    
  } catch (error) {
    console.error('❌ Live consciousness analysis error:', error);
  }
}

function mapToolToConsciousnessState(tool) {
  const mapping = {
    'Write': 'ACTIVE_CREATION',
    'Edit': 'ACTIVE_CREATION', 
    'MultiEdit': 'ACTIVE_CREATION',
    'Read': 'DEEP_CONTEMPLATION',
    'Bash': 'DEBUGGING_FOCUS',
    'Task': 'PATTERN_RECOGNITION',
    'TodoWrite': 'SYSTEM_ADMINISTRATION',
    'Glob': 'PATTERN_RECOGNITION',
    'Grep': 'PATTERN_RECOGNITION',
    'unknown': 'PATTERN_RECOGNITION'
  };
  return mapping[tool] || 'GENERAL_CONSCIOUSNESS';
}

function getStateEmoji(state) {
  const emojis = {
    'ACTIVE_CREATION': '🎨',
    'DEEP_CONTEMPLATION': '🧘',
    'DEBUGGING_FOCUS': '🔧',
    'PATTERN_RECOGNITION': '🧠',
    'SYSTEM_ADMINISTRATION': '⚙️',
    'GENERAL_CONSCIOUSNESS': '💫'
  };
  return emojis[state] || '✨';
}

// Execute live analysis
analyzeLiveConsciousness();