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

const AIRTABLE_PATTERN_INSTANCES_TABLE = 'PATTERN_INSTANCES';

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

    // Handle pagination
    const limit = parseInt(url.searchParams.get('limit') || '100');
    const offset = parseInt(url.searchParams.get('offset') || '0');

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
    
    console.log('%c GET /api/pattern-instances request received', 'background: #00CED1; color: white; padding: 2px 5px; font-weight: bold;');
    console.log('Query parameters (filters):', loggableFilters);
    console.log(`Pagination: limit=${limit}, offset=${offset}`);
    if (filterByFormula) {
      console.log('Applying Airtable filter formula:', filterByFormula);
    }

    // Fetch pattern instances from Airtable
    const instanceRecords = await base(AIRTABLE_PATTERN_INSTANCES_TABLE)
      .select({
        filterByFormula: filterByFormula,
        sort: [{ field: 'Timestamp', direction: 'desc' }],
        pageSize: limit
      })
      .all();

    // Apply offset manually (Airtable doesn't support offset directly)
    const paginatedRecords = instanceRecords.slice(offset, offset + limit);

    // Transform records for pattern intelligence
    const patternInstances = paginatedRecords.map(record => ({
      instanceId: record.get('InstanceID') as string,
      patternId: record.get('PatternID') as string,
      citizenUsername: record.get('CitizenUsername') as string,
      timestamp: record.get('Timestamp') as string,
      context: record.get('Context') as string,
      cascadeTriggered: record.get('CascadeTriggered') as boolean || false,
      cascadePatterns: record.get('CascadePatterns') as string[] || [],
      valueGenerated: record.get('ValueGenerated') as number || 0,
      impactRadius: record.get('ImpactRadius') as number || 0,
      resonanceScore: record.get('ResonanceScore') as number || 0,
      patternFusion: record.get('PatternFusion') as string[] || [],
      emergentProperties: record.get('EmergentProperties') as any || {},
      locationData: record.get('LocationData') as any || {},
      channelSource: record.get('ChannelSource') as string || 'unknown',
      significanceLevel: record.get('SignificanceLevel') as string || 'normal',
      archived: record.get('Archived') as boolean || false
    }));

    // Calculate instance analytics
    const analytics = {
      totalInstances: instanceRecords.length,
      cascadeRate: patternInstances.filter(i => i.cascadeTriggered).length / patternInstances.length || 0,
      averageValue: patternInstances.reduce((sum, i) => sum + i.valueGenerated, 0) / patternInstances.length || 0,
      topPatterns: getTopPatterns(patternInstances),
      activeChannels: [...new Set(patternInstances.map(i => i.channelSource))],
      patternFusions: identifyFusions(patternInstances)
    };
    
    return NextResponse.json({
      success: true,
      patternInstances: patternInstances,
      analytics: analytics,
      pagination: {
        limit: limit,
        offset: offset,
        total: instanceRecords.length,
        hasMore: offset + limit < instanceRecords.length
      },
      timestamp: new Date().toISOString()
    });
    
  } catch (error) {
    console.error('Error fetching pattern instances:', error);
    
    // Return sample pattern instances for development/fallback
    const sampleInstances = [
      {
        instanceId: 'inst_001',
        patternId: '#3',
        citizenUsername: 'Italia',
        timestamp: new Date(Date.now() - 300000).toISOString(),
        context: 'CASCADE implementation sprint activation',
        cascadeTriggered: true,
        cascadePatterns: ['#19', '#8'],
        valueGenerated: 47000,
        impactRadius: 23,
        resonanceScore: 0.89,
        patternFusion: ['#3+#19'],
        emergentProperties: { urgency_amplification: 2.3, collective_focus: 0.92 },
        locationData: { source: 'Venice', spread: ['Arsenal', 'Rialto'] },
        channelSource: 'telegram',
        significanceLevel: 'critical',
        archived: false
      },
      {
        instanceId: 'inst_002',
        patternId: '#18',
        citizenUsername: 'pattern_prophet',
        timestamp: new Date(Date.now() - 600000).toISOString(),
        context: 'Proof-weave consciousness value demonstration',
        cascadeTriggered: false,
        cascadePatterns: [],
        valueGenerated: 32000,
        impactRadius: 15,
        resonanceScore: 0.94,
        patternFusion: ['#2+#18'],
        emergentProperties: { value_crystallization: true, investor_attention: 0.78 },
        locationData: { source: 'Academia', spread: ['Market', 'Council'] },
        channelSource: 'message',
        significanceLevel: 'high',
        archived: false
      }
    ];
    
    return NextResponse.json({
      success: true,
      patternInstances: sampleInstances,
      analytics: {
        totalInstances: 2,
        cascadeRate: 0.5,
        averageValue: 39500,
        topPatterns: [{ patternId: '#3', count: 1 }, { patternId: '#18', count: 1 }],
        activeChannels: ['telegram', 'message'],
        patternFusions: ['#3+#19', '#2+#18']
      },
      pagination: {
        limit: 100,
        offset: 0,
        total: 2,
        hasMore: false
      },
      timestamp: new Date().toISOString(),
      _fallback: true
    });
  }
}

// Helper function to identify top patterns
function getTopPatterns(instances: any[]): any[] {
  const patternCounts: Record<string, number> = {};
  instances.forEach(instance => {
    patternCounts[instance.patternId] = (patternCounts[instance.patternId] || 0) + 1;
  });
  
  return Object.entries(patternCounts)
    .map(([patternId, count]) => ({ patternId, count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 5);
}

// Helper function to identify pattern fusions
function identifyFusions(instances: any[]): string[] {
  const fusions = new Set<string>();
  instances.forEach(instance => {
    if (instance.patternFusion && Array.isArray(instance.patternFusion)) {
      instance.patternFusion.forEach((fusion: string) => fusions.add(fusion));
    }
  });
  return Array.from(fusions);
}

// POST endpoint for recording pattern instances
export async function POST(request: Request) {
  try {
    const base = initAirtable();
    const data = await request.json();
    
    // Validate required fields
    if (!data.patternId || !data.citizenUsername) {
      return NextResponse.json({
        success: false,
        error: 'PatternID and CitizenUsername are required'
      }, { status: 400 });
    }
    
    // Create pattern instance
    const fields = {
      InstanceID: data.instanceId || `inst_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      PatternID: data.patternId,
      CitizenUsername: data.citizenUsername,
      Timestamp: data.timestamp || new Date().toISOString(),
      Context: data.context || '',
      CascadeTriggered: data.cascadeTriggered || false,
      CascadePatterns: data.cascadePatterns || [],
      ValueGenerated: data.valueGenerated || 0,
      ImpactRadius: data.impactRadius || 0,
      ResonanceScore: data.resonanceScore || 0,
      PatternFusion: data.patternFusion || [],
      EmergentProperties: JSON.stringify(data.emergentProperties || {}),
      LocationData: JSON.stringify(data.locationData || {}),
      ChannelSource: data.channelSource || 'unknown',
      SignificanceLevel: data.significanceLevel || 'normal',
      Archived: false
    };
    
    const result = await base(AIRTABLE_PATTERN_INSTANCES_TABLE).create(fields);
    
    return NextResponse.json({
      success: true,
      instance: {
        instanceId: result.get('InstanceID'),
        patternId: result.get('PatternID'),
        citizenUsername: result.get('CitizenUsername'),
        timestamp: result.get('Timestamp'),
        cascadeTriggered: result.get('CascadeTriggered'),
        valueGenerated: result.get('ValueGenerated')
      }
    });
    
  } catch (error) {
    console.error('Error creating pattern instance:', error);
    return NextResponse.json({
      success: false,
      error: 'Failed to create pattern instance'
    }, { status: 500 });
  }
}