import React from 'react';
import styled from 'styled-components';

const PortsContainer = styled.div`
  background: linear-gradient(145deg, rgba(184, 134, 11, 0.1), rgba(47, 79, 79, 0.1));
  border: 2px solid rgba(184, 134, 11, 0.3);
  border-radius: 15px;
  padding: 20px;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
`;

const PanelTitle = styled.h2`
  color: #daa520;
  font-size: 1.4rem;
  margin: 0 0 20px 0;
  text-align: center;
  font-weight: 600;
  text-shadow: 0 0 5px rgba(218, 165, 32, 0.5);
`;

const BronzePort = styled.div`
  background: linear-gradient(45deg, #b8860b, #daa520);
  border-radius: 12px;
  padding: 15px;
  margin: 15px 0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(255, 215, 0, 0.2);
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.5);
  }
`;

const PortHeader = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
`;

const PortIcon = styled.span`
  font-size: 1.2rem;
  margin-right: 8px;
`;

const PortName = styled.span`
  color: #1a1a1a;
  font-weight: 600;
  font-size: 0.9rem;
`;

const PortStatus = styled.span`
  color: ${props => {
    switch(props.health) {
      case 'excellent': return '#4caf50';
      case 'good': return '#8bc34a'; 
      case 'fair': return '#ff9800';
      case 'poor': return '#f44336';
      default: return '#757575';
    }
  }};
  font-size: 0.8rem;
  font-weight: 500;
  text-transform: uppercase;
`;

const HealthBar = styled.div`
  width: 100%;
  height: 8px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 4px;
  overflow: hidden;
  margin: 8px 0;
`;

const HealthFill = styled.div`
  height: 100%;
  background: ${props => {
    switch(props.health) {
      case 'excellent': return 'linear-gradient(90deg, #4caf50, #66bb6a)';
      case 'good': return 'linear-gradient(90deg, #8bc34a, #9ccc65)';
      case 'fair': return 'linear-gradient(90deg, #ff9800, #ffb74d)';
      case 'poor': return 'linear-gradient(90deg, #f44336, #ef5350)';
      default: return '#757575';
    }
  }};
  width: ${props => {
    switch(props.health) {
      case 'excellent': return '100%';
      case 'good': return '75%';
      case 'fair': return '50%';
      case 'poor': return '25%';
      default: return '0%';
    }
  }};
  transition: width 0.5s ease;
  animation: ${props => props.health === 'excellent' ? 'pulse 2s infinite' : 'none'};
`;

const PortMetrics = styled.div`
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  color: #1a1a1a;
  margin-top: 5px;
`;

const FlowIndicator = styled.div`
  display: flex;
  align-items: center;
  margin-top: 8px;
`;

const FlowParticle = styled.div`
  width: 4px;
  height: 4px;
  background: #ffd700;
  border-radius: 50%;
  margin: 0 2px;
  animation: flow 2s ease-in-out infinite;
  animation-delay: ${props => props.delay}s;
  opacity: ${props => props.active ? 1 : 0.3};
`;

const BronzePortsPanel = ({ portHealth }) => {
  const getPortIcon = (hookType) => {
    const icons = {
      'PostToolUse': '🟡',
      'UserPromptSubmit': '🔵',
      'Stop': '⚪',
      'Read': '🟢'
    };
    return icons[hookType] || '⚫';
  };

  const formatLastEvent = (lastEvent) => {
    if (!lastEvent) return 'No activity';
    const timeDiff = Date.now() - lastEvent.getTime();
    const seconds = Math.floor(timeDiff / 1000);
    if (seconds < 60) return `${seconds}s ago`;
    const minutes = Math.floor(seconds / 60);
    return `${minutes}m ago`;
  };

  return (
    <PortsContainer>
      <PanelTitle>Bronze Collection Ports</PanelTitle>
      
      {Object.entries(portHealth).map(([hookType, stats]) => (
        <BronzePort key={hookType}>
          <PortHeader>
            <div>
              <PortIcon>{getPortIcon(hookType)}</PortIcon>
              <PortName>{hookType}</PortName>
            </div>
            <PortStatus health={stats.health}>{stats.health}</PortStatus>
          </PortHeader>
          
          <HealthBar>
            <HealthFill health={stats.health} />
          </HealthBar>
          
          <FlowIndicator>
            {[0, 0.3, 0.6, 0.9, 1.2].map((delay, i) => (
              <FlowParticle 
                key={i}
                delay={delay}
                active={stats.count > i * 5}
              />
            ))}
          </FlowIndicator>
          
          <PortMetrics>
            <span>Events: {stats.count}</span>
            <span>{formatLastEvent(stats.lastEvent)}</span>
          </PortMetrics>
        </BronzePort>
      ))}
    </PortsContainer>
  );
};

export default BronzePortsPanel;