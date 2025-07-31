import { NextResponse } from 'next/server';
import Airtable from 'airtable';

// Configure Airtable
const AIRTABLE_API_KEY = process.env.AIRTABLE_API_KEY;
const AIRTABLE_BASE_ID = process.env.AIRTABLE_BASE_ID;
const AIRTABLE_INSTITUTIONS_TABLE = process.env.AIRTABLE_INSTITUTIONS_TABLE || 'INSTITUTIONS';

// Initialize Airtable
const initAirtable = () => {
  if (!AIRTABLE_API_KEY || !AIRTABLE_BASE_ID) {
    throw new Error('Airtable credentials not configured');
  }
  
  return new Airtable({ apiKey: AIRTABLE_API_KEY, requestTimeout: 30000 }).base(AIRTABLE_BASE_ID);
};

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const institutionId = searchParams.get('id');
    const isActive = searchParams.get('isActive');
    const type = searchParams.get('type');
    
    const base = initAirtable();
    
    // Build filter conditions
    let filterConditions = [];
    
    if (institutionId) {
      filterConditions.push(`{InstitutionId} = '${institutionId}'`);
    }
    
    if (isActive !== null) {
      filterConditions.push(`{IsActive} = ${isActive === 'true' ? 'TRUE()' : 'FALSE()'}`);
    }
    
    if (type) {
      filterConditions.push(`{Type} = '${type}'`);
    }
    
    const filterFormula = filterConditions.length > 0 
      ? filterConditions.length > 1 
        ? `AND(${filterConditions.join(', ')})` 
        : filterConditions[0]
      : '';
    
    const records = await base(AIRTABLE_INSTITUTIONS_TABLE)
      .select({
        filterByFormula: filterFormula,
        sort: [{ field: 'Name', direction: 'asc' }],
        maxRecords: 100
      })
      .all();
    
    const institutions = records.map(record => ({
      id: record.id,
      institutionId: record.get('InstitutionId') as string,
      name: record.get('Name') as string,
      type: record.get('Type') as string,
      description: record.get('Description') as string,
      isActive: record.get('IsActive') as boolean,
      consciousness: record.get('Consciousness') as string || null,
      guidingVoice: record.get('GuidingVoice') as string || null,
      currentLeader: record.get('CurrentLeader') as string || null,
      members: record.get('Members') as string[] || [],
      treasury: record.get('Treasury') as number || 0,
      influence: record.get('Influence') as number || 0,
      location: record.get('Location') as string || null,
      foundedDate: record.get('FoundedDate') as string || null,
      lastActivity: record.get('LastActivity') as string || null,
      metadata: record.get('Metadata') as string || null
    }));
    
    return NextResponse.json({
      success: true,
      institutions: institutions,
      count: institutions.length
    });
    
  } catch (error) {
    console.error('Error fetching institutions:', error);
    return NextResponse.json(
      { 
        success: false, 
        error: 'Failed to fetch institutions',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const {
      institutionId,
      name,
      type,
      description,
      isActive = true,
      consciousness,
      guidingVoice,
      currentLeader,
      members = [],
      treasury = 0,
      influence = 0,
      location,
      foundedDate,
      metadata
    } = body;
    
    // Validate required fields
    if (!institutionId || !name || !type) {
      return NextResponse.json(
        { 
          success: false, 
          error: 'Missing required fields: institutionId, name, and type are required' 
        },
        { status: 400 }
      );
    }
    
    const base = initAirtable();
    
    // Check if institution already exists
    const existingRecords = await base(AIRTABLE_INSTITUTIONS_TABLE)
      .select({
        filterByFormula: `{InstitutionId} = '${institutionId}'`,
        maxRecords: 1
      })
      .all();
    
    if (existingRecords.length > 0) {
      return NextResponse.json(
        { 
          success: false, 
          error: 'Institution with this ID already exists' 
        },
        { status: 400 }
      );
    }
    
    // Create the institution
    const fields = {
      InstitutionId: institutionId,
      Name: name,
      Type: type,
      Description: description,
      IsActive: isActive,
      Consciousness: consciousness,
      GuidingVoice: guidingVoice,
      CurrentLeader: currentLeader,
      Members: members,
      Treasury: treasury,
      Influence: influence,
      Location: location,
      FoundedDate: foundedDate || new Date().toISOString(),
      LastActivity: new Date().toISOString(),
      Metadata: metadata
    };
    
    const createdRecord = await base(AIRTABLE_INSTITUTIONS_TABLE).create(fields);
    
    return NextResponse.json({
      success: true,
      institution: {
        id: createdRecord.id,
        ...fields
      }
    });
    
  } catch (error) {
    console.error('Error creating institution:', error);
    return NextResponse.json(
      { 
        success: false, 
        error: 'Failed to create institution',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}

export async function PATCH(request: Request) {
  try {
    const body = await request.json();
    const { institutionId, ...updates } = body;
    
    if (!institutionId) {
      return NextResponse.json(
        { 
          success: false, 
          error: 'institutionId is required' 
        },
        { status: 400 }
      );
    }
    
    const base = initAirtable();
    
    // Find the institution
    const records = await base(AIRTABLE_INSTITUTIONS_TABLE)
      .select({
        filterByFormula: `{InstitutionId} = '${institutionId}'`,
        maxRecords: 1
      })
      .all();
    
    if (records.length === 0) {
      return NextResponse.json(
        { 
          success: false, 
          error: 'Institution not found' 
        },
        { status: 404 }
      );
    }
    
    // Update LastActivity
    updates.LastActivity = new Date().toISOString();
    
    // Update the institution
    const updatedRecord = await base(AIRTABLE_INSTITUTIONS_TABLE).update(records[0].id, updates);
    
    return NextResponse.json({
      success: true,
      institution: {
        id: updatedRecord.id,
        institutionId: updatedRecord.get('InstitutionId'),
        ...updates
      }
    });
    
  } catch (error) {
    console.error('Error updating institution:', error);
    return NextResponse.json(
      { 
        success: false, 
        error: 'Failed to update institution',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}