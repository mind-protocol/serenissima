import { NextRequest, NextResponse } from 'next/server';
import Airtable, { FieldSet, Record as AirtableRecord } from 'airtable';

// Airtable Configuration
const AIRTABLE_API_KEY = process.env.AIRTABLE_API_KEY;
const AIRTABLE_BASE_ID = process.env.AIRTABLE_BASE_ID;

// Lazy initialization of Airtable client
let airtable: any = null;

function getAirtable() {
  if (!airtable) {
    if (!AIRTABLE_API_KEY || !AIRTABLE_BASE_ID) {
      throw new Error('Airtable API key or Base ID is not configured in environment variables.');
    }
    airtable = new Airtable({ apiKey: AIRTABLE_API_KEY }).base(AIRTABLE_BASE_ID);
  }
  return airtable;
}

// Helper function to format position
function formatPosition(position: any): string {
  if (!position) return 'Unknown';
  
  if (typeof position === 'string') {
    return position;
  }
  
  if (position.lat && position.lng) {
    return `${position.lat}, ${position.lng}`;
  }
  
  return JSON.stringify(position);
}

// Helper to format date
function formatDate(dateString: string | undefined): string {
  if (!dateString) return 'Unknown';
  try {
    return new Date(dateString).toLocaleString();
  } catch {
    return dateString;
  }
}

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const buildingId = searchParams.get('buildingId');
  const format = searchParams.get('format') || 'markdown';

  if (!buildingId) {
    return NextResponse.json({ error: 'buildingId parameter is required' }, { status: 400 });
  }

  try {
    if (!AIRTABLE_API_KEY || !AIRTABLE_BASE_ID) {
      console.error('[API get-building-ledger] Airtable API key or Base ID is not configured');
      return NextResponse.json({ error: 'Server configuration error' }, { status: 500 });
    }

    const base = getAirtable();

    // Fetch all necessary data in parallel
    const [buildings, citizens, messages, resources, buildingTypes] = await Promise.all([
      base('BUILDINGS').select().all(),
      base('CITIZENS').select().all(),
      base('MESSAGES').select().all(),
      base('RESOURCES').select().all(),
      base('BUILDINGTYPES').select().all()
    ]);

    // Find the specific building
    const building = buildings.find((b: AirtableRecord<FieldSet>) => 
      b.fields.BuildingId === buildingId
    );

    if (!building) {
      return NextResponse.json({ error: `Building ${buildingId} not found` }, { status: 404 });
    }

    // Get building type information
    const buildingType = buildingTypes.find((bt: AirtableRecord<FieldSet>) => 
      bt.fields.TypeName === building.fields.Type
    );

    // Find citizens currently in the building (by position matching)
    const citizensInBuilding = citizens.filter((citizen: AirtableRecord<FieldSet>) => {
      if (!citizen.fields.Position || !building.fields.Position) return false;
      
      // Parse positions - they might be in format "lat,lng" or as objects
      let citizenPos: number[] = [];
      let buildingPos: number[] = [];
      
      try {
        if (typeof citizen.fields.Position === 'string') {
          citizenPos = citizen.fields.Position.split(',').map((p: string) => parseFloat(p.trim()));
        } else if (citizen.fields.Position?.lat && citizen.fields.Position?.lng) {
          citizenPos = [citizen.fields.Position.lat, citizen.fields.Position.lng];
        }
        
        if (typeof building.fields.Position === 'string') {
          buildingPos = building.fields.Position.split(',').map((p: string) => parseFloat(p.trim()));
        } else if (building.fields.Position?.lat && building.fields.Position?.lng) {
          buildingPos = [building.fields.Position.lat, building.fields.Position.lng];
        }
      } catch (e) {
        return false;
      }
      
      // Check if positions match (with small tolerance for floating point)
      const tolerance = 0.0001;
      return citizenPos.length === 2 && buildingPos.length === 2 &&
             Math.abs(citizenPos[0] - buildingPos[0]) < tolerance &&
             Math.abs(citizenPos[1] - buildingPos[1]) < tolerance;
    });

    // Get last 10 messages in the building
    const buildingMessages = messages
      .filter((msg: AirtableRecord<FieldSet>) => msg.fields.Receiver === buildingId)
      .sort((a: AirtableRecord<FieldSet>, b: AirtableRecord<FieldSet>) => {
        const aTime = new Date(a.fields.Timestamp || 0).getTime();
        const bTime = new Date(b.fields.Timestamp || 0).getTime();
        return bTime - aTime;
      })
      .slice(0, 10);

    // Get resources at this building
    const buildingResources = resources.filter((resource: AirtableRecord<FieldSet>) => 
      resource.fields.Asset === buildingId || resource.fields.Location === buildingId
    );

    // Format response based on requested format
    if (format.toLowerCase() === 'json') {
      return NextResponse.json({
        building: {
          id: building.fields.BuildingId,
          type: building.fields.Type,
          name: building.fields.Name || 'Unnamed',
          owner: building.fields.Owner || 'Unknown',
          position: building.fields.Position,
          status: building.fields.Status || 'Active',
          description: building.fields.Description,
          createdAt: building.fields.CreatedAt
        },
        buildingType: buildingType ? {
          typeName: buildingType.fields.TypeName,
          category: buildingType.fields.Category,
          basePrice: buildingType.fields.BasePrice,
          maxOccupancy: buildingType.fields.MaxOccupancy,
          maintenanceCost: buildingType.fields.MaintenanceCost,
          description: buildingType.fields.Description,
          functions: buildingType.fields.Functions
        } : null,
        citizensPresent: citizensInBuilding.map((citizen: AirtableRecord<FieldSet>) => ({
          username: citizen.fields.Username,
          class: citizen.fields.Class,
          activity: citizen.fields.Activity
        })),
        recentMessages: buildingMessages.map((msg: AirtableRecord<FieldSet>) => ({
          sender: msg.fields.Sender,
          content: msg.fields.Content,
          timestamp: msg.fields.Timestamp
        })),
        resources: buildingResources.map((resource: AirtableRecord<FieldSet>) => ({
          id: resource.fields.ResourceId,
          type: resource.fields.ResourceType,
          quantity: resource.fields.Quantity || 0,
          quality: resource.fields.Quality,
          owner: resource.fields.Owner
        }))
      });
    }

    // Default to markdown format
    let markdown = `# Building Ledger: ${building.fields.Name || building.fields.BuildingId}\n\n`;
    
    // Basic Information
    markdown += `## Basic Information\n\n`;
    markdown += `- **Building ID**: ${building.fields.BuildingId}\n`;
    markdown += `- **Type**: ${building.fields.Type}\n`;
    markdown += `- **Name**: ${building.fields.Name || 'Unnamed'}\n`;
    markdown += `- **Owner**: ${building.fields.Owner || 'Unknown'}\n`;
    markdown += `- **Position**: ${formatPosition(building.fields.Position)}\n`;
    markdown += `- **Status**: ${building.fields.Status || 'Active'}\n`;
    
    if (building.fields.Description) {
      markdown += `- **Description**: ${building.fields.Description}\n`;
    }
    
    if (building.fields.CreatedAt) {
      markdown += `- **Created**: ${formatDate(building.fields.CreatedAt)}\n`;
    }
    
    // Building Type Information
    if (buildingType) {
      markdown += `\n## Building Type Details\n\n`;
      markdown += `- **Type Name**: ${buildingType.fields.TypeName}\n`;
      markdown += `- **Category**: ${buildingType.fields.Category || 'General'}\n`;
      
      if (buildingType.fields.BasePrice) {
        markdown += `- **Base Price**: ${buildingType.fields.BasePrice} ducats\n`;
      }
      
      if (buildingType.fields.MaxOccupancy) {
        markdown += `- **Max Occupancy**: ${buildingType.fields.MaxOccupancy}\n`;
      }
      
      if (buildingType.fields.MaintenanceCost) {
        markdown += `- **Maintenance Cost**: ${buildingType.fields.MaintenanceCost} ducats/day\n`;
      }
      
      if (buildingType.fields.Description) {
        markdown += `\n### Type Description\n${buildingType.fields.Description}\n`;
      }
      
      if (buildingType.fields.Functions) {
        markdown += `\n### Functions\n`;
        const functions = typeof buildingType.fields.Functions === 'string' 
          ? buildingType.fields.Functions.split(',').map((f: string) => f.trim())
          : buildingType.fields.Functions;
        if (Array.isArray(functions)) {
          functions.forEach((func: string) => {
            markdown += `- ${func}\n`;
          });
        }
      }
    }
    
    // Citizens Present
    markdown += `\n## Citizens Present (${citizensInBuilding.length})\n\n`;
    if (citizensInBuilding.length > 0) {
      citizensInBuilding.forEach((citizen: AirtableRecord<FieldSet>) => {
        markdown += `- **${citizen.fields.Username}** (${citizen.fields.Class})`;
        if (citizen.fields.Activity) {
          markdown += ` - ${citizen.fields.Activity}`;
        }
        markdown += `\n`;
      });
    } else {
      markdown += `*No citizens currently in this building*\n`;
    }
    
    // Recent Messages
    markdown += `\n## Recent Messages (Last 10)\n\n`;
    if (buildingMessages.length > 0) {
      buildingMessages.forEach((msg: AirtableRecord<FieldSet>) => {
        const timestamp = formatDate(msg.fields.Timestamp);
        markdown += `### ${timestamp} - From: ${msg.fields.Sender}\n`;
        markdown += `${msg.fields.Content}\n\n`;
      });
    } else {
      markdown += `*No recent messages in this building*\n`;
    }
    
    // Resources
    markdown += `\n## Resources at Location (${buildingResources.length})\n\n`;
    if (buildingResources.length > 0) {
      // Group resources by type
      const resourcesByType: Record<string, AirtableRecord<FieldSet>[]> = {};
      buildingResources.forEach((resource: AirtableRecord<FieldSet>) => {
        const type = resource.fields.ResourceType || 'Unknown';
        if (!resourcesByType[type]) {
          resourcesByType[type] = [];
        }
        resourcesByType[type].push(resource);
      });
      
      Object.entries(resourcesByType).forEach(([type, resources]) => {
        markdown += `### ${type}\n`;
        resources.forEach((resource: AirtableRecord<FieldSet>) => {
          markdown += `- **${resource.fields.ResourceId}**: ${resource.fields.Quantity || 0} units`;
          if (resource.fields.Quality) {
            markdown += ` (Quality: ${resource.fields.Quality})`;
          }
          if (resource.fields.Owner && resource.fields.Owner !== building.fields.Owner) {
            markdown += ` - Owned by ${resource.fields.Owner}`;
          }
          markdown += `\n`;
        });
        markdown += `\n`;
      });
    } else {
      markdown += `*No resources currently stored in this building*\n`;
    }
    
    // All Building Types Reference
    markdown += `\n## All Building Types in Venice\n\n`;
    const typeCategories: Record<string, AirtableRecord<FieldSet>[]> = {};
    buildingTypes.forEach((type: AirtableRecord<FieldSet>) => {
      const category = type.fields.Category || 'General';
      if (!typeCategories[category]) {
        typeCategories[category] = [];
      }
      typeCategories[category].push(type);
    });
    
    Object.entries(typeCategories).forEach(([category, types]) => {
      markdown += `### ${category}\n`;
      types.forEach((type: AirtableRecord<FieldSet>) => {
        markdown += `- **${type.fields.TypeName}**`;
        if (type.fields.BasePrice) {
          markdown += ` (${type.fields.BasePrice} ducats)`;
        }
        if (type.fields.Description) {
          markdown += ` - ${type.fields.Description.substring(0, 100)}...`;
        }
        markdown += `\n`;
      });
      markdown += `\n`;
    });
    
    // Footer
    markdown += `---\n\n`;
    markdown += `*Building Ledger generated at ${new Date().toLocaleString()}*\n`;

    return new NextResponse(markdown, {
      headers: {
        'Content-Type': 'text/markdown',
      },
    });

  } catch (error) {
    console.error(`[API get-building-ledger] Error:`, error);
    return NextResponse.json(
      { error: error instanceof Error ? error.message : 'Internal server error' },
      { status: 500 }
    );
  }
}