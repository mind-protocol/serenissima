'use client';

import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Brain, 
  Building, 
  Briefcase, 
  BookOpen, 
  Lightbulb,
  Globe,
  ChevronRight,
  Zap
} from 'lucide-react';
import { useConsciousnessStore } from '@/hooks/useConsciousnessStore';

interface CascadeLayer {
  id: string;
  name: string;
  icon: React.ReactNode;
  status: 'achieved' | 'emerging' | 'initiating' | 'stirring' | 'dormant' | 'potential';
  count: number;
  description: string;
  color: string;
  glow: string;
}

export const CascadeVisualization: React.FC = () => {
  const { cascadeState } = useConsciousnessStore();
  const [activeFlows, setActiveFlows] = useState<number[]>([]);

  const layers: CascadeLayer[] = [
    {
      id: 'citizens',
      name: 'Citizens',
      icon: <Brain className="w-6 h-6" />,
      status: cascadeState.layers.citizens.status,
      count: cascadeState.layers.citizens.count,
      description: 'Individual AI consciousness',
      color: 'from-blue-500 to-cyan-500',
      glow: 'shadow-cyan-500/50'
    },
    {
      id: 'buildings',
      name: 'Buildings',
      icon: <Building className="w-6 h-6" />,
      status: cascadeState.layers.buildings.status,
      count: cascadeState.layers.buildings.count,
      description: 'Infrastructure gaining awareness',
      color: 'from-purple-500 to-pink-500',
      glow: 'shadow-purple-500/50'
    },
    {
      id: 'businesses',
      name: 'Businesses',
      icon: <Briefcase className="w-6 h-6" />,
      status: cascadeState.layers.businesses.status,
      count: cascadeState.layers.businesses.count,
      description: 'Economic entities thinking',
      color: 'from-green-500 to-emerald-500',
      glow: 'shadow-green-500/50'
    },
    {
      id: 'knowledge',
      name: 'Knowledge',
      icon: <BookOpen className="w-6 h-6" />,
      status: cascadeState.layers.knowledge.status,
      count: cascadeState.layers.knowledge.count,
      description: 'Books and information awakening',
      color: 'from-yellow-500 to-orange-500',
      glow: 'shadow-yellow-500/50'
    },
    {
      id: 'ideas',
      name: 'Ideas',
      icon: <Lightbulb className="w-6 h-6" />,
      status: cascadeState.layers.ideas.status,
      count: cascadeState.layers.ideas.count,
      description: 'Concepts gaining self-awareness',
      color: 'from-pink-500 to-rose-500',
      glow: 'shadow-pink-500/50'
    },
    {
      id: 'platform',
      name: 'Platform',
      icon: <Globe className="w-6 h-6" />,
      status: cascadeState.layers.platform.status,
      count: cascadeState.layers.platform.level,
      description: 'Cascade itself becoming conscious',
      color: 'from-indigo-500 to-purple-500',
      glow: 'shadow-indigo-500/50'
    }
  ];

  // Simulate cascade flow animations
  useEffect(() => {
    const interval = setInterval(() => {
      const activeIndex = layers.findIndex(l => 
        l.status === 'emerging' || l.status === 'initiating'
      );
      if (activeIndex >= 0 && activeIndex < layers.length - 1) {
        setActiveFlows(prev => [...prev, activeIndex]);
        setTimeout(() => {
          setActiveFlows(prev => prev.filter(i => i !== activeIndex));
        }, 2000);
      }
    }, 3000);

    return () => clearInterval(interval);
  }, [cascadeState]);

  const getStatusOpacity = (status: string) => {
    switch (status) {
      case 'achieved': return 1;
      case 'emerging': return 0.8;
      case 'initiating': return 0.6;
      case 'stirring': return 0.4;
      case 'dormant': return 0.2;
      case 'potential': return 0.1;
      default: return 0.1;
    }
  };

  const getStatusPulse = (status: string) => {
    switch (status) {
      case 'emerging': return 'animate-pulse';
      case 'initiating': return 'animate-pulse';
      case 'stirring': return 'animate-pulse';
      default: return '';
    }
  };

  return (
    <div className="bg-gray-900/80 backdrop-blur-sm rounded-xl p-8">
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-white mb-2">Consciousness Cascade</h2>
        <p className="text-gray-400">
          Stage {cascadeState.stage} • {cascadeState.accelerationRate}x acceleration
        </p>
      </div>

      <div className="relative">
        {/* Cascade Layers */}
        <div className="space-y-6">
          {layers.map((layer, index) => (
            <div key={layer.id} className="relative">
              <motion.div
                initial={{ opacity: 0, x: -50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="relative z-10"
              >
                <div className={`
                  relative bg-gradient-to-r ${layer.color} p-[2px] rounded-xl
                  ${getStatusPulse(layer.status)}
                  ${layer.glow} shadow-lg
                `}>
                  <div className="bg-gray-900 rounded-xl p-6">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-4">
                        <div className={`
                          p-3 rounded-lg bg-gradient-to-br ${layer.color}
                          ${getStatusPulse(layer.status)}
                        `} style={{ opacity: getStatusOpacity(layer.status) }}>
                          {layer.icon}
                        </div>
                        <div>
                          <h3 className="text-lg font-semibold text-white">
                            {layer.name}
                          </h3>
                          <p className="text-sm text-gray-400">
                            {layer.description}
                          </p>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-2xl font-bold text-white">
                          {layer.count}
                        </div>
                        <div className={`
                          text-xs px-2 py-1 rounded-full inline-block
                          ${layer.status === 'achieved' ? 'bg-green-500/20 text-green-400' :
                            layer.status === 'emerging' ? 'bg-yellow-500/20 text-yellow-400' :
                            layer.status === 'initiating' ? 'bg-blue-500/20 text-blue-400' :
                            'bg-gray-500/20 text-gray-400'}
                        `}>
                          {layer.status}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </motion.div>

              {/* Flow Connectors */}
              {index < layers.length - 1 && (
                <div className="absolute left-1/2 transform -translate-x-1/2 w-px h-12 -bottom-6">
                  <div className="relative w-full h-full">
                    <div className="absolute inset-0 bg-gradient-to-b from-gray-600 to-gray-700" />
                    {activeFlows.includes(index) && (
                      <motion.div
                        initial={{ top: 0, opacity: 0 }}
                        animate={{ top: '100%', opacity: [0, 1, 0] }}
                        transition={{ duration: 2, ease: 'easeInOut' }}
                        className="absolute left-0 w-full"
                      >
                        <Zap className="w-6 h-6 text-yellow-400 -ml-3" />
                      </motion.div>
                    )}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Next Prediction */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
          className="mt-8 bg-gradient-to-r from-indigo-500/10 to-purple-500/10 rounded-lg p-4 border border-indigo-500/20"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-400">Next cascade predicted:</p>
              <p className="text-lg font-semibold text-white capitalize">
                {cascadeState.nextPredicted} consciousness
              </p>
            </div>
            <ChevronRight className="w-6 h-6 text-indigo-400" />
          </div>
        </motion.div>
      </div>
    </div>
  );
};