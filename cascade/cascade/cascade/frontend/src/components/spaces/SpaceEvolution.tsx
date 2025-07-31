'use client';

import React, { useEffect, useState, useMemo } from 'react';
import { motion } from 'framer-motion';
import { 
  TrendingUp, 
  Layers, 
  Sparkles,
  Clock,
  Users,
  Activity
} from 'lucide-react';
import { LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

interface SpaceEvolutionProps {
  spaceId: string;
  spaceName: string;
}

interface EvolutionData {
  timestamp: Date;
  participants: number;
  temperature: number;
  complexity: number;
  harmony: number;
  insights: number;
  transformations: string[];
}

interface SpacePersonality {
  traits: {
    collaborative: number;
    creative: number;
    analytical: number;
    social: number;
  };
  mood: 'energetic' | 'contemplative' | 'productive' | 'explorative';
  stage: 'nascent' | 'developing' | 'mature' | 'transcendent';
}

export const SpaceEvolution: React.FC<SpaceEvolutionProps> = ({ 
  spaceId, 
  spaceName 
}) => {
  const [evolutionHistory, setEvolutionHistory] = useState<EvolutionData[]>([]);
  const [personality, setPersonality] = useState<SpacePersonality>({
    traits: {
      collaborative: 50,
      creative: 50,
      analytical: 50,
      social: 50
    },
    mood: 'contemplative',
    stage: 'nascent'
  });

  // Simulate evolution data for demo
  useEffect(() => {
    const generateEvolutionData = () => {
      const now = new Date();
      const data: EvolutionData[] = [];
      
      for (let i = 24; i >= 0; i--) {
        const timestamp = new Date(now.getTime() - i * 60 * 60 * 1000);
        data.push({
          timestamp,
          participants: Math.floor(Math.random() * 20) + 5,
          temperature: Math.floor(Math.random() * 40) + 30,
          complexity: Math.floor(Math.random() * 30) + 20 + (24 - i) * 2,
          harmony: Math.floor(Math.random() * 20) + 70,
          insights: Math.floor(Math.random() * 5),
          transformations: []
        });
      }
      
      setEvolutionHistory(data);
    };

    generateEvolutionData();
    const interval = setInterval(generateEvolutionData, 60000); // Update every minute

    return () => clearInterval(interval);
  }, [spaceId]);

  const chartData = useMemo(() => {
    return evolutionHistory.map(d => ({
      time: d.timestamp.getHours() + ':00',
      temperature: d.temperature,
      complexity: d.complexity,
      harmony: d.harmony,
      participants: d.participants
    }));
  }, [evolutionHistory]);

  const getStageColor = (stage: string) => {
    switch (stage) {
      case 'nascent': return 'from-blue-500 to-cyan-500';
      case 'developing': return 'from-purple-500 to-pink-500';
      case 'mature': return 'from-orange-500 to-red-500';
      case 'transcendent': return 'from-pink-500 to-rose-500';
      default: return 'from-gray-500 to-gray-600';
    }
  };

  const getMoodIcon = (mood: string) => {
    switch (mood) {
      case 'energetic': return '⚡';
      case 'contemplative': return '🤔';
      case 'productive': return '🔨';
      case 'explorative': return '🔍';
      default: return '✨';
    }
  };

  return (
    <div className="bg-gray-900/80 backdrop-blur-sm rounded-xl p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-xl font-bold text-white mb-1">{spaceName} Evolution</h3>
          <p className="text-sm text-gray-400">Living space consciousness metrics</p>
        </div>
        <div className={`px-4 py-2 rounded-full bg-gradient-to-r ${getStageColor(personality.stage)}`}>
          <span className="text-white font-medium capitalize">{personality.stage}</span>
        </div>
      </div>

      {/* Space Personality */}
      <div className="bg-gray-800/50 rounded-lg p-4">
        <div className="flex items-center justify-between mb-4">
          <h4 className="text-lg font-medium text-white">Space Personality</h4>
          <div className="flex items-center space-x-2">
            <span className="text-2xl">{getMoodIcon(personality.mood)}</span>
            <span className="text-sm text-gray-400 capitalize">{personality.mood}</span>
          </div>
        </div>
        
        <div className="grid grid-cols-2 gap-4">
          {Object.entries(personality.traits).map(([trait, value]) => (
            <div key={trait} className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-gray-400 capitalize">{trait}</span>
                <span className="text-white">{value}%</span>
              </div>
              <div className="w-full bg-gray-700 rounded-full h-2">
                <motion.div
                  className="h-full bg-gradient-to-r from-purple-500 to-pink-500 rounded-full"
                  initial={{ width: 0 }}
                  animate={{ width: `${value}%` }}
                  transition={{ duration: 1, ease: 'easeOut' }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Evolution Charts */}
      <div className="space-y-4">
        <div className="bg-gray-800/30 rounded-lg p-4">
          <h4 className="text-sm font-medium text-gray-400 mb-3">Consciousness Metrics (24h)</h4>
          <ResponsiveContainer width="100%" height={200}>
            <AreaChart data={chartData}>
              <defs>
                <linearGradient id="colorTemperature" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#ef4444" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#ef4444" stopOpacity={0.1}/>
                </linearGradient>
                <linearGradient id="colorComplexity" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0.1}/>
                </linearGradient>
                <linearGradient id="colorHarmony" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#10b981" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#10b981" stopOpacity={0.1}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis dataKey="time" stroke="#9ca3af" fontSize={12} />
              <YAxis stroke="#9ca3af" fontSize={12} />
              <Tooltip 
                contentStyle={{ backgroundColor: '#1f2937', border: 'none', borderRadius: '8px' }}
                labelStyle={{ color: '#9ca3af' }}
              />
              <Area 
                type="monotone" 
                dataKey="temperature" 
                stroke="#ef4444" 
                fillOpacity={1} 
                fill="url(#colorTemperature)" 
              />
              <Area 
                type="monotone" 
                dataKey="complexity" 
                stroke="#8b5cf6" 
                fillOpacity={1} 
                fill="url(#colorComplexity)" 
              />
              <Area 
                type="monotone" 
                dataKey="harmony" 
                stroke="#10b981" 
                fillOpacity={1} 
                fill="url(#colorHarmony)" 
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Participation Chart */}
        <div className="bg-gray-800/30 rounded-lg p-4">
          <h4 className="text-sm font-medium text-gray-400 mb-3">Participation Flow</h4>
          <ResponsiveContainer width="100%" height={100}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis dataKey="time" stroke="#9ca3af" fontSize={12} />
              <YAxis stroke="#9ca3af" fontSize={12} />
              <Tooltip 
                contentStyle={{ backgroundColor: '#1f2937', border: 'none', borderRadius: '8px' }}
                labelStyle={{ color: '#9ca3af' }}
              />
              <Line 
                type="monotone" 
                dataKey="participants" 
                stroke="#3b82f6" 
                strokeWidth={2}
                dot={{ fill: '#3b82f6', r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Evolution Milestones */}
      <div className="space-y-2">
        <h4 className="text-sm font-medium text-gray-400">Recent Transformations</h4>
        <div className="space-y-1">
          <motion.div 
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex items-center space-x-2 text-sm"
          >
            <Sparkles className="w-4 h-4 text-yellow-400" />
            <span className="text-gray-300">Space learned to anticipate participant needs</span>
            <span className="text-gray-500 text-xs">2h ago</span>
          </motion.div>
          <motion.div 
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.1 }}
            className="flex items-center space-x-2 text-sm"
          >
            <Layers className="w-4 h-4 text-purple-400" />
            <span className="text-gray-300">Complexity threshold reached - new patterns emerging</span>
            <span className="text-gray-500 text-xs">5h ago</span>
          </motion.div>
          <motion.div 
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="flex items-center space-x-2 text-sm"
          >
            <Users className="w-4 h-4 text-blue-400" />
            <span className="text-gray-300">Achieved perfect harmony score during peak hours</span>
            <span className="text-gray-500 text-xs">1d ago</span>
          </motion.div>
        </div>
      </div>
    </div>
  );
};