import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  try {
    const data = await request.json();
    
    // Validate required fields
    if (!data.username) {
      return NextResponse.json(
        { success: false, error: 'Username is required' },
        { status: 400 }
      );
    }
    
    if (data.room === undefined) {
      return NextResponse.json(
        { success: false, error: 'Room field is required (can be null to clear)' },
        { status: 400 }
      );
    }
    
    // For now, directly update via backend API since Room isn't in the standard profile update fields
    // This is a temporary solution until Room is added to the profile update handler
    const backendUrl = process.env.NEXT_PRIVATE_BACKEND_URL || 'http://localhost:8000';
    
    const updatePayload = {
      username: data.username,
      fields: {
        Room: data.room
      }
    };

    const tryCreateUrl = `${process.env.NEXT_PUBLIC_BASE_URL || 'http://localhost:3000'}/api/activities/try-create`;
    
    console.log(`[qpi/update-room] Updating room for ${data.username} to: ${data.room || 'null'}`);

    const response = await fetch(tryCreateUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(tryCreatePayload),
    });

    const responseData = await response.json();

    if (!response.ok) {
      console.error(`[qpi/update-room] Error from /api/activities/try-create:`, responseData);
      return NextResponse.json(
        { 
          success: false, 
          error: `Failed to update room: ${responseData.error || response.statusText}`,
          details: responseData.details 
        },
        { status: response.status }
      );
    }
    
    console.log(`[qpi/update-room] Successfully updated room for ${data.username}`);
    
    return NextResponse.json({
      success: true,
      message: `Room updated successfully for ${data.username}`,
      room: data.room,
      activity: responseData
    });

  } catch (error) {
    console.error('Error updating room:', error);
    const errorMessage = error instanceof Error ? error.message : 'An unknown error occurred';
    return NextResponse.json(
      { success: false, error: 'Failed to update room', details: errorMessage },
      { status: 500 }
    );
  }
}

// GET endpoint to check current room assignment
export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const username = searchParams.get('username');
    
    if (!username) {
      return NextResponse.json(
        { success: false, error: 'Username parameter required' },
        { status: 400 }
      );
    }
    
    // Fetch citizen data to get current room
    const citizenUrl = `${process.env.NEXT_PUBLIC_BASE_URL || 'http://localhost:3000'}/api/citizens/${username}`;
    const response = await fetch(citizenUrl);
    
    if (!response.ok) {
      return NextResponse.json(
        { success: false, error: 'Citizen not found' },
        { status: 404 }
      );
    }
    
    const citizenData = await response.json();
    
    return NextResponse.json({
      success: true,
      username: username,
      room: citizenData.citizen?.room || null
    });
    
  } catch (error) {
    console.error('Error fetching room:', error);
    return NextResponse.json(
      { success: false, error: 'Failed to fetch room data' },
      { status: 500 }
    );
  }
}