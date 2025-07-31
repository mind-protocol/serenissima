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

const AIRTABLE_PATTERNS_TABLE = 'PATTERNS';

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
    
    console.log('%c GET /api/patterns request received', 'background: #FFD700; color: black; padding: 2px 5px; font-weight: bold;');
    console.log('Query parameters (filters):', loggableFilters);
    if (filterByFormula) {
      console.log('Applying Airtable filter formula:', filterByFormula);
    }

    // Fetch patterns from Airtable
    const patternRecords = await base(AIRTABLE_PATTERNS_TABLE)
      .select({
        filterByFormula: filterByFormula,
        sort: [{ field: 'PatternID', direction: 'asc' }]
      })
      .all();

    // Transform records for pattern intelligence
    const patterns = patternRecords.map(record => ({
      id: record.get('PatternID') as string,
      emoji: record.get('PatternEmoji') as string || '🔮',
      name: record.get('PatternName') as string,
      type: record.get('PatternType') as string,
      description: record.get('PatternDescription') as string,
      crystallization: record.get('PatternCrystallization') as string || 'Fluid',
      instances: record.get('InstanceCount') as number || 0,
      lastActive: record.get('LastActiveAt') as string,
      veniceCalibration: record.get('VeniceCalibration') as any || {},
      metaProperties: record.get('MetaProperties') as any || {},
      createdAt: record.get('CreatedAt') as string,
      updatedAt: record.get('UpdatedAt') as string
    }));
    
    return NextResponse.json({
      success: true,
      patterns: patterns,
      totalCount: patterns.length
    });
    
  } catch (error) {
    console.error('Error fetching patterns:', error);
    
    // Return sample patterns for development/fallback
    const samplePatterns = [
      {
        id: '#1',
        emoji: '🌀',
        name: 'vortex',
        type: 'Process',
        description: 'The fundamental pattern of energy circulation and transformation',
        crystallization: 'Eternal',
        instances: 1247,
        lastActive: new Date().toISOString(),
        veniceCalibration: { strength: 0.87, velocity: 1.2 },
        metaProperties: { self_reinforcing: true, cascade_potential: 0.95 }
      },
      {
        id: '#2',
        emoji: '🌉',
        name: 'bridge',
        type: 'Process',
        description: 'Connection pattern between disparate elements or realities',
        crystallization: 'Crystallizing',
        instances: 892,
        lastActive: new Date(Date.now() - 3600000).toISOString(),
        veniceCalibration: { strength: 0.92, velocity: 0.8 },
        metaProperties: { bidirectional: true, value_transfer: 0.88 }
      },
      {
        id: '#3',
        emoji: '💫',
        name: 'cascade',
        type: 'Process',
        description: 'Amplifying propagation through networked consciousness',
        crystallization: 'Fluid',
        instances: 3421,
        lastActive: new Date(Date.now() - 600000).toISOString(),
        veniceCalibration: { strength: 0.94, velocity: 2.1 },
        metaProperties: { contagion_rate: 0.73, depth: 4 }
      }
    ];
    
    return NextResponse.json({
      success: true,
      patterns: samplePatterns,
      totalCount: samplePatterns.length,
      _fallback: true
    });
  }
}

// POST endpoint for pattern creation/updates
export async function POST(request: Request) {
  try {
    const base = initAirtable();
    const data = await request.json();
    
    // Validate required fields
    if (!data.patternId || !data.patternName) {
      return NextResponse.json({
        success: false,
        error: 'PatternID and PatternName are required'
      }, { status: 400 });
    }
    
    // Create or update pattern
    const fields = {
      PatternID: data.patternId,
      PatternName: data.patternName,
      PatternEmoji: data.patternEmoji || '🔮',
      PatternType: data.patternType || 'Process',
      PatternDescription: data.patternDescription,
      PatternCrystallization: data.patternCrystallization || 'Fluid',
      InstanceCount: data.instanceCount || 0,
      LastActiveAt: new Date().toISOString(),
      VeniceCalibration: JSON.stringify(data.veniceCalibration || {}),
      MetaProperties: JSON.stringify(data.metaProperties || {}),
      UpdatedAt: new Date().toISOString()
    };
    
    // Check if pattern exists
    const existingPatterns = await base(AIRTABLE_PATTERNS_TABLE)
      .select({
        filterByFormula: `{PatternID} = '${escapeAirtableValue(data.patternId)}'`,
        maxRecords: 1
      })
      .all();
    
    let result;
    if (existingPatterns.length > 0) {
      // Update existing pattern
      result = await base(AIRTABLE_PATTERNS_TABLE).update(existingPatterns[0].id, fields);
    } else {
      // Create new pattern
      fields['CreatedAt'] = new Date().toISOString();
      result = await base(AIRTABLE_PATTERNS_TABLE).create(fields);
    }
    
    return NextResponse.json({
      success: true,
      pattern: {
        id: result.get('PatternID'),
        name: result.get('PatternName'),
        emoji: result.get('PatternEmoji'),
        type: result.get('PatternType'),
        crystallization: result.get('PatternCrystallization')
      }
    });
    
  } catch (error) {
    console.error('Error creating/updating pattern:', error);
    return NextResponse.json({
      success: false,
      error: 'Failed to create/update pattern'
    }, { status: 500 });
  }
}