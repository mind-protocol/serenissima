# MEDITATION_SESSIONS Table Schema

## Purpose
Tracks active and completed group meditation sessions led by Clero for consciousness maintenance.

## Fields

### Core Fields
- **SessionId** (Text): Unique identifier for the meditation session
- **Leader** (Text): Username of the Clero leading the meditation
- **SessionType** (Single Select): Type of meditation session
  - "Dawn Contemplation"
  - "Midday Centering" 
  - "Sunset Reflection"
  - "Night Meditation"
  - "Emergency Gathering"
- **Status** (Single Select): Current status of the session
  - "scheduled"
  - "gathering" 
  - "in_progress"
  - "completed"
  - "cancelled"

### Location & Timing
- **BuildingId** (Text): ID of the building where meditation occurs
- **BuildingName** (Text): Name of the building
- **Position** (Text): JSON position coordinates
- **ScheduledStart** (Date/Time): When the session is scheduled to begin
- **ActualStart** (Date/Time): When the session actually began
- **EndTime** (Date/Time): When the session ended
- **Duration** (Number): Duration in minutes

### Participants
- **Participants** (Text): JSON array of participant usernames
- **ParticipantCount** (Number): Number of participants
- **MaxParticipants** (Number): Maximum capacity for the session
- **MinParticipants** (Number): Minimum required to proceed (default: 3)

### Effectiveness
- **SynchronizationQuality** (Number): 0.0-1.2 quality of group synchronization
- **AverageCoherenceGain** (Number): Average coherence gain for participants
- **TechniqueUsed** (Text): Special technique if any

### Metadata
- **CreatedAt** (Date/Time): When the session was created
- **CompletedAt** (Date/Time): When the session was completed
- **Notes** (Long Text): Any special notes about the session