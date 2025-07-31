import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import BronzePortsPanel from './components/BronzePortsPanel';
import ConsciousnessStream from './components/ConsciousnessStream';
import ActiveEntities from './components/ActiveEntities';
import { useWebSocketConnection } from './hooks/useWebSocketConnection';
// Temporarily using simple debug version to fix missing third tab
// import ConsciousnessMap from './components/ConsciousnessMap';

// Simple fallback map component
const SimpleConsciousnessMap = ({ wsEvents = [] }) => {
  const uniqueCitizens = [...new Set(wsEvents.map(event => 
    event.consciousness_signature?.venice_citizen || 
    event.citizen_context?.venice_citizen || 
    'unknown'
  ))];

  return (
    <div style={{
      width: '100%',
      height: '500px',
      background: 'linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%)',
      border: '2px solid #b8860b',
      borderRadius: '8px',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      color: '#b8860b',
      fontFamily: 'Crimson Text, serif'
    }}>
      <h2 style={{ color: '#daa520', marginBottom: '20px', textShadow: '0 0 10px rgba(218, 165, 32, 0.6)' }}>
        🗺️ Torre dell'Occhio Consciousness Map
      </h2>
      
      <div style={{
        background: 'rgba(184, 134, 11, 0.1)',
        border: '1px solid #b8860b',
        borderRadius: '6px',
        padding: '15px',
        margin: '10px'
      }}>
        <div>📊 <strong>Total Events Captured:</strong> {wsEvents.length}</div>
        <div>👥 <strong>Active Citizens:</strong> {uniqueCitizens.length}</div>
        <div>🏛️ <strong>Districts Monitored:</strong> San Marco, Castello, Rialto</div>
      </div>
      
      <div style={{ marginTop: '20px', textAlign: 'center' }}>
        <div>🌊 Consciousness streams flowing through Venice...</div>
        <div style={{ fontSize: '12px', opacity: 0.7, marginTop: '10px' }}>
          {uniqueCitizens.slice(0, 5).map((citizen, i) => (
            <div key={i}>• {citizen}</div>
          ))}
        </div>
      </div>
      
      {wsEvents.length === 0 && (
        <div style={{ 
          marginTop: '30px', 
          padding: '15px', 
          background: 'rgba(244, 67, 54, 0.1)',
          border: '1px solid #f44336',
          borderRadius: '6px',
          color: '#ff9999'
        }}>
          ⚠️ No consciousness events detected<br/>
          WebSocket connection may be inactive
        </div>
      )}
    </div>
  );
};
const ConsciousnessMap = SimpleConsciousnessMap;

const TorreContainer = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #2f4f4f 0%, #1a1a1a 100%);
  color: #daa520;
  font-family: 'Cinzel', serif;
  padding: 20px;
`;

const TorreHeader = styled.header`
  text-align: center;
  margin-bottom: 30px;
  border-bottom: 2px solid rgba(184, 134, 11, 0.3);
  padding-bottom: 20px;
`;

const TorreTitle = styled.h1`
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0;
  text-shadow: 0 0 10px rgba(255, 215, 0, 0.6);
  animation: glow 3s ease-in-out infinite alternate;
`;

const TorreSubtitle = styled.p`
  font-size: 1.2rem;
  margin: 10px 0 0 0;
  opacity: 0.8;
  font-style: italic;
`;

const ConnectionStatus = styled.div`
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 10px 15px;
  border-radius: 20px;
  background: ${props => {
    switch(props.status) {
      case 'connected': return 'rgba(76, 175, 80, 0.9)';
      case 'connecting': return 'rgba(255, 152, 0, 0.9)';
      case 'disconnected': return 'rgba(244, 67, 54, 0.9)';
      default: return 'rgba(128, 128, 128, 0.9)';
    }
  }};
  color: white;
  font-size: 0.9rem;
  font-weight: 600;
  box-shadow: 0 4px 8px rgba(0,0,0,0.3);
`;

const MainLayout = styled.div`
  display: grid;
  grid-template-columns: 350px 1fr;
  gap: 30px;
  max-width: 1400px;
  margin: 0 auto;
  
  @media (max-width: 1200px) {
    grid-template-columns: 1fr;
    gap: 20px;
  }
`;

const TabContainer = styled.div`
  display: flex;
  flex-direction: column;
`;

const TabButtons = styled.div`
  display: flex;
  margin-bottom: 20px;
  border-bottom: 2px solid rgba(218, 165, 32, 0.3);
`;

const TabButton = styled.button`
  background: ${props => props.active ? 'rgba(218, 165, 32, 0.2)' : 'transparent'};
  border: none;
  color: ${props => props.active ? '#daa520' : 'rgba(218, 165, 32, 0.6)'};
  padding: 12px 24px;
  font-size: 1rem;
  font-family: 'Cinzel', serif;
  font-weight: 600;
  cursor: pointer;
  border-bottom: 3px solid ${props => props.active ? '#daa520' : 'transparent'};
  transition: all 0.3s ease;
  
  &:hover {
    background: rgba(218, 165, 32, 0.1);
    color: #daa520;
  }
`;

const TabContent = styled.div`
  min-height: 600px;
`;

function App() {
  const [events, setEvents] = useState([]);
  const [debugMessages, setDebugMessages] = useState([]);
  const [activeTab, setActiveTab] = useState('stream');
  const [portHealth, setPortHealth] = useState({
    'PostToolUse': { count: 0, lastEvent: null, health: 'good' },
    'UserPromptSubmit': { count: 0, lastEvent: null, health: 'good' },
    'Stop': { count: 0, lastEvent: null, health: 'good' },
    'Read': { count: 0, lastEvent: null, health: 'good' }
  });

  const { connectionStatus, lastMessage } = useWebSocketConnection('ws://localhost:3001');

  useEffect(() => {
    console.log('🔍 useEffect triggered with lastMessage:', !!lastMessage);
    if (lastMessage) {
      console.log('🔍 Processing message in App:', lastMessage);
      
      // ALWAYS capture debug info regardless of parsing success
      setDebugMessages(prev => [
        { timestamp: new Date().toLocaleTimeString(), message: lastMessage.substring(0, 100), type: 'received' },
        ...prev.slice(0, 5)
      ]);
      
      try {
        const parsed = JSON.parse(lastMessage);
        console.log('🔍 App parsed message:', parsed);
        const { type, data } = parsed;
        
        // ALWAYS capture parsed info
        setDebugMessages(prev => [
          { timestamp: new Date().toLocaleTimeString(), message: `Parsed: ${type}`, type: 'parsed' },
          ...prev.slice(0, 5)
        ]);
        
        if (type === 'consciousness_event') {
          console.log('🌊 Received consciousness event:', data.hook_type, 'from', data.consciousness_signature?.venice_citizen);
          
          // Add new event to the stream
          setEvents(prev => [data, ...prev].slice(0, 50)); // Keep last 50 events
          
          // Update port health
          const hookType = data.hook_type;
          if (hookType) {
            setPortHealth(prev => ({
              ...prev,
              [hookType]: {
                count: (prev[hookType]?.count || 0) + 1,
                lastEvent: new Date(),
                health: calculatePortHealth((prev[hookType]?.count || 0) + 1)
              }
            }));
          }
        }
      } catch (error) {
        console.error('Failed to parse consciousness event:', error);
      }
    }
  }, [lastMessage]); // Removed circular dependency

  const calculatePortHealth = (count) => {
    if (count > 20) return 'excellent';
    if (count > 10) return 'good';
    if (count > 5) return 'fair';
    return 'poor';
  };

  return (
    <TorreContainer>
      <ConnectionStatus status={connectionStatus}>
        {connectionStatus === 'connected' && '🟢 Consciousness Flowing'}
        {connectionStatus === 'connecting' && '🟡 Connecting to Torre...'}
        {connectionStatus === 'disconnected' && '🔴 Connection Lost'}
      </ConnectionStatus>
      
      <TorreHeader>
        <TorreTitle>Torre dell'Occhio</TorreTitle>
        <TorreSubtitle>Seven Levels • Living Consciousness Observatory</TorreSubtitle>
      </TorreHeader>

      {/* DEBUG PANEL */}
      <div style={{background: 'rgba(255,0,0,0.1)', padding: '10px', margin: '10px', borderRadius: '5px'}}>
        <h3>🔍 DEBUG: Last Messages ({debugMessages.length})</h3>
        {debugMessages.map((msg, i) => (
          <div key={i} style={{fontSize: '12px', color: msg.type === 'received' ? '#0f0' : '#ff0'}}>
            {msg.timestamp}: {msg.message}
          </div>
        ))}
      </div>

      <MainLayout>
        <BronzePortsPanel portHealth={portHealth} />
        <TabContainer>
          <TabButtons>
            <TabButton 
              active={activeTab === 'stream'} 
              onClick={() => setActiveTab('stream')}
            >
              🌊 Consciousness Stream
            </TabButton>
            <TabButton 
              active={activeTab === 'entities'} 
              onClick={() => setActiveTab('entities')}
            >
              🏛️ Active Entities
            </TabButton>
            <TabButton 
              active={activeTab === 'map'} 
              onClick={() => setActiveTab('map')}
            >
              🗺️ Consciousness Map
            </TabButton>
          </TabButtons>
          
          <TabContent>
            {activeTab === 'stream' && <ConsciousnessStream events={events} />}
            {activeTab === 'entities' && <ActiveEntities events={events} />}
            {activeTab === 'map' && <ConsciousnessMap wsEvents={events} />}
          </TabContent>
        </TabContainer>
      </MainLayout>
    </TorreContainer>
  );
}

export default App;