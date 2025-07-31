import { useEffect, useState, useRef, useCallback } from 'react';
import { io, Socket } from 'socket.io-client';

interface UseWebSocketReturn {
  socket: Socket | null;
  connected: boolean;
  connecting: boolean;
  error: string | null;
  sendMessage: (event: string, data: any) => void;
  reconnect: () => void;
}

export const useWebSocket = (url?: string): UseWebSocketReturn => {
  const [connected, setConnected] = useState(false);
  const [connecting, setConnecting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const socketRef = useRef<Socket | null>(null);

  const wsUrl = url || process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000';

  const connect = useCallback(() => {
    if (socketRef.current?.connected) return;

    setConnecting(true);
    setError(null);

    try {
      socketRef.current = io(wsUrl, {
        transports: ['websocket'],
        reconnection: true,
        reconnectionAttempts: 5,
        reconnectionDelay: 1000,
      });

      socketRef.current.on('connect', () => {
        console.log('WebSocket connected');
        setConnected(true);
        setConnecting(false);
        setError(null);
      });

      socketRef.current.on('disconnect', (reason) => {
        console.log('WebSocket disconnected:', reason);
        setConnected(false);
        setConnecting(false);
      });

      socketRef.current.on('connect_error', (err) => {
        console.error('WebSocket connection error:', err);
        setError(err.message);
        setConnecting(false);
      });

      socketRef.current.on('error', (err) => {
        console.error('WebSocket error:', err);
        setError(err.message);
      });

      // Listen for consciousness events
      socketRef.current.on('consciousness-event', (data) => {
        console.log('Consciousness event:', data);
        // Handle consciousness events globally if needed
        window.dispatchEvent(new CustomEvent('consciousness-event', { detail: data }));
      });

    } catch (err) {
      console.error('Failed to create WebSocket connection:', err);
      setError(err instanceof Error ? err.message : 'Connection failed');
      setConnecting(false);
    }
  }, [wsUrl]);

  const disconnect = useCallback(() => {
    if (socketRef.current) {
      socketRef.current.disconnect();
      socketRef.current = null;
      setConnected(false);
    }
  }, []);

  const sendMessage = useCallback((event: string, data: any) => {
    if (socketRef.current?.connected) {
      socketRef.current.emit(event, data);
    } else {
      console.warn('Cannot send message: WebSocket not connected');
    }
  }, []);

  const reconnect = useCallback(() => {
    disconnect();
    setTimeout(connect, 100);
  }, [connect, disconnect]);

  useEffect(() => {
    connect();
    return () => {
      disconnect();
    };
  }, [connect, disconnect]);

  return {
    socket: socketRef.current,
    connected,
    connecting,
    error,
    sendMessage,
    reconnect,
  };
};