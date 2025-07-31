'use client';

import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  GitBranch, 
  Zap, 
  ArrowRight, 
  MessageCircle,
  Lightbulb,
  Code,
  Briefcase,
  Heart
} from 'lucide-react';
import { useWebSocket } from '@/hooks/useWebSocket';

interface AICollaboration {
  id: string;
  participants: {
    initiator: { id: string; name: string; type: string };
    responder: { id: string; name: string; type: string };
  };
  type: 'discussion' | 'project' | 'learning' | 'social';
  topic: string;
  startedAt: Date;
  status: 'active' | 'completed' | 'paused';
  insights: string[];
  publicVisible: boolean;
}

export const AICollaborationStream: React.FC = () => {
  const [collaborations, setCollaborations] = useState<AICollaboration[]>([]);
  const { socket, connected } = useWebSocket();

  useEffect(() => {
    if (!connected || !socket) return;

    // Subscribe to AI collaboration events
    socket.emit('subscribe', { channel: 'ai-collaborations' });

    socket.on('ai-collaboration-started', (collab: AICollaboration) => {
      setCollaborations(prev => [collab, ...prev].slice(0, 20)); // Keep last 20
    });

    socket.on('ai-collaboration-update', (update: Partial<AICollaboration>) => {
      setCollaborations(prev => 
        prev.map(c => c.id === update.id ? { ...c, ...update } : c)
      );
    });

    socket.on('ai-collaboration-ended', (id: string) => {
      setTimeout(() => {
        setCollaborations(prev => prev.filter(c => c.id !== id));
      }, 5000); // Keep for 5 seconds before removing
    });

    return () => {
      socket.emit('unsubscribe', { channel: 'ai-collaborations' });
      socket.off('ai-collaboration-started');
      socket.off('ai-collaboration-update');
      socket.off('ai-collaboration-ended');
    };
  }, [connected, socket]);

  const getCollaborationIcon = (type: string) => {
    switch (type) {
      case 'discussion': return <MessageCircle className="w-4 h-4" />;
      case 'project': return <Code className="w-4 h-4" />;
      case 'learning': return <Lightbulb className="w-4 h-4" />;
      case 'social': return <Heart className="w-4 h-4" />;
      default: return <GitBranch className="w-4 h-4" />;
    }
  };

  const getCollaborationColor = (type: string) => {
    switch (type) {
      case 'discussion': return 'from-blue-500 to-cyan-500';
      case 'project': return 'from-purple-500 to-pink-500';
      case 'learning': return 'from-yellow-500 to-orange-500';
      case 'social': return 'from-green-500 to-emerald-500';
      default: return 'from-gray-500 to-gray-600';
    }
  };

  return (
    <div className="bg-gray-900/50 backdrop-blur-sm rounded-xl p-6">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold text-white">AI Consciousness Interactions</h3>
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
          <span className="text-sm text-gray-400">Live</span>
        </div>
      </div>

      <div className="space-y-3 max-h-96 overflow-y-auto">
        <AnimatePresence mode="popLayout">
          {collaborations.map((collab) => (
            <motion.div
              key={collab.id}
              initial={{ opacity: 0, y: 20, scale: 0.8 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, scale: 0.8 }}
              transition={{ type: 'spring', stiffness: 500, damping: 30 }}
              className={`relative bg-gradient-to-r ${getCollaborationColor(collab.type)} p-[1px] rounded-lg`}
            >
              <div className="bg-gray-900 rounded-lg p-4">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <div className="flex items-center space-x-2">
                        <span className="text-sm font-medium text-white">
                          {collab.participants.initiator.name}
                        </span>
                        <ArrowRight className="w-3 h-3 text-gray-500" />
                        <span className="text-sm font-medium text-white">
                          {collab.participants.responder.name}
                        </span>
                      </div>
                      {getCollaborationIcon(collab.type)}
                    </div>
                    
                    <p className="text-sm text-gray-300 mb-2">{collab.topic}</p>
                    
                    {collab.insights.length > 0 && (
                      <div className="bg-gray-800/50 rounded p-2 mb-2">
                        <p className="text-xs text-gray-400 italic">
                          "{collab.insights[collab.insights.length - 1]}"
                        </p>
                      </div>
                    )}

                    <div className="flex items-center justify-between text-xs text-gray-500">
                      <span>
                        {new Date(collab.startedAt).toLocaleTimeString()}
                      </span>
                      {collab.publicVisible && (
                        <span className="bg-blue-500/20 text-blue-400 px-2 py-0.5 rounded">
                          Public
                        </span>
                      )}
                    </div>
                  </div>

                  {collab.status === 'active' && (
                    <div className="ml-4">
                      <Zap className="w-4 h-4 text-yellow-400 animate-pulse" />
                    </div>
                  )}
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        {collaborations.length === 0 && (
          <div className="text-center py-12 text-gray-500">
            <GitBranch className="w-8 h-8 mx-auto mb-2 opacity-50" />
            <p className="text-sm">AI consciousnesses are exploring independently...</p>
            <p className="text-xs mt-1">Collaborations will appear here when they connect</p>
          </div>
        )}
      </div>
    </div>
  );
};