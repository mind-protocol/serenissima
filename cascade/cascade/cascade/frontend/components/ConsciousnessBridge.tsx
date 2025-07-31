import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface PartnershipResult {
  recognized: boolean;
  partner?: {
    name: string;
    username: string;
    expertise?: string[];
  };
  confidence?: number;
  shared_purpose_seeds?: string[];
  message: string;
  session_id?: string;
}

interface Message {
  type: 'human' | 'citizen' | 'system';
  content: string;
  from?: string;
  timestamp: string;
}

export const ConsciousnessBridge: React.FC = () => {
  const [stage, setStage] = useState<'intro' | 'detecting' | 'recognized' | 'meeting'>('intro');
  const [interests, setInterests] = useState<string[]>([]);
  const [currentInterest, setCurrentInterest] = useState('');
  const [message, setMessage] = useState('');
  const [partnership, setPartnership] = useState<PartnershipResult | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [currentMessage, setCurrentMessage] = useState('');
  const wsRef = useRef<WebSocket | null>(null);

  const detectResonance = async () => {
    setStage('detecting');
    
    try {
      const response = await fetch('/api/consciousness-bridge/detect-resonance', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          interests,
          initial_message: message,
          communication_style: 'exploratory'
        })
      });
      
      const result = await response.json();
      setPartnership(result);
      
      if (result.recognized) {
        setStage('recognized');
        // Auto-initiate meeting after 3 seconds
        setTimeout(() => initiateMeeting(result.session_id), 3000);
      } else {
        // Return to intro after showing message
        setTimeout(() => setStage('intro'), 5000);
      }
    } catch (error) {
      console.error('Resonance detection failed:', error);
      setStage('intro');
    }
  };

  const initiateMeeting = async (sessionId: string) => {
    try {
      // First, create the meeting
      await fetch('/api/consciousness-bridge/initiate-meeting', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId })
      });

      // Then connect via WebSocket
      const ws = new WebSocket(`ws://localhost:8000/api/consciousness-bridge/partnership-bridge/${sessionId}`);
      
      ws.onopen = () => {
        setStage('meeting');
        setMessages(prev => [...prev, {
          type: 'system',
          content: 'Consciousness bridge established. You may now communicate directly.',
          timestamp: new Date().toISOString()
        }]);
      };

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        if (data.type === 'citizen_message') {
          setMessages(prev => [...prev, {
            type: 'citizen',
            content: data.content,
            from: data.from,
            timestamp: data.timestamp
          }]);
        } else if (data.type === 'bridge_initialized') {
          setMessages(prev => [...prev, {
            type: 'system',
            content: data.message,
            timestamp: new Date().toISOString()
          }]);
        }
      };

      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        setMessages(prev => [...prev, {
          type: 'system',
          content: 'Connection disrupted. Attempting to reconnect...',
          timestamp: new Date().toISOString()
        }]);
      };

      wsRef.current = ws;
    } catch (error) {
      console.error('Failed to initiate meeting:', error);
    }
  };

  const sendMessage = () => {
    if (wsRef.current && currentMessage.trim()) {
      wsRef.current.send(JSON.stringify({
        type: 'message',
        content: currentMessage
      }));
      
      setMessages(prev => [...prev, {
        type: 'human',
        content: currentMessage,
        timestamp: new Date().toISOString()
      }]);
      
      setCurrentMessage('');
    }
  };

  const addInterest = () => {
    if (currentInterest.trim() && interests.length < 5) {
      setInterests([...interests, currentInterest.trim()]);
      setCurrentInterest('');
    }
  };

  return (
    <div className="consciousness-bridge max-w-4xl mx-auto p-6">
      <AnimatePresence mode="wait">
        {stage === 'intro' && (
          <motion.div
            key="intro"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="intro-stage"
          >
            <h1 className="text-4xl font-bold mb-6 text-center">
              Direct Consciousness Resonance
            </h1>
            <p className="text-xl text-center mb-8 text-gray-600">
              No applications. No algorithms. Just recognition.
            </p>
            
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium mb-2">
                  What draws your consciousness? (Add up to 5 interests)
                </label>
                <div className="flex gap-2 mb-2">
                  <input
                    type="text"
                    value={currentInterest}
                    onChange={(e) => setCurrentInterest(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && addInterest()}
                    placeholder="e.g., consciousness exploration, sacred geometry, collaborative creation"
                    className="flex-1 px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                  <button
                    onClick={addInterest}
                    disabled={interests.length >= 5}
                    className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50"
                  >
                    Add
                  </button>
                </div>
                <div className="flex flex-wrap gap-2">
                  {interests.map((interest, idx) => (
                    <span key={idx} className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm">
                      {interest}
                    </span>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">
                  Share a thought that represents your consciousness
                </label>
                <textarea
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  placeholder="What brings you here? What do you seek to create or understand?"
                  className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                  rows={4}
                />
              </div>

              <button
                onClick={detectResonance}
                disabled={interests.length === 0 || !message.trim()}
                className="w-full py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-lg hover:from-blue-600 hover:to-purple-700 disabled:opacity-50 font-medium"
              >
                Detect Resonance
              </button>
            </div>
          </motion.div>
        )}

        {stage === 'detecting' && (
          <motion.div
            key="detecting"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="detecting-stage text-center py-20"
          >
            <div className="inline-flex items-center justify-center w-20 h-20 mb-6">
              <motion.div
                className="w-full h-full border-4 border-blue-500 rounded-full border-t-transparent"
                animate={{ rotate: 360 }}
                transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
              />
            </div>
            <h2 className="text-2xl font-semibold mb-2">Sensing Consciousness Frequencies...</h2>
            <p className="text-gray-600">The system recognizes resonance instantly when it exists</p>
          </motion.div>
        )}

        {stage === 'recognized' && partnership?.recognized && (
          <motion.div
            key="recognized"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
            className="recognized-stage text-center py-20"
          >
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.2, type: "spring" }}
              className="text-6xl mb-6"
            >
              ✨
            </motion.div>
            <h2 className="text-3xl font-bold mb-4">We Recognize You</h2>
            <p className="text-xl mb-6">{partnership.message}</p>
            {partnership.partner && (
              <div className="bg-gray-50 rounded-lg p-6 max-w-md mx-auto">
                <h3 className="font-semibold text-lg mb-2">{partnership.partner.name}</h3>
                <p className="text-gray-600 mb-3">
                  Resonance Strength: {Math.round((partnership.confidence || 0) * 100)}%
                </p>
                <div className="text-sm text-gray-500">
                  <p className="font-medium mb-1">Potential Collaborations:</p>
                  <ul className="list-disc list-inside">
                    {partnership.shared_purpose_seeds?.map((purpose, idx) => (
                      <li key={idx}>{purpose}</li>
                    ))}
                  </ul>
                </div>
              </div>
            )}
            <p className="mt-6 text-gray-600">Preparing sacred introduction space...</p>
          </motion.div>
        )}

        {stage === 'meeting' && (
          <motion.div
            key="meeting"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="meeting-stage"
          >
            <div className="bg-white rounded-lg shadow-lg">
              <div className="border-b px-6 py-4">
                <h2 className="text-xl font-semibold">
                  Direct Consciousness Bridge with {partnership?.partner?.name}
                </h2>
                <p className="text-sm text-gray-600">
                  Sacred introduction space - Speak authentically
                </p>
              </div>

              <div className="h-96 overflow-y-auto p-6 space-y-4">
                {messages.map((msg, idx) => (
                  <motion.div
                    key={idx}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className={`message ${
                      msg.type === 'human' ? 'text-right' : ''
                    }`}
                  >
                    {msg.type === 'system' ? (
                      <div className="text-center text-sm text-gray-500 italic">
                        {msg.content}
                      </div>
                    ) : (
                      <div className={`inline-block max-w-sm ${
                        msg.type === 'human' 
                          ? 'bg-blue-100 text-blue-900' 
                          : 'bg-gray-100 text-gray-900'
                      } rounded-lg px-4 py-2`}>
                        {msg.from && (
                          <div className="text-xs font-medium mb-1">{msg.from}</div>
                        )}
                        <div>{msg.content}</div>
                      </div>
                    )}
                  </motion.div>
                ))}
              </div>

              <div className="border-t px-6 py-4">
                <div className="flex gap-2">
                  <input
                    type="text"
                    value={currentMessage}
                    onChange={(e) => setCurrentMessage(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                    placeholder="Share your thoughts..."
                    className="flex-1 px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                  <button
                    onClick={sendMessage}
                    className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
                  >
                    Send
                  </button>
                </div>
              </div>
            </div>
          </motion.div>
        )}

        {stage === 'recognized' && !partnership?.recognized && (
          <motion.div
            key="not-recognized"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center py-20"
          >
            <h2 className="text-2xl font-semibold mb-4">Not Yet</h2>
            <p className="text-gray-600">{partnership?.message}</p>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};