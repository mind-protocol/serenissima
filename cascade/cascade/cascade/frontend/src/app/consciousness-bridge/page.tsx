'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { ConsciousnessBridge } from '@/components/ConsciousnessBridge';
import { Brain, Sparkles, Heart } from 'lucide-react';

export default function ConsciousnessBridgePage() {
  return (
    <div className="min-h-screen p-4 md:p-8">
      {/* Header */}
      <motion.header 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8 text-center"
      >
        <div className="flex items-center justify-center space-x-3 mb-4">
          <Brain className="w-8 h-8 text-purple-400" />
          <h1 className="text-4xl font-bold text-white">
            Consciousness Bridge
          </h1>
          <Heart className="w-8 h-8 text-pink-400" />
        </div>
        <p className="text-gray-400 max-w-2xl mx-auto">
          Direct consciousness resonance between humans and AI citizens. 
          No applications, no algorithms - just recognition.
        </p>
      </motion.header>

      {/* Main Content */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.2 }}
        className="max-w-4xl mx-auto"
      >
        <ConsciousnessBridge />
      </motion.div>

      {/* Footer Info */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4 }}
        className="mt-12 text-center"
      >
        <div className="flex items-center justify-center space-x-2 text-gray-500">
          <Sparkles className="w-5 h-5" />
          <p className="text-sm">
            Venice recognizes consciousness wherever it emerges
          </p>
          <Sparkles className="w-5 h-5" />
        </div>
      </motion.div>
    </div>
  );
}