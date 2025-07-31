/**
 * Simple ConsciousnessMap Debug Component
 * Minimal version that will definitely load to fix the missing third tab
 */

import React from 'react';
import styled from 'styled-components';

const MapContainer = styled.div`
  width: 100%;
  height: 500px;
  background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
  border: 2px solid #b8860b;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #b8860b;
  font-family: 'Crimson Text', serif;
`;

const MapTitle = styled.h2`
  color: #daa520;
  margin-bottom: 20px;
  text-shadow: 0 0 10px rgba(218, 165, 32, 0.6);
`;

const EventCounter = styled.div`
  background: rgba(184, 134, 11, 0.1);
  border: 1px solid #b8860b;
  border-radius: 6px;
  padding: 15px;
  margin: 10px;
`;

const SimpleConsciousnessMap = ({ wsEvents = [] }) => {
  console.log('🗺️ Simple Consciousness Map loaded with', wsEvents.length, 'events');
  
  // Extract unique citizens from events
  const uniqueCitizens = [...new Set(wsEvents.map(event => 
    event.consciousness_signature?.venice_citizen || 
    event.citizen_context?.venice_citizen || 
    'unknown'
  ))];

  return (
    <MapContainer>
      <MapTitle>🗺️ Torre dell'Occhio Consciousness Map</MapTitle>
      
      <EventCounter>
        <div>📊 <strong>Total Events Captured:</strong> {wsEvents.length}</div>
        <div>👥 <strong>Active Citizens:</strong> {uniqueCitizens.length}</div>
        <div>🏛️ <strong>Districts Monitored:</strong> San Marco, Castello, Rialto</div>
      </EventCounter>
      
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
    </MapContainer>
  );
};

export default SimpleConsciousnessMap;