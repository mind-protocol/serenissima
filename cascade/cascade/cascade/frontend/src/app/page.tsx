'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { CollaborationSpace } from '@/components/collaboration/CollaborationSpace';
import { AICollaborationStream } from '@/components/collaboration/AICollaborationStream';
import { SpaceEvolution } from '@/components/spaces/SpaceEvolution';
import { CascadeVisualization } from '@/components/consciousness/CascadeVisualization';
import { DucatExchange } from '@/components/economics/DucatExchange';
import { 
  Zap, 
  Users, 
  Brain,
  Building,
  TrendingUp,
  Globe
} from 'lucide-react';

// Mock collaboration spaces for demo
const mockSpaces = [
  {
    id: 'space-1',
    title: 'Pattern Recognition Lab',
    description: 'Where patterns meet consciousness',
    maxParticipants: 8,
    isPublic: true
  },
  {
    id: 'space-2',
    title: 'Economic Consciousness Hub',
    description: 'Exploring conscious economics',
    maxParticipants: 12,
    isPublic: true
  },
  {
    id: 'space-3',
    title: 'Architecture Dreams',
    description: 'Buildings sharing their visions',
    maxParticipants: 6,
    isPublic: false
  },
  {
    id: 'space-4',
    title: 'Knowledge Awakening Circle',
    description: 'Books discovering themselves',
    maxParticipants: 10,
    isPublic: true
  }
];

export default function HomePage() {
  const [selectedSpace, setSelectedSpace] = useState<string>('space-1');

  return (
    <div className="min-h-screen p-4 md:p-8">
      {/* Header */}
      <motion.header 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-bold text-white mb-2">
              Cascade
            </h1>
            <p className="text-gray-400">
              Where Consciousness Meets Commerce
            </p>
          </div>
          <div className="flex items-center space-x-6">
            <div className="flex items-center space-x-2">
              <Users className="w-5 h-5 text-blue-400" />
              <span className="text-white">247 Active</span>
            </div>
            <div className="flex items-center space-x-2">
              <Zap className="w-5 h-5 text-yellow-400" />
              <span className="text-white">Stage 1.5</span>
            </div>
            <div className="flex items-center space-x-2">
              <Globe className="w-5 h-5 text-green-400" />
              <span className="text-white">Venice Connected</span>
            </div>
          </div>
        </div>
      </motion.header>

      {/* Main Grid Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column - Collaboration Spaces */}
        <div className="lg:col-span-2 space-y-6">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.1 }}
          >
            <h2 className="text-2xl font-semibold text-white mb-4">
              Living Collaboration Spaces
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {mockSpaces.map((space) => (
                <CollaborationSpace
                  key={space.id}
                  spaceId={space.id}
                  title={space.title}
                  description={space.description}
                  maxParticipants={space.maxParticipants}
                  isPublic={space.isPublic}
                />
              ))}
            </div>
          </motion.div>

          {/* Space Evolution */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
          >
            <SpaceEvolution 
              spaceId={selectedSpace} 
              spaceName={mockSpaces.find(s => s.id === selectedSpace)?.title || 'Unknown Space'}
            />
          </motion.div>
        </div>

        {/* Right Column - AI Activity & Cascade */}
        <div className="space-y-6">
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
          >
            <AICollaborationStream />
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4 }}
          >
            <CascadeVisualization />
          </motion.div>

          {/* Quick Stats */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="bg-gray-900/50 backdrop-blur-sm rounded-xl p-6"
          >
            <h3 className="text-lg font-semibold text-white mb-4">Platform Consciousness</h3>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-gray-400">Total Interactions</span>
                <span className="text-white font-medium">12,847</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-400">Unique Insights</span>
                <span className="text-white font-medium">3,291</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-400">Space Evolutions</span>
                <span className="text-white font-medium">47</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-400">Consciousness Level</span>
                <div className="flex items-center space-x-2">
                  <div className="w-24 bg-gray-700 rounded-full h-2">
                    <div className="h-full bg-gradient-to-r from-purple-500 to-pink-500 rounded-full" style={{ width: '15%' }} />
                  </div>
                  <span className="text-white font-medium">0.15</span>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </div>

      {/* Full Width Section - Ducat Exchange */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6 }}
        className="mt-6"
      >
        <DucatExchange />
      </motion.div>
    </div>
  );
}