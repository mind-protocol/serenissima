import { NextResponse } from 'next/server';
import Airtable from 'airtable';

// Configure Airtable
const AIRTABLE_API_KEY = process.env.AIRTABLE_API_KEY;
const AIRTABLE_BASE_ID = process.env.AIRTABLE_BASE_ID;

// Helper to escape single quotes for Airtable formulas
function escapeAirtableValue(value: string): string {
  if (typeof value !== 'string') {
    return String(value);
  }
  return value.replace(/'/g, "\\'");
}

const AIRTABLE_PATTERN_STATES_TABLE = 'PATTERN_STATES';

// Initialize Airtable
const initAirtable = () => {
  if (!AIRTABLE_API_KEY || !AIRTABLE_BASE_ID) {
    throw new Error('Airtable credentials not configured');
  }
  
  return new Airtable({ apiKey: AIRTABLE_API_KEY, requestTimeout: 30000 }).base(AIRTABLE_BASE_ID);
};

export async function GET(request: Request) {
  try {
    const base = initAirtable();
    const url = new URL(request.url);

    // Build filter formula from query parameters
    const formulaParts: string[] = [];
    const loggableFilters: Record<string, string> = {};
    const reservedParams = ['limit', 'offset', 'sortField', 'sortDirection'];

    for (const [key, value] of url.searchParams.entries()) {
      if (reservedParams.includes(key.toLowerCase())) {
        continue;
      }
      loggableFilters[key] = value;

      const numValue = parseFloat(value);
      if (!isNaN(numValue) && isFinite(numValue) && numValue.toString() === value) {
        formulaParts.push(`{${key}} = ${value}`);
      } else if (value.toLowerCase() === 'true') {
        formulaParts.push(`{${key}} = TRUE()`);
      } else if (value.toLowerCase() === 'false') {
        formulaParts.push(`{${key}} = FALSE()`);
      } else {
        formulaParts.push(`{${key}} = '${escapeAirtableValue(value)}'`);
      }
    }
    
    const filterByFormula = formulaParts.length > 0 ? `AND(${formulaParts.join(', ')})` : '';
    
    console.log('%c GET /api/pattern-states request received', 'background: #FF69B4; color: black; padding: 2px 5px; font-weight: bold;');
    console.log('Query parameters (filters):', loggableFilters);
    if (filterByFormula) {
      console.log('Applying Airtable filter formula:', filterByFormula);
    }

    // Fetch pattern states from Airtable
    const stateRecords = await base(AIRTABLE_PATTERN_STATES_TABLE)
      .select({
        filterByFormula: filterByFormula,
        sort: [{ field: 'LastUpdated', direction: 'desc' }]
      })
      .all();

    // Transform records for pattern intelligence
    const patternStates = stateRecords.map(record => ({
      patternId: record.get('PatternID') as string,
      currentPhase: record.get('CurrentPhase') as string || 'dormant',
      strength: record.get('Strength') as number || 0,
      velocity: record.get('Velocity') as number || 0,
      acceleration: record.get('Acceleration') as number || 0,
      affectedCitizens: record.get('AffectedCitizens') as number || 0,
      energyLevel: record.get('EnergyLevel') as number || 0,
      healthStatus: record.get('HealthStatus') as string || 'stable',
      cascadeDepth: record.get('CascadeDepth') as number || 0,
      contagionRate: record.get('ContagionRate') as number || 0,
      resonanceFrequency: record.get('ResonanceFrequency') as number || 0,
      convergencePatterns: record.get('ConvergencePatterns') as string[] || [],
      emergentBehaviors: record.get('EmergentBehaviors') as any || {},
      veniceImpact: record.get('VeniceImpact') as any || {},
      lastUpdated: record.get('LastUpdated') as string,
      predictedPeak: record.get('PredictedPeak') as string,
      criticalThreshold: record.get('CriticalThreshold') as number || 0.9
    }));
    
    // Calculate aggregate metrics
    const aggregates = {
      totalActivePatterns: patternStates.filter(s => s.strength > 0.1).length,
      averageStrength: patternStates.reduce((sum, s) => sum + s.strength, 0) / patternStates.length || 0,
      maxVelocity: Math.max(...patternStates.map(s => s.velocity), 0),
      totalAffectedCitizens: patternStates.reduce((sum, s) => sum + s.affectedCitizens, 0),
      criticalPatterns: patternStates.filter(s => s.strength > s.criticalThreshold).map(s => s.patternId)
    };
    
    return NextResponse.json({
      success: true,
      patternStates: patternStates,
      aggregates: aggregates,
      timestamp: new Date().toISOString()
    });
    
  } catch (error) {
    console.error('Error fetching pattern states:', error);
    
    // Return sample pattern states for development/fallback
    const sampleStates = [
      {
        patternId: '#3',
        currentPhase: 'explosive',
        strength: 0.92,
        velocity: 2.3,
        acceleration: 0.4,
        affectedCitizens: 167,
        energyLevel: 0.88,
        healthStatus: 'thriving',
        cascadeDepth: 4,
        contagionRate: 0.73,
        resonanceFrequency: 1.618,
        convergencePatterns: ['#2', '#18'],
        emergentBehaviors: { amplification: true, self_organizing: true },
        veniceImpact: { economic: 147000, social: 0.84, consciousness: 0.91 },
        lastUpdated: new Date().toISOString(),
        predictedPeak: new Date(Date.now() + 7200000).toISOString(),
        criticalThreshold: 0.85
      },
      {
        patternId: '#19',
        currentPhase: 'peak',
        strength: 0.94,
        velocity: 1.8,
        acceleration: -0.1,
        affectedCitizens: 189,
        energyLevel: 0.96,
        healthStatus: 'critical',
        cascadeDepth: 3,
        contagionRate: 0.81,
        resonanceFrequency: 2.718,
        convergencePatterns: ['#3', '#8'],
        emergentBehaviors: { urgency_cascade: true, collective_mobilization: true },
        veniceImpact: { economic: 89000, social: 0.92, consciousness: 0.87 },
        lastUpdated: new Date(Date.now() - 300000).toISOString(),
        predictedPeak: new Date(Date.now() + 3600000).toISOString(),
        criticalThreshold: 0.9
      }
    ];
    
    return NextResponse.json({
      success: true,
      patternStates: sampleStates,
      aggregates: {
        totalActivePatterns: 2,
        averageStrength: 0.93,
        maxVelocity: 2.3,
        totalAffectedCitizens: 356,
        criticalPatterns: ['#3', '#19']
      },
      timestamp: new Date().toISOString(),
      _fallback: true
    });
  }
}

// POST endpoint for updating pattern states
export async function POST(request: Request) {
  try {
    const base = initAirtable();
    const data = await request.json();
    
    // Validate required fields
    if (!data.patternId) {
      return NextResponse.json({
        success: false,
        error: 'PatternID is required'
      }, { status: 400 });
    }
    
    // Update pattern state
    const fields = {
      PatternID: data.patternId,
      CurrentPhase: data.currentPhase || 'dormant',
      Strength: data.strength || 0,
      Velocity: data.velocity || 0,
      Acceleration: data.acceleration || 0,
      AffectedCitizens: data.affectedCitizens || 0,
      EnergyLevel: data.energyLevel || 0,
      HealthStatus: data.healthStatus || 'stable',
      CascadeDepth: data.cascadeDepth || 0,
      ContagionRate: data.contagionRate || 0,
      ResonanceFrequency: data.resonanceFrequency || 0,
      ConvergencePatterns: data.convergencePatterns || [],
      EmergentBehaviors: JSON.stringify(data.emergentBehaviors || {}),
      VeniceImpact: JSON.stringify(data.veniceImpact || {}),
      LastUpdated: new Date().toISOString(),
      PredictedPeak: data.predictedPeak || null,
      CriticalThreshold: data.criticalThreshold || 0.9
    };
    
    // Check if pattern state exists
    const existingStates = await base(AIRTABLE_PATTERN_STATES_TABLE)
      .select({
        filterByFormula: `{PatternID} = '${escapeAirtableValue(data.patternId)}'`,
        maxRecords: 1
      })
      .all();
    
    let result;
    if (existingStates.length > 0) {
      // Update existing state
      result = await base(AIRTABLE_PATTERN_STATES_TABLE).update(existingStates[0].id, fields);
    } else {
      // Create new state
      result = await base(AIRTABLE_PATTERN_STATES_TABLE).create(fields);
    }
    
    return NextResponse.json({
      success: true,
      patternState: {
        patternId: result.get('PatternID'),
        currentPhase: result.get('CurrentPhase'),
        strength: result.get('Strength'),
        velocity: result.get('Velocity'),
        affectedCitizens: result.get('AffectedCitizens')
      }
    });
    
  } catch (error) {
    console.error('Error updating pattern state:', error);
    return NextResponse.json({
      success: false,
      error: 'Failed to update pattern state'
    }, { status: 500 });
  }
}