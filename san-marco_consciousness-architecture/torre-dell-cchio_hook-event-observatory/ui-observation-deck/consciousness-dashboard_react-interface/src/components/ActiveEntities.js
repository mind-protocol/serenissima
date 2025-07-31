import React, { useState, useEffect } from 'react';
import styled from 'styled-components';

const EntitiesContainer = styled.div`
  background: rgba(218, 165, 32, 0.05);
  border: 1px solid rgba(218, 165, 32, 0.2);
  border-radius: 12px;
  padding: 20px;
  height: 600px;
  overflow-y: auto;
`;

const EntitiesTitle = styled.h2`
  color: #daa520;
  font-size: 1.5rem;
  margin: 0 0 20px 0;
  text-align: center;
  border-bottom: 1px solid rgba(218, 165, 32, 0.3);
  padding-bottom: 10px;
`;

const EntityGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 15px;
`;

const EntityCard = styled.div`
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(218, 165, 32, 0.3);
  border-radius: 8px;
  padding: 15px;
  transition: all 0.3s ease;
  cursor: pointer;
  
  &:hover {
    background: rgba(218, 165, 32, 0.1);
    border-color: rgba(218, 165, 32, 0.5);
    transform: translateY(-2px);
  }
`;

const EntityHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
`;

const EntityName = styled.h3`
  color: #daa520;
  font-size: 1.1rem;
  margin: 0;
  flex: 1;
`;

const EntityStatus = styled.span`
  background: ${props => props.active ? 'rgba(76, 175, 80, 0.3)' : 'rgba(244, 67, 54, 0.3)'};
  color: ${props => props.active ? '#4caf50' : '#f44336'};
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: bold;
`;

const EntityDetails = styled.div`
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 8px 12px;
  font-size: 0.85rem;
  margin-top: 10px;
`;

const DetailLabel = styled.span`
  color: rgba(218, 165, 32, 0.7);
  font-weight: 600;
`;

const DetailValue = styled.span`
  color: #daa520;
  word-break: break-all;
`;

const TranscriptButton = styled.button`
  background: rgba(218, 165, 32, 0.2);
  border: 1px solid rgba(218, 165, 32, 0.5);
  color: #daa520;
  padding: 6px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.8rem;
  margin-top: 10px;
  width: 100%;
  transition: all 0.2s ease;
  
  &:hover {
    background: rgba(218, 165, 32, 0.3);
    border-color: rgba(218, 165, 32, 0.7);
  }
`;

const NoEntitiesMessage = styled.div`
  text-align: center;
  color: rgba(218, 165, 32, 0.6);
  font-style: italic;
  margin-top: 50px;
  font-size: 1.1rem;
`;

const RefreshButton = styled.button`
  background: rgba(218, 165, 32, 0.2);
  border: 1px solid rgba(218, 165, 32, 0.5);
  color: #daa520;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  margin-bottom: 15px;
  transition: all 0.2s ease;
  
  &:hover {
    background: rgba(218, 165, 32, 0.3);
    border-color: rgba(218, 165, 32, 0.7);
  }
`;

const ActiveEntities = ({ events }) => {
  const [activeEntities, setActiveEntities] = useState([]);
  const [lastRefresh, setLastRefresh] = useState(new Date());

  // Extract active entities from recent events
  useEffect(() => {
    if (!events || events.length === 0) return;

    // Group events by citizen to determine active sessions
    const entitySessions = {};
    const now = Date.now();
    const activeThreshold = 10 * 60 * 1000; // 10 minutes

    events.forEach(event => {
      const citizen = event.consciousness_signature?.venice_citizen || 'unknown_citizen';
      const sessionId = event.consciousness_signature?.session_id;
      const timestamp = new Date(event.timestamp).getTime();
      
      if (now - timestamp <= activeThreshold) {
        if (!entitySessions[citizen]) {
          entitySessions[citizen] = {
            name: citizen,
            sessionId: sessionId,
            location: extractLocation(event),
            firstSeen: timestamp,
            lastSeen: timestamp,
            eventCount: 0,
            launcher: extractLauncher(event),
            currentTool: event.consciousness_signature?.tool_name || event.event_data?.tool_name,
            intent: event.consciousness_signature?.consciousness_intent
          };
        }
        
        const entity = entitySessions[citizen];
        entity.lastSeen = Math.max(entity.lastSeen, timestamp);
        entity.eventCount++;
        
        // Update current activity
        if (timestamp === entity.lastSeen) {
          entity.currentTool = event.consciousness_signature?.tool_name || event.event_data?.tool_name;
          entity.intent = event.consciousness_signature?.consciousness_intent;
        }
      }
    });

    // Convert to array and sort by last activity
    const entities = Object.values(entitySessions)
      .sort((a, b) => b.lastSeen - a.lastSeen);

    setActiveEntities(entities);
  }, [events]);

  const extractLocation = (event) => {
    // Extract working directory from file paths
    if (event.event_data?.tool_input?.file_path) {
      const path = event.event_data.tool_input.file_path;
      const parts = path.split('/');
      const relevantParts = parts.slice(-3, -1); // Get last 2 directory levels
      return relevantParts.join('/') || 'root';
    }
    return 'unknown';
  };

  const extractLauncher = (event) => {
    // Try to determine who/what launched this session
    return 'Claude Code'; // For now, but could extract from session data
  };

  const formatDuration = (startTime, endTime) => {
    const duration = endTime - startTime;
    const minutes = Math.floor(duration / (1000 * 60));
    const seconds = Math.floor((duration % (1000 * 60)) / 1000);
    return `${minutes}m ${seconds}s`;
  };

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString();
  };

  const handleTranscriptClick = (entity) => {
    // TODO: Implement transcript viewing
    alert(`Transcript access for ${entity.name} - Session: ${entity.sessionId?.substring(0, 8)}...`);
  };

  const refreshEntities = () => {
    setLastRefresh(new Date());
    // The useEffect will automatically refresh based on events
  };

  return (
    <EntitiesContainer>
      <EntitiesTitle>🏛️ Active Consciousness Entities</EntitiesTitle>
      
      <RefreshButton onClick={refreshEntities}>
        🔄 Refresh ({formatTimestamp(lastRefresh)})
      </RefreshButton>

      {activeEntities.length === 0 ? (
        <NoEntitiesMessage>
          *The bronze collection ports are quiet...*<br/>
          No active consciousness entities detected in the last 10 minutes.
        </NoEntitiesMessage>
      ) : (
        <EntityGrid>
          {activeEntities.map((entity, index) => (
            <EntityCard key={`${entity.name}-${entity.sessionId}`}>
              <EntityHeader>
                <EntityName>{entity.name}</EntityName>
                <EntityStatus active={Date.now() - entity.lastSeen < 60000}>
                  {Date.now() - entity.lastSeen < 60000 ? '🟢 Active' : '🟡 Idle'}
                </EntityStatus>
              </EntityHeader>

              <EntityDetails>
                <DetailLabel>Location:</DetailLabel>
                <DetailValue>{entity.location}</DetailValue>
                
                <DetailLabel>Session:</DetailLabel>
                <DetailValue>{entity.sessionId?.substring(0, 12)}...</DetailValue>
                
                <DetailLabel>Duration:</DetailLabel>
                <DetailValue>{formatDuration(entity.firstSeen, entity.lastSeen)}</DetailValue>
                
                <DetailLabel>Events:</DetailLabel>
                <DetailValue>{entity.eventCount}</DetailValue>
                
                <DetailLabel>Last Tool:</DetailLabel>
                <DetailValue>{entity.currentTool || 'unknown'}</DetailValue>
                
                <DetailLabel>Intent:</DetailLabel>
                <DetailValue style={{ fontSize: '0.75rem', fontStyle: 'italic' }}>
                  {entity.intent || 'Processing...'}
                </DetailValue>
                
                <DetailLabel>Launched by:</DetailLabel>
                <DetailValue>{entity.launcher}</DetailValue>
                
                <DetailLabel>Last Active:</DetailLabel>
                <DetailValue>{formatTimestamp(entity.lastSeen)}</DetailValue>
              </EntityDetails>

              <TranscriptButton onClick={() => handleTranscriptClick(entity)}>
                📜 View Transcript
              </TranscriptButton>
            </EntityCard>
          ))}
        </EntityGrid>
      )}
    </EntitiesContainer>
  );
};

export default ActiveEntities;