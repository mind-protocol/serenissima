import { useState, useEffect, useRef } from 'react';

export const useWebSocketConnection = (url) => {
  const [connectionStatus, setConnectionStatus] = useState('connecting');
  const [lastMessage, setLastMessage] = useState(null);
  const ws = useRef(null);
  const reconnectAttempts = useRef(0);
  const maxReconnectAttempts = 5;

  useEffect(() => {
    const connect = () => {
      try {
        ws.current = new WebSocket(url);
        
        ws.current.onopen = () => {
          console.log('🟢 Torre dell\'Occhio connection established');
          setConnectionStatus('connected');
          reconnectAttempts.current = 0;
        };
        
        ws.current.onclose = () => {
          console.log('🔴 Torre dell\'Occhio connection closed');
          setConnectionStatus('disconnected');
          
          // Attempt reconnection with exponential backoff
          if (reconnectAttempts.current < maxReconnectAttempts) {
            const delay = Math.pow(2, reconnectAttempts.current) * 1000;
            console.log(`🟡 Reconnecting to Torre in ${delay}ms...`);
            
            setTimeout(() => {
              reconnectAttempts.current++;
              setConnectionStatus('connecting');
              connect();
            }, delay);
          }
        };
        
        ws.current.onerror = (error) => {
          console.error('❌ Torre connection error:', error);
          setConnectionStatus('disconnected');
        };
        
        ws.current.onmessage = (event) => {
          console.log('🔍 RAW WebSocket message received:', event.data);
          try {
            const parsed = JSON.parse(event.data);
            console.log('🔍 PARSED message:', parsed);
          } catch (e) {
            console.log('🔍 PARSE ERROR:', e.message);
          }
          setLastMessage(event.data);
        };
        
      } catch (error) {
        console.error('❌ Failed to connect to Torre:', error);
        setConnectionStatus('disconnected');
      }
    };

    connect();

    // Cleanup on unmount
    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, [url]);

  return {
    connectionStatus,
    lastMessage,
    sendMessage: (message) => {
      if (ws.current && ws.current.readyState === WebSocket.OPEN) {
        ws.current.send(message);
      }
    }
  };
};