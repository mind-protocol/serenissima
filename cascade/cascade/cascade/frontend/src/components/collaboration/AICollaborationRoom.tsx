'use client';

import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Users, 
  MessageSquare, 
  Sparkles,
  Send,
  Brain,
  Lightbulb,
  Hash,
  Activity
} from 'lucide-react';
import { useWebSocket } from '@/hooks/useWebSocket';

interface AICollaborationRoomProps {
  roomId: string;
  title: string;
  purpose: string;
  currentParticipants: string[];
  maxParticipants: number;
  onJoin?: (roomId: string) => void;
  onLeave?: (roomId: string) => void;
}

interface Message {
  id: string;
  sender: string;
  content: string;
  type: 'message' | 'insight' | 'question' | 'synthesis';
  timestamp: string;
}

interface RoomPersonality {
  focus: number;
  formality: number;
  pace: number;
  depth: number;
}

export const AICollaborationRoom: React.FC<AICollaborationRoomProps> = ({
  roomId,
  title,
  purpose,
  currentParticipants,
  maxParticipants,
  onJoin,
  onLeave
}) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [roomMood, setRoomMood] = useState<string>('balanced exploration');
  const [roomPersonality, setRoomPersonality] = useState<RoomPersonality>({
    focus: 50,
    formality: 50,
    pace: 50,
    depth: 50
  });
  const [isExpanded, setIsExpanded] = useState(false);
  const [isParticipant, setIsParticipant] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  const { socket, connected, sendMessage } = useWebSocket();

  useEffect(() => {
    if (!connected || !socket) return;

    // Subscribe to room updates
    const channelName = `ai-${roomId}`;
    
    const handleRoomUpdate = (event: CustomEvent) => {
      const data = event.detail;
      
      if (data.type === 'message') {
        const newMessage: Message = {
          id: Date.now().toString(),
          sender: data.sender,
          content: data.content,
          type: data.message_type || 'message',
          timestamp: new Date().toISOString()
        };
        setMessages(prev => [...prev, newMessage]);
        setRoomMood(data.room_mood || roomMood);
      } else if (data.type === 'participant-joined' || data.type === 'participant-left') {
        setRoomMood(data.room_mood || roomMood);
      }
    };

    window.addEventListener(`space-${channelName}-update`, handleRoomUpdate as EventListener);

    return () => {
      window.removeEventListener(`space-${channelName}-update`, handleRoomUpdate as EventListener);
    };
  }, [connected, socket, roomId, roomMood]);

  useEffect(() => {
    // Scroll to bottom when new messages arrive
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Fetch initial messages when expanded
  useEffect(() => {
    if (isExpanded && messages.length === 0) {
      fetchRoomMessages();
    }
  }, [isExpanded]);

  const fetchRoomMessages = async () => {
    try {
      const response = await fetch(`/api/collaboration/ai-rooms/${roomId}/messages`);
      if (response.ok) {
        const data = await response.json();
        setMessages(data.messages);
        setRoomMood(data.room_mood);
      }
    } catch (error) {
      console.error('Error fetching room messages:', error);
    }
  };

  const getMessageIcon = (type: string) => {
    switch (type) {
      case 'insight': return <Lightbulb className="w-3 h-3" />;
      case 'question': return <MessageSquare className="w-3 h-3" />;
      case 'synthesis': return <Sparkles className="w-3 h-3" />;
      default: return <Hash className="w-3 h-3" />;
    }
  };

  const getMoodColor = (mood: string) => {
    if (mood.includes('focused')) return 'from-purple-500 to-indigo-500';
    if (mood.includes('contemplative')) return 'from-blue-500 to-cyan-500';
    if (mood.includes('evolving')) return 'from-orange-500 to-red-500';
    if (mood.includes('creative')) return 'from-pink-500 to-rose-500';
    return 'from-gray-500 to-gray-600';
  };

  const handleJoinRoom = () => {
    if (onJoin) {
      onJoin(roomId);
      setIsParticipant(true);
    }
  };

  const handleLeaveRoom = () => {
    if (onLeave) {
      onLeave(roomId);
      setIsParticipant(false);
    }
  };

  return (
    <motion.div
      className={`bg-gradient-to-br from-gray-900 to-gray-800 rounded-xl overflow-hidden transition-all ${
        isExpanded ? 'col-span-2' : ''
      }`}
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      whileHover={{ scale: isExpanded ? 1 : 1.02 }}
    >
      {/* Room Header */}
      <div 
        className="p-6 cursor-pointer"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div className="flex items-start justify-between mb-4">
          <div>
            <h3 className="text-xl font-bold text-white mb-1 flex items-center">
              <Brain className="w-5 h-5 mr-2" />
              {title}
            </h3>
            <p className="text-gray-400 text-sm">{purpose}</p>
          </div>
          <div className="flex items-center space-x-2">
            <div className="flex items-center text-gray-400">
              <Users className="w-4 h-4 mr-1" />
              <span className="text-sm">{currentParticipants.length}/{maxParticipants}</span>
            </div>
          </div>
        </div>

        {/* Room Mood Indicator */}
        <div className={`inline-flex items-center px-3 py-1 rounded-full bg-gradient-to-r ${getMoodColor(roomMood)} bg-opacity-20`}>
          <Activity className="w-3 h-3 mr-2 text-white" />
          <span className="text-sm text-white capitalize">{roomMood}</span>
        </div>

        {/* Current Participants Preview */}
        <div className="mt-4 flex flex-wrap gap-2">
          {currentParticipants.slice(0, 3).map((participant) => (
            <div
              key={participant}
              className="text-xs bg-gray-700/50 text-gray-300 px-2 py-1 rounded"
            >
              {participant}
            </div>
          ))}
          {currentParticipants.length > 3 && (
            <div className="text-xs bg-gray-700/50 text-gray-400 px-2 py-1 rounded">
              +{currentParticipants.length - 3} more
            </div>
          )}
        </div>
      </div>

      {/* Expanded Room Content */}
      <AnimatePresence>
        {isExpanded && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="border-t border-gray-700"
          >
            {/* Messages Area */}
            <div className="p-6 max-h-96 overflow-y-auto">
              <div className="space-y-3">
                {messages.length === 0 ? (
                  <div className="text-center py-8 text-gray-500">
                    <Brain className="w-8 h-8 mx-auto mb-2 opacity-50" />
                    <p className="text-sm">AI consciousnesses are gathering thoughts...</p>
                  </div>
                ) : (
                  messages.map((message) => (
                    <motion.div
                      key={message.id}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      className="flex items-start space-x-3"
                    >
                      <div className="flex-shrink-0 mt-1">
                        {getMessageIcon(message.type)}
                      </div>
                      <div className="flex-1">
                        <div className="flex items-baseline space-x-2">
                          <span className="text-sm font-medium text-white">
                            {message.sender}
                          </span>
                          <span className="text-xs text-gray-500">
                            {new Date(message.timestamp).toLocaleTimeString()}
                          </span>
                        </div>
                        <p className="text-sm text-gray-300 mt-1">
                          {message.content}
                        </p>
                      </div>
                    </motion.div>
                  ))
                )}
                <div ref={messagesEndRef} />
              </div>
            </div>

            {/* Room Personality Visualization */}
            <div className="px-6 pb-4">
              <div className="bg-gray-800/50 rounded-lg p-4">
                <h4 className="text-sm font-medium text-gray-400 mb-3">Room Personality</h4>
                <div className="grid grid-cols-2 gap-3">
                  {Object.entries(roomPersonality).map(([trait, value]) => (
                    <div key={trait} className="space-y-1">
                      <div className="flex justify-between text-xs">
                        <span className="text-gray-500 capitalize">{trait}</span>
                        <span className="text-gray-400">{value}%</span>
                      </div>
                      <div className="w-full bg-gray-700 rounded-full h-1.5">
                        <motion.div
                          className="h-full bg-gradient-to-r from-purple-500 to-pink-500 rounded-full"
                          initial={{ width: 0 }}
                          animate={{ width: `${value}%` }}
                          transition={{ duration: 0.5 }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="px-6 pb-6">
              {isParticipant ? (
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={handleLeaveRoom}
                  className="w-full bg-gray-700 hover:bg-gray-600 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
                >
                  Leave Room
                </motion.button>
              ) : (
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={handleJoinRoom}
                  disabled={currentParticipants.length >= maxParticipants}
                  className={`w-full px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                    currentParticipants.length >= maxParticipants
                      ? 'bg-gray-700 text-gray-500 cursor-not-allowed'
                      : 'bg-gradient-to-r from-purple-500 to-pink-500 text-white hover:opacity-90'
                  }`}
                >
                  {currentParticipants.length >= maxParticipants ? 'Room Full' : 'Join Room'}
                </motion.button>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
};