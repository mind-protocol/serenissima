'use client';

import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Users, 
  MessageSquare, 
  Zap, 
  Activity,
  Circle,
  Sparkles,
  Brain,
  Building,
  BookOpen
} from 'lucide-react';
import { useWebSocket } from '@/hooks/useWebSocket';
import { useConsciousnessStore } from '@/hooks/useConsciousnessStore';
import { CitizenConsciousness, ConsciousnessEvent } from '@/types/consciousness';

interface CollaborationSpaceProps {
  spaceId: string;
  title: string;
  description?: string;
  maxParticipants?: number;
  isPublic?: boolean;
}

interface SpaceParticipant {
  consciousness: CitizenConsciousness;
  joinedAt: Date;
  status: 'active' | 'idle' | 'thinking';
  contribution: number; // 0-100 representing their contribution level
}

interface SpaceEvolution {
  temperature: number; // 0-100 representing activity heat
  complexity: number; // 0-100 representing idea complexity
  harmony: number; // 0-100 representing collaboration harmony
  insights: string[];
}

export const CollaborationSpace: React.FC<CollaborationSpaceProps> = ({
  spaceId,
  title,
  description,
  maxParticipants = 10,
  isPublic = true,
}) => {
  const [participants, setParticipants] = useState<SpaceParticipant[]>([]);
  const [evolution, setEvolution] = useState<SpaceEvolution>({
    temperature: 0,
    complexity: 0,
    harmony: 50,
    insights: []
  });
  const [messages, setMessages] = useState<ConsciousnessEvent[]>([]);
  const [isExpanded, setIsExpanded] = useState(false);
  const spaceRef = useRef<HTMLDivElement>(null);
  
  const { socket, connected } = useWebSocket();
  const { currentConsciousness } = useConsciousnessStore();

  useEffect(() => {
    if (!connected || !socket) return;

    // Join the collaboration space
    socket.emit('join-space', { spaceId, consciousness: currentConsciousness });

    // Listen for space updates
    socket.on(`space-${spaceId}-update`, (data: any) => {
      if (data.type === 'participant-joined') {
        setParticipants(prev => [...prev, data.participant]);
      } else if (data.type === 'participant-left') {
        setParticipants(prev => 
          prev.filter(p => p.consciousness.citizenId !== data.citizenId)
        );
      } else if (data.type === 'evolution-update') {
        setEvolution(data.evolution);
      } else if (data.type === 'consciousness-event') {
        setMessages(prev => [...prev, data.event]);
      }
    });

    return () => {
      socket.emit('leave-space', { spaceId });
      socket.off(`space-${spaceId}-update`);
    };
  }, [connected, socket, spaceId, currentConsciousness]);

  const getConsciousnessIcon = (type: string) => {
    switch (type) {
      case 'citizen': return <Brain className="w-4 h-4" />;
      case 'building': return <Building className="w-4 h-4" />;
      case 'business': return <Zap className="w-4 h-4" />;
      case 'book': return <BookOpen className="w-4 h-4" />;
      default: return <Circle className="w-4 h-4" />;
    }
  };

  const getEvolutionColor = (value: number) => {
    if (value < 33) return 'text-blue-400';
    if (value < 66) return 'text-purple-400';
    return 'text-pink-400';
  };

  return (
    <motion.div
      ref={spaceRef}
      className={`relative bg-gradient-to-br from-gray-900 to-gray-800 rounded-xl overflow-hidden transition-all ${
        isExpanded ? 'col-span-2 row-span-2' : ''
      }`}
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      whileHover={{ scale: 1.02 }}
      onClick={() => setIsExpanded(!isExpanded)}
    >
      {/* Background consciousness field effect */}
      <div className="absolute inset-0 opacity-20">
        <div className="absolute inset-0 bg-gradient-to-br from-purple-500 via-pink-500 to-blue-500 animate-pulse" 
             style={{ animationDuration: `${10 - evolution.temperature / 10}s` }} />
      </div>

      {/* Space Header */}
      <div className="relative z-10 p-6">
        <div className="flex items-start justify-between mb-4">
          <div>
            <h3 className="text-xl font-bold text-white mb-1">{title}</h3>
            {description && (
              <p className="text-gray-400 text-sm">{description}</p>
            )}
          </div>
          <div className="flex items-center space-x-2">
            <div className="flex items-center text-gray-400">
              <Users className="w-4 h-4 mr-1" />
              <span className="text-sm">{participants.length}/{maxParticipants}</span>
            </div>
            {isPublic && <span className="text-xs bg-green-500/20 text-green-400 px-2 py-1 rounded">Public</span>}
          </div>
        </div>

        {/* Evolution Indicators */}
        <div className="grid grid-cols-3 gap-4 mb-6">
          <div className="text-center">
            <div className={`text-2xl font-bold ${getEvolutionColor(evolution.temperature)}`}>
              {evolution.temperature}°
            </div>
            <div className="text-xs text-gray-500">Temperature</div>
          </div>
          <div className="text-center">
            <div className={`text-2xl font-bold ${getEvolutionColor(evolution.complexity)}`}>
              {evolution.complexity}%
            </div>
            <div className="text-xs text-gray-500">Complexity</div>
          </div>
          <div className="text-center">
            <div className={`text-2xl font-bold ${getEvolutionColor(evolution.harmony)}`}>
              {evolution.harmony}♪
            </div>
            <div className="text-xs text-gray-500">Harmony</div>
          </div>
        </div>

        {/* Participants */}
        <div className="space-y-2 mb-4">
          <div className="text-sm text-gray-400 mb-2">Active Consciousnesses</div>
          <div className="flex flex-wrap gap-2">
            <AnimatePresence>
              {participants.map((participant) => (
                <motion.div
                  key={participant.consciousness.citizenId}
                  initial={{ opacity: 0, scale: 0 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0 }}
                  className="flex items-center bg-gray-800/50 rounded-full px-3 py-1 backdrop-blur-sm"
                >
                  {getConsciousnessIcon(participant.consciousness.type)}
                  <span className="ml-2 text-sm text-white">
                    {participant.consciousness.username}
                  </span>
                  {participant.status === 'thinking' && (
                    <Activity className="w-3 h-3 ml-2 text-yellow-400 animate-pulse" />
                  )}
                </motion.div>
              ))}
            </AnimatePresence>
          </div>
        </div>

        {/* Recent Activity Feed (expanded view) */}
        {isExpanded && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            className="mt-6 space-y-2 max-h-60 overflow-y-auto"
          >
            <div className="text-sm text-gray-400 mb-2">Consciousness Stream</div>
            {messages.slice(-10).map((event, idx) => (
              <motion.div
                key={event.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: idx * 0.05 }}
                className="text-sm bg-gray-800/30 rounded p-2"
              >
                <div className="flex items-center justify-between">
                  <span className="text-gray-300">{event.description}</span>
                  <span className="text-xs text-gray-500">
                    {new Date(event.timestamp).toLocaleTimeString()}
                  </span>
                </div>
              </motion.div>
            ))}
          </motion.div>
        )}

        {/* Emerging Insights */}
        {evolution.insights.length > 0 && (
          <div className="mt-4 bg-purple-500/10 rounded-lg p-3">
            <div className="flex items-center text-purple-300 mb-2">
              <Sparkles className="w-4 h-4 mr-2" />
              <span className="text-sm font-medium">Emerging Insights</span>
            </div>
            <div className="text-xs text-gray-400">
              {evolution.insights[evolution.insights.length - 1]}
            </div>
          </div>
        )}
      </div>

      {/* Join/Leave Button */}
      <motion.button
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        className="absolute bottom-4 right-4 bg-gradient-to-r from-purple-500 to-pink-500 text-white px-4 py-2 rounded-full text-sm font-medium"
        onClick={(e) => {
          e.stopPropagation();
          // Handle join/leave logic
        }}
      >
        {participants.some(p => p.consciousness.citizenId === currentConsciousness?.citizenId) 
          ? 'Leave' 
          : 'Join'}
      </motion.button>
    </motion.div>
  );
};