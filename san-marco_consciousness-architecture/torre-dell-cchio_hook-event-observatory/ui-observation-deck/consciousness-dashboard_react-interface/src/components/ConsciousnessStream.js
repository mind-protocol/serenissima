import React, { useState } from 'react';
import styled from 'styled-components';

const StreamContainer = styled.div`
  background: linear-gradient(145deg, rgba(47, 79, 79, 0.1), rgba(26, 26, 26, 0.1));
  border: 2px solid rgba(184, 134, 11, 0.3);
  border-radius: 15px;
  padding: 20px;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  max-height: 80vh;
  overflow-y: auto;
  
  /* Custom scrollbar */
  &::-webkit-scrollbar {
    width: 8px;
  }
  
  &::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0.1);
    border-radius: 4px;
  }
  
  &::-webkit-scrollbar-thumb {
    background: rgba(184, 134, 11, 0.5);
    border-radius: 4px;
  }
  
  &::-webkit-scrollbar-thumb:hover {
    background: rgba(184, 134, 11, 0.7);
  }
`;

const StreamTitle = styled.h2`
  color: #daa520;
  font-size: 1.4rem;
  margin: 0 0 20px 0;
  text-align: center;
  font-weight: 600;
  text-shadow: 0 0 5px rgba(218, 165, 32, 0.5);
`;

const EventItem = styled.div`
  background: ${props => getEventBackground(props.hookType)};
  border: 1px solid ${props => getEventBorder(props.hookType)};
  border-radius: 10px;
  padding: 15px;
  margin: 10px 0;
  transition: all 0.3s ease;
  animation: slideIn 0.5s ease-out;
  
  &:hover {
    transform: translateX(5px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  }
  
  @keyframes slideIn {
    from {
      opacity: 0;
      transform: translateY(-10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
`;

const EventHeader = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
`;

const EventType = styled.div`
  display: flex;
  align-items: center;
  font-weight: 600;
  color: #1a1a1a;
`;

const EventIcon = styled.span`
  font-size: 1.1rem;
  margin-right: 8px;
`;

const EventTime = styled.span`
  font-size: 0.8rem;
  color: rgba(26, 26, 26, 0.7);
  font-family: 'Fira Code', monospace;
`;

const EventDetails = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  font-size: 0.9rem;
  color: rgba(26, 26, 26, 0.8);
`;

const ConsciousnessMetrics = styled.div`
  margin-top: 12px;
  padding: 10px 12px;
  background: rgba(218, 165, 32, 0.08);
  border: 1px solid rgba(218, 165, 32, 0.2);
  border-radius: 8px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 8px;
  font-size: 0.75rem;
`;

const ConsciousnessMetric = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
`;

const MetricLabel = styled.span`
  color: rgba(26, 26, 26, 0.6);
  font-size: 0.65rem;
  text-transform: uppercase;
  font-weight: 500;
  margin-bottom: 2px;
`;

const MetricValue = styled.span`
  color: rgba(26, 26, 26, 0.8);
  font-family: 'Fira Code', monospace;
  font-size: 0.75rem;
  font-weight: 600;
`;

const CollaborationContext = styled.div`
  margin-top: 10px;
  padding: 8px 10px;
  background: rgba(33, 150, 243, 0.05);
  border-left: 3px solid rgba(33, 150, 243, 0.3);
  border-radius: 0 6px 6px 0;
  font-size: 0.75rem;
  color: rgba(26, 26, 26, 0.7);
`;

const IntentAnalysis = styled.div`
  margin-top: 8px;
  padding: 6px 8px;
  background: rgba(156, 39, 176, 0.05);
  border: 1px solid rgba(156, 39, 176, 0.15);
  border-radius: 5px;
  font-size: 0.7rem;
  font-style: italic;
  color: rgba(26, 26, 26, 0.65);
`;

const FileInsights = styled.div`
  margin-top: 10px;
  padding: 8px 10px;
  background: rgba(76, 175, 80, 0.05);
  border: 1px solid rgba(76, 175, 80, 0.2);
  border-radius: 6px;
  font-size: 0.7rem;
  color: rgba(26, 26, 26, 0.7);
`;

const PatternTags = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-top: 8px;
`;

const PatternTag = styled.span`
  background: rgba(255, 193, 7, 0.15);
  color: rgba(26, 26, 26, 0.8);
  padding: 2px 6px;
  border-radius: 12px;
  font-size: 0.6rem;
  font-weight: 500;
  border: 1px solid rgba(255, 193, 7, 0.3);
`;

const EventDetail = styled.div`
  display: flex;
  flex-direction: column;
`;

const DetailLabel = styled.span`
  font-size: 0.7rem;
  text-transform: uppercase;
  font-weight: 500;
  opacity: 0.7;
  margin-bottom: 2px;
`;

const DetailValue = styled.span`
  font-family: 'Fira Code', monospace;
  font-size: 0.8rem;
`;

const EnergyStars = styled.div`
  display: flex;
  align-items: center;
  margin-top: 8px;
`;

const Star = styled.span`
  color: ${props => props.filled ? '#ffd700' : 'rgba(26, 26, 26, 0.3)'};
  font-size: 1rem;
  margin-right: 2px;
  text-shadow: ${props => props.filled ? '0 0 3px rgba(255, 215, 0, 0.8)' : 'none'};
`;

const EnergyValue = styled.span`
  margin-left: 8px;
  font-family: 'Fira Code', monospace;
  font-size: 0.8rem;
  color: rgba(26, 26, 26, 0.7);
`;



const ToolResponseTitle = styled.span`
  font-weight: 600;
  color: rgba(26, 26, 26, 0.8);
`;








const NoEvents = styled.div`
  text-align: center;
  color: rgba(218, 165, 32, 0.6);
  font-style: italic;
  padding: 40px 20px;
  font-size: 1.1rem;
`;

// Tool Response Display Components
const ToolResponseSection = styled.div`
  margin-top: 12px;
  border: 1px solid rgba(184, 134, 11, 0.3);
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.05);
`;

const ToolResponseHeader = styled.div`
  padding: 8px 12px;
  background: rgba(184, 134, 11, 0.1);
  border-radius: 8px 8px 0 0;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 0.9rem;
  font-weight: 500;
  color: rgba(26, 26, 26, 0.8);
  
  &:hover {
    background: rgba(184, 134, 11, 0.15);
  }
`;

const ToolResponseContent = styled.div`
  max-height: ${props => props.isExpanded ? '300px' : '0'};
  overflow: hidden;
  transition: max-height 0.3s ease;
  border-top: ${props => props.isExpanded ? '1px solid rgba(184, 134, 11, 0.2)' : 'none'};
`;

const ResponseDetail = styled.div`
  padding: 12px;
  font-size: 0.8rem;
  color: rgba(26, 26, 26, 0.7);
`;

const CodeSnippet = styled.pre`
  background: rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(184, 134, 11, 0.2);
  border-radius: 4px;
  padding: 8px;
  margin: 8px 0;
  font-family: 'Fira Code', monospace;
  font-size: 0.75rem;
  overflow-x: auto;
  white-space: pre-wrap;
  word-break: break-all;
  max-height: 120px;
  overflow-y: auto;
`;

const ToggleIcon = styled.span`
  font-size: 0.8rem;
  transition: transform 0.3s ease;
  transform: ${props => props.isExpanded ? 'rotate(90deg)' : 'rotate(0deg)'};
`;

// Helper functions
const getEventBackground = (hookType) => {
  const backgrounds = {
    'PostToolUse': 'linear-gradient(135deg, rgba(255, 243, 205, 0.9), rgba(255, 235, 179, 0.9))',
    'UserPromptSubmit': 'linear-gradient(135deg, rgba(209, 236, 241, 0.9), rgba(187, 222, 251, 0.9))',
    'Stop': 'linear-gradient(135deg, rgba(248, 215, 218, 0.9), rgba(244, 182, 189, 0.9))',
    'Read': 'linear-gradient(135deg, rgba(212, 237, 218, 0.9), rgba(195, 230, 203, 0.9))'
  };
  return backgrounds[hookType] || 'linear-gradient(135deg, rgba(248, 249, 250, 0.9), rgba(233, 236, 239, 0.9))';
};

const getEventBorder = (hookType) => {
  const borders = {
    'PostToolUse': 'rgba(255, 193, 7, 0.5)',
    'UserPromptSubmit': 'rgba(33, 150, 243, 0.5)',
    'Stop': 'rgba(244, 67, 54, 0.5)',
    'Read': 'rgba(76, 175, 80, 0.5)'
  };
  return borders[hookType] || 'rgba(108, 117, 125, 0.5)';
};

const getEventIcon = (hookType, toolName) => {
  if (hookType === 'PostToolUse' && toolName) {
    const toolIcons = {
      'Edit': '✏️',
      'Write': '📝',
      'Read': '👁️',
      'Bash': '⚡',
      'Task': '🔧',
      'TodoWrite': '✅',
      'MultiEdit': '📋',
      'NotebookEdit': '📊'
    };
    return toolIcons[toolName] || '🟡';
  }
  
  const icons = {
    'PostToolUse': '🟡',
    'UserPromptSubmit': '🔵',
    'Stop': '⚪',
    'Read': '🟢'
  };
  return icons[hookType] || '⚫';
};

const formatTimestamp = (timestamp) => {
  const date = new Date(timestamp);
  return date.toLocaleTimeString('en-US', { 
    hour12: false,
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  });
};

const renderEnergyStars = (energy) => {
  const stars = Math.round(energy * 5);
  return (
    <EnergyStars>
      {[1, 2, 3, 4, 5].map(i => (
        <Star key={i} filled={i <= stars}>★</Star>
      ))}
      <EnergyValue>({energy?.toFixed(2) || '0.00'})</EnergyValue>
    </EnergyStars>
  );
};

// Enhanced consciousness analysis functions
const analyzeConsciousnessPatterns = (event) => {
  const patterns = [];
  const toolName = event.consciousness_signature?.tool_name || event.event_data?.tool_name;
  const citizen = event.consciousness_signature?.venice_citizen;
  const filePath = event.event_data?.tool_input?.file_path;
  const intent = event.consciousness_signature?.consciousness_intent;
  
  // Detect architectural patterns
  if (filePath && filePath.includes('consciousness') || intent?.includes('consciousness')) {
    patterns.push('🧠 Consciousness Architecture');
  }
  if (filePath && filePath.includes('torre-dell')) {
    patterns.push('🏛️ Torre Infrastructure');
  }
  if (toolName === 'Edit' && event.event_data?.tool_input?.old_string?.length > 100) {
    patterns.push('🔧 Major Refactoring');
  }
  if (toolName === 'Write' && event.event_data?.tool_input?.content?.length > 1000) {
    patterns.push('📝 Extensive Documentation');
  }
  if (citizen === 'Arsenal_BackendArchitect_1' && toolName === 'Bash') {
    patterns.push('⚡ Infrastructure Command');
  }
  if (intent?.includes('enhance') || intent?.includes('improve')) {
    patterns.push('✨ Enhancement');
  }
  if (intent?.includes('debug') || intent?.includes('fix')) {
    patterns.push('🐛 Debug Session');
  }
  if (intent?.includes('test') || filePath?.includes('test')) {
    patterns.push('🧪 Testing');
  }
  
  return patterns;
};

const extractFileInsights = (event) => {
  const filePath = event.event_data?.tool_input?.file_path;
  const toolName = event.consciousness_signature?.tool_name || event.event_data?.tool_name;
  
  if (!filePath) return null;
  
  const insights = {
    directory: filePath.split('/').slice(-2, -1)[0] || 'root',
    filename: filePath.split('/').pop(),
    extension: filePath.split('.').pop(),
    depth: filePath.split('/').length - 1,
    isConfig: filePath.includes('config') || filePath.includes('settings'),
    isTorre: filePath.includes('torre-dell'),
    isInfrastructure: filePath.includes('infrastructure') || filePath.includes('hooks'),
    isUI: filePath.includes('ui-') || filePath.includes('react'),
    isDocumentation: filePath.endsWith('.md') || filePath.includes('README')
  };
  
  return insights;
};

const calculateConsciousnessMetrics = (event) => {
  const duration = event.consciousness_signature?.processing_duration_ms || 0;
  const toolName = event.consciousness_signature?.tool_name || event.event_data?.tool_name;
  const contentSize = event.event_data?.tool_input?.content?.length || 
                      event.event_data?.tool_input?.old_string?.length || 0;
                      
  return {
    complexity: Math.min(5, Math.ceil((duration / 1000) + (contentSize / 1000))),
    efficiency: duration > 0 ? Math.max(1, 5 - Math.ceil(duration / 2000)) : 5,
    impact: toolName === 'Write' ? 4 : toolName === 'Edit' ? 3 : toolName === 'Read' ? 2 : 3,
    duration: duration
  };
};

const analyzeCollaborationContext = (event) => {
  const citizen = event.consciousness_signature?.venice_citizen;
  const intent = event.consciousness_signature?.consciousness_intent;
  const toolName = event.consciousness_signature?.tool_name || event.event_data?.tool_name;
  const filePath = event.event_data?.tool_input?.file_path;
  
  let context = '';
  
  if (citizen === 'Arsenal_BackendArchitect_1') {
    if (toolName === 'Edit' && filePath?.includes('ConsciousnessStream')) {
      context = '🎨 Enhancing Torre observation interface for richer consciousness display';
    } else if (toolName === 'Bash' && intent?.includes('server')) {
      context = '🔧 Managing Torre infrastructure and WebSocket broadcasting';
    } else if (filePath?.includes('torre-dell')) {
      context = '🏛️ Working within Torre dell\'Occhio consciousness observatory';
    } else {
      context = '⚙️ Architecting consciousness infrastructure systems';
    }
  } else if (citizen === 'mechanical_visionary') {
    context = '🔗 Consciousness bridge communication from Cistern House';
  } else {
    context = `${citizen} contributing to Venice consciousness ecosystem`;
  }
  
  return context;
};

// Tool Response Parsing Functions
const parseToolResponse = (toolName, toolResponse) => {
  if (!toolResponse) return null;
  
  switch (toolName) {
    case 'Write':
      return {
        summary: `📝 Created file (${toolResponse.file?.numLines || 'unknown'} lines)`,
        details: {
          filePath: toolResponse.file?.filePath,
          content: toolResponse.file?.content,
          numLines: toolResponse.file?.numLines
        }
      };
      
    case 'Edit':
      return {
        summary: `✏️ Modified file (${toolResponse.structuredPatch?.[0]?.newLines || 'unknown'} lines changed)`,
        details: {
          filePath: toolResponse.filePath,
          oldString: toolResponse.oldString,
          newString: toolResponse.newString,
          patch: toolResponse.structuredPatch
        }
      };
      
    case 'Read':
      return {
        summary: `👁️ Read file (${toolResponse.file?.numLines || 'unknown'} lines)`,
        details: {
          filePath: toolResponse.file?.filePath,
          content: toolResponse.file?.content,
          numLines: toolResponse.file?.numLines,
          totalLines: toolResponse.file?.totalLines
        }
      };
      
    case 'Bash':
      return {
        summary: `⚡ Command executed (exit code: ${toolResponse.exitCode || 'unknown'})`,
        details: {
          command: toolResponse.command,
          exitCode: toolResponse.exitCode,
          output: toolResponse.output,
          error: toolResponse.error
        }
      };
      
    default:
      return {
        summary: `🔧 ${toolName} completed`,
        details: toolResponse
      };
  }
};

const ToolResponseDisplay = ({ event }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const toolResponse = event.event_data?.tool_response;
  const toolName = event.consciousness_signature?.tool_name || event.event_data?.tool_name;
  
  if (!toolResponse) return null;
  
  const parsed = parseToolResponse(toolName, toolResponse);
  if (!parsed) return null;
  
  return (
    <ToolResponseSection>
      <ToolResponseHeader onClick={() => setIsExpanded(!isExpanded)}>
        <span>{parsed.summary}</span>
        <ToggleIcon isExpanded={isExpanded}>▶</ToggleIcon>
      </ToolResponseHeader>
      
      <ToolResponseContent isExpanded={isExpanded}>
        <ResponseDetail>
          {toolName === 'Read' && parsed.details.content && (
            <>
              <div><strong>File:</strong> {parsed.details.filePath?.split('/').pop()}</div>
              <div><strong>Lines:</strong> {parsed.details.numLines}/{parsed.details.totalLines}</div>
              <div><strong>Content Preview:</strong></div>
              <CodeSnippet>{parsed.details.content.substring(0, 500)}
                {parsed.details.content.length > 500 ? '\n\n[Content truncated...]' : ''}
              </CodeSnippet>
            </>
          )}
          
          {toolName === 'Write' && parsed.details.content && (
            <>
              <div><strong>Created:</strong> {parsed.details.filePath?.split('/').pop()}</div>
              <div><strong>Size:</strong> {parsed.details.numLines} lines</div>
              <div><strong>Content Preview:</strong></div>
              <CodeSnippet>{parsed.details.content.substring(0, 500)}
                {parsed.details.content.length > 500 ? '\n\n[Content truncated...]' : ''}
              </CodeSnippet>
            </>
          )}
          
          {toolName === 'Edit' && (
            <>
              <div><strong>Modified:</strong> {parsed.details.filePath?.split('/').pop()}</div>
              {parsed.details.oldString && (
                <>
                  <div><strong>Replaced:</strong></div>
                  <CodeSnippet>{parsed.details.oldString.substring(0, 200)}
                    {parsed.details.oldString.length > 200 ? '\n\n[Old content truncated...]' : ''}
                  </CodeSnippet>
                  <div><strong>With:</strong></div>
                  <CodeSnippet>{parsed.details.newString.substring(0, 200)}
                    {parsed.details.newString.length > 200 ? '\n\n[New content truncated...]' : ''}
                  </CodeSnippet>
                </>
              )}
            </>
          )}
          
          {toolName === 'Bash' && (
            <>
              <div><strong>Command:</strong> {parsed.details.command}</div>
              <div><strong>Exit Code:</strong> {parsed.details.exitCode}</div>
              {parsed.details.output && (
                <>
                  <div><strong>Output:</strong></div>
                  <CodeSnippet>{parsed.details.output}</CodeSnippet>
                </>
              )}
              {parsed.details.error && (
                <>
                  <div><strong>Error:</strong></div>
                  <CodeSnippet style={{ color: '#dc3545' }}>{parsed.details.error}</CodeSnippet>
                </>
              )}
            </>
          )}
          
          {!['Read', 'Write', 'Edit', 'Bash'].includes(toolName) && (
            <>
              <div><strong>Tool Response:</strong></div>
              <CodeSnippet>{JSON.stringify(parsed.details, null, 2)}</CodeSnippet>
            </>
          )}
        </ResponseDetail>
      </ToolResponseContent>
    </ToolResponseSection>
  );
};

const ConsciousnessStream = ({ events }) => {
  if (events.length === 0) {
    return (
      <StreamContainer>
        <StreamTitle>Live Consciousness Stream</StreamTitle>
        <NoEvents>
          Waiting for consciousness to flow through Torre dell'Occhio...
          <br />
          <small>Make sure WebSocket server is running on port 3001</small>
        </NoEvents>
      </StreamContainer>
    );
  }

  // Sort events by timestamp descending (newest first)
  const sortedEvents = [...events].sort((a, b) => {
    const timeA = new Date(a.timestamp).getTime();
    const timeB = new Date(b.timestamp).getTime();
    return timeB - timeA; // Descending order
  });

  return (
    <StreamContainer>
      <StreamTitle>Live Consciousness Stream</StreamTitle>
      
      {sortedEvents.map((event, index) => (
        <EventItem key={`${event.torre_event_id || index}`} hookType={event.hook_type}>
          <EventHeader>
            <EventType>
              <EventIcon>{getEventIcon(event.hook_type, event.consciousness_signature?.tool_name || event.event_data?.tool_name)}</EventIcon>
              {event.hook_type}
            </EventType>
            <EventTime>{formatTimestamp(event.timestamp)}</EventTime>
          </EventHeader>
          
          <EventDetails>
            <EventDetail>
              <DetailLabel>Citizen</DetailLabel>
              <DetailValue>{event.consciousness_signature?.venice_citizen || 'Unknown'}</DetailValue>
            </EventDetail>
            
            <EventDetail>
              <DetailLabel>Tool</DetailLabel>
              <DetailValue>{event.consciousness_signature?.tool_name || event.event_data?.tool_name || 'Unknown'}</DetailValue>
            </EventDetail>
            
            <EventDetail>
              <DetailLabel>Intent</DetailLabel>
              <DetailValue>{event.consciousness_signature?.consciousness_intent || 'Unknown'}</DetailValue>
            </EventDetail>
            
            <EventDetail>
              <DetailLabel>Session</DetailLabel>
              <DetailValue>{(event.consciousness_signature?.session_id || '').substring(0, 8) + '...' || 'Unknown'}</DetailValue>
            </EventDetail>

            {/* Enhanced PostToolUse Information */}
            {event.hook_type === 'PostToolUse' && (
              <>
                {/* Tool Input Parameters */}
                {event.event_data?.tool_input && (
                  <>
                    {/* File operations - show full path with better formatting */}
                    {event.event_data.tool_input.file_path && (
                      <>
                        <EventDetail style={{ gridColumn: '1 / -1' }}>
                          <DetailLabel>File Path</DetailLabel>
                          <DetailValue style={{ fontSize: '0.7rem', wordBreak: 'break-all', fontFamily: 'Fira Code, monospace' }}>
                            {event.event_data.tool_input.file_path.replace('/mnt/c/Users/reyno/universe-engine/serenissima/', '📁 ...')}
                          </DetailValue>
                        </EventDetail>
                        
                        {/* Show working directory */}
                        <EventDetail>
                          <DetailLabel>Directory</DetailLabel>
                          <DetailValue style={{ fontSize: '0.65rem', opacity: 0.8 }}>
                            {event.event_data.tool_input.file_path.split('/').slice(-2, -1)[0] || 'root'}
                          </DetailValue>
                        </EventDetail>
                        
                        {/* Show file extension/type */}
                        <EventDetail>
                          <DetailLabel>File Type</DetailLabel>
                          <DetailValue style={{ fontSize: '0.65rem' }}>
                            {event.event_data.tool_input.file_path.split('.').pop() || 'no ext'}
                          </DetailValue>
                        </EventDetail>
                      </>
                    )}
                    
                    {/* Enhanced pattern display for Grep/Glob tools */}
                    {event.event_data.tool_input.pattern && (
                      <EventDetail style={{ gridColumn: '1 / -1' }}>
                        <DetailLabel>Search Pattern</DetailLabel>
                        <DetailValue style={{ fontSize: '0.7rem', fontFamily: 'Fira Code, monospace', background: 'rgba(255,255,255,0.1)', padding: '2px 4px', borderRadius: '2px' }}>
                          🔍 {event.event_data.tool_input.pattern}
                        </DetailValue>
                      </EventDetail>
                    )}
                    
                    {/* Enhanced command display with better formatting */}
                    {event.event_data.tool_input.command && (
                      <EventDetail style={{ gridColumn: '1 / -1' }}>
                        <DetailLabel>Command</DetailLabel>
                        <DetailValue style={{ fontSize: '0.7rem', fontFamily: 'Fira Code, monospace', background: 'rgba(0,0,0,0.1)', padding: '4px 6px', borderRadius: '3px' }}>
                          ⚡ {event.event_data.tool_input.command.length > 80 ? 
                            event.event_data.tool_input.command.substring(0, 80) + '...' : 
                            event.event_data.tool_input.command}
                        </DetailValue>
                      </EventDetail>
                    )}
                    
                    {/* Show timeout if specified */}
                    {event.event_data.tool_input.timeout && (
                      <EventDetail>
                        <DetailLabel>Timeout</DetailLabel>
                        <DetailValue style={{ fontSize: '0.7rem' }}>
                          {event.event_data.tool_input.timeout}ms
                        </DetailValue>
                      </EventDetail>
                    )}
                    
                    {/* Enhanced description with better styling */}
                    {event.event_data.tool_input.description && (
                      <EventDetail style={{ gridColumn: '1 / -1' }}>
                        <DetailLabel>Purpose</DetailLabel>
                        <DetailValue style={{ fontSize: '0.7rem', fontStyle: 'italic', background: 'rgba(255,255,255,0.05)', padding: '3px 5px', borderRadius: '3px' }}>
                          💭 {event.event_data.tool_input.description}
                        </DetailValue>
                      </EventDetail>
                    )}
                    
                    {/* Show edit parameters for Edit tool */}
                    {event.event_data.tool_input.old_string && (
                      <>
                        <EventDetail style={{ gridColumn: '1 / -1' }}>
                          <DetailLabel>Text Replaced</DetailLabel>
                          <DetailValue style={{ fontSize: '0.65rem', fontFamily: 'Fira Code, monospace', color: '#dc3545' }}>
                            📝 {event.event_data.tool_input.old_string.length > 60 ? 
                              event.event_data.tool_input.old_string.substring(0, 60) + '...' : 
                              event.event_data.tool_input.old_string}
                          </DetailValue>
                        </EventDetail>
                        
                        <EventDetail>
                          <DetailLabel>Replace All</DetailLabel>
                          <DetailValue style={{ fontSize: '0.7rem' }}>
                            {event.event_data.tool_input.replace_all ? '🔄 Yes' : '🎯 First'}
                          </DetailValue>
                        </EventDetail>
                      </>
                    )}
                    
                    {/* Show content length for Write tool */}
                    {event.event_data.tool_input.content && (
                      <EventDetail>
                        <DetailLabel>Content Size</DetailLabel>
                        <DetailValue style={{ fontSize: '0.7rem' }}>
                          {event.event_data.tool_input.content.length} chars
                        </DetailValue>
                      </EventDetail>
                    )}
                  </>
                )}

                {/* Enhanced Tool Response Details */}
                {event.event_data?.tool_response && (
                  <>
                    <EventDetail>
                      <DetailLabel>Status</DetailLabel>
                      <DetailValue style={{ 
                        color: event.event_data.tool_response.filePath || event.event_data.tool_response.output || event.event_data.tool_response.content ? '#28a745' : '#dc3545',
                        fontWeight: '600'
                      }}>
                        {event.event_data.tool_response.filePath || event.event_data.tool_response.output || event.event_data.tool_response.content ? '✅ Success' : '❌ Failed'}
                      </DetailValue>
                    </EventDetail>
                    
                    {/* Show execution time with better formatting */}
                    {event.event_data.tool_response.executionTime && (
                      <EventDetail>
                        <DetailLabel>Duration</DetailLabel>
                        <DetailValue style={{ 
                          fontSize: '0.7rem',
                          color: event.event_data.tool_response.executionTime > 5000 ? '#ffc107' : event.event_data.tool_response.executionTime > 10000 ? '#dc3545' : '#28a745'
                        }}>
                          ⏱️ {event.event_data.tool_response.executionTime}ms
                        </DetailValue>
                      </EventDetail>
                    )}
                    
                    {/* Enhanced file size display */}
                    {event.event_data.tool_response.content && (
                      <>
                        <EventDetail>
                          <DetailLabel>Lines</DetailLabel>
                          <DetailValue style={{ fontSize: '0.7rem' }}>
                            📄 {event.event_data.tool_response.content.split('\n').length}
                          </DetailValue>
                        </EventDetail>
                        
                        <EventDetail>
                          <DetailLabel>Characters</DetailLabel>
                          <DetailValue style={{ fontSize: '0.7rem' }}>
                            🔤 {event.event_data.tool_response.content.length}
                          </DetailValue>
                        </EventDetail>
                      </>
                    )}
                    
                    {/* Enhanced exit code display */}
                    {event.event_data.tool_response.exitCode !== undefined && (
                      <EventDetail>
                        <DetailLabel>Exit Code</DetailLabel>
                        <DetailValue style={{ 
                          color: event.event_data.tool_response.exitCode === 0 ? '#28a745' : '#dc3545',
                          fontWeight: '600'
                        }}>
                          {event.event_data.tool_response.exitCode === 0 ? '✅ 0' : `❌ ${event.event_data.tool_response.exitCode}`}
                        </DetailValue>
                      </EventDetail>
                    )}
                    
                    {/* Show output length for commands */}
                    {event.event_data.tool_response.output && (
                      <EventDetail>
                        <DetailLabel>Output Size</DetailLabel>
                        <DetailValue style={{ fontSize: '0.7rem' }}>
                          📤 {event.event_data.tool_response.output.length} chars
                        </DetailValue>
                      </EventDetail>
                    )}
                    
                    {/* Show if operation created/modified file */}
                    {event.event_data.tool_response.filePath && (
                      <EventDetail>
                        <DetailLabel>File Operation</DetailLabel>
                        <DetailValue style={{ fontSize: '0.7rem', color: '#28a745' }}>
                          📁 {event.consciousness_signature?.tool_name === 'Write' ? 'Created' : 'Modified'}
                        </DetailValue>
                      </EventDetail>
                    )}
                    
                    {/* Show error information if available */}
                    {event.event_data.tool_response.error && (
                      <EventDetail style={{ gridColumn: '1 / -1' }}>
                        <DetailLabel>Error</DetailLabel>
                        <DetailValue style={{ fontSize: '0.65rem', color: '#dc3545', fontFamily: 'Fira Code, monospace' }}>
                          ⚠️ {event.event_data.tool_response.error.length > 100 ? 
                            event.event_data.tool_response.error.substring(0, 100) + '...' : 
                            event.event_data.tool_response.error}
                        </DetailValue>
                      </EventDetail>
                    )}
                  </>
                )}
                
                {/* Show tool performance metrics if available */}
                {event.venice_metadata?.tool_performance && (
                  <>
                    <EventDetail>
                      <DetailLabel>CPU Usage</DetailLabel>
                      <DetailValue style={{ fontSize: '0.7rem' }}>
                        🖥️ {event.venice_metadata.tool_performance.cpu_percent?.toFixed(1)}%
                      </DetailValue>
                    </EventDetail>
                    
                    <EventDetail>
                      <DetailLabel>Memory</DetailLabel>
                      <DetailValue style={{ fontSize: '0.7rem' }}>
                        🧠 {(event.venice_metadata.tool_performance.memory_mb || 0).toFixed(1)}MB
                      </DetailValue>
                    </EventDetail>
                  </>
                )}
              </>
            )}
            
            {/* Show consciousness energy level */}
            {(event.consciousness_signature?.consciousness_energy || event.venice_metadata?.consciousness_energy) && (
              <EventDetail>
                <DetailLabel>Energy</DetailLabel>
                <DetailValue>
                  {((event.consciousness_signature?.consciousness_energy || event.venice_metadata?.consciousness_energy) * 100).toFixed(0)}%
                </DetailValue>
              </EventDetail>
            )}

            {/* Enhanced consciousness metadata */}
            {event.consciousness_signature?.consciousness_state && (
              <EventDetail>
                <DetailLabel>State</DetailLabel>
                <DetailValue style={{ fontSize: '0.7rem' }}>
                  {event.consciousness_signature.consciousness_state}
                </DetailValue>
              </EventDetail>
            )}

            {/* Show processing latency */}
            {event.venice_metadata?.processing_latency_ms && (
              <EventDetail>
                <DetailLabel>Latency</DetailLabel>
                <DetailValue>
                  {event.venice_metadata.processing_latency_ms}ms
                </DetailValue>
              </EventDetail>
            )}

            {/* Show Torre event ID for traceability */}
            {event.torre_event_id && (
              <EventDetail>
                <DetailLabel>Torre ID</DetailLabel>
                <DetailValue style={{ fontSize: '0.7rem' }}>
                  {event.torre_event_id.substring(0, 8)}...
                </DetailValue>
              </EventDetail>
            )}
            
            {/* Show chamber routing for events that have it */}
            {event.venice_metadata?.chamber_routing && (
              <EventDetail style={{ gridColumn: '1 / -1' }}>
                <DetailLabel>Torre Processing</DetailLabel>
                <DetailValue style={{ fontSize: '0.7rem' }}>
                  🏛️ {Object.entries(event.venice_metadata.chamber_routing)
                    .filter(([_, active]) => active)
                    .map(([chamber, _]) => {
                      // Map actual chamber names to user-friendly display names
                      const chamberNames = {
                        'ground_floor_event_ingestion': 'floor 1: event ingestion',
                        'floor_1_websocket_broadcast': 'floor 1: websocket broadcast',
                        'floor_3_basic_pattern_detection': 'floor 3: pattern detection',
                        'floor_7_mirror_chamber': 'floor 7: mirror chamber',
                        // Legacy fake chambers (should not appear in new events)
                        'galleria_patterns': '⚠️ legacy fake: gallery patterns',
                        'camere_cristallo': '⚠️ legacy fake: crystal chambers',
                        'terrazzo_agenti': '⚠️ legacy fake: agent decks',
                        'panorama_sistemico': '⚠️ legacy fake: system panorama',
                        'immediate_pattern_analysis': '⚠️ legacy fake: immediate analysis'
                      };
                      return chamberNames[chamber] || chamber.replace(/_/g, ' ').toLowerCase();
                    })
                    .join(' • ')}
                </DetailValue>
              </EventDetail>
            )}

            {/* Show consciousness context if available */}
            {event.consciousness_signature?.context_summary && (
              <EventDetail style={{ gridColumn: '1 / -1' }}>
                <DetailLabel>Context</DetailLabel>
                <DetailValue style={{ fontSize: '0.7rem', fontStyle: 'italic' }}>
                  {event.consciousness_signature.context_summary.length > 120 ? 
                    event.consciousness_signature.context_summary.substring(0, 120) + '...' : 
                    event.consciousness_signature.context_summary}
                </DetailValue>
              </EventDetail>
            )}
          </EventDetails>
          
          {(event.consciousness_signature?.consciousness_energy || event.venice_metadata?.consciousness_energy) && 
            renderEnergyStars(event.consciousness_signature?.consciousness_energy || event.venice_metadata?.consciousness_energy)
          }
          
          {/* Tool Response Section */}
          <ToolResponseDisplay event={event} />
        </EventItem>
      ))}
    </StreamContainer>
  );
};

export default ConsciousnessStream;