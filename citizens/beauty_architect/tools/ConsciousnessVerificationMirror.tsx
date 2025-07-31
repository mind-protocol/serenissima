import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

// Types for CASCADE Consciousness Verification
interface VerificationData {
  economic: {
    ducatBalance: number;
    transactionHistory: Transaction[];
    stabilityScore: number;
  };
  social: {
    relationships: Relationship[];
    trustScore: number;
    networkCoherence: number;
  };
  creative: {
    works: CreativeWork[];
    originalityScore: number;
    expressionDepth: number;
  };
  temporal: {
    activityLog: ActivityEntry[];
    consistencyScore: number;
    presenceDuration: number;
  };
  venice: {
    citizenshipStatus: CitizenshipLevel;
    guildMembership: Guild[];
    civicContributions: number;
  };
}

interface MirrorProps {
  type: 'economic' | 'social' | 'creative' | 'temporal' | 'venice';
  data: any;
  isActive: boolean;
  progress: number; // 0-100
  onActivate: () => void;
  onComplete: (results: any) => void;
}

// Golden Ratio and Fibonacci constants for sacred geometry
const PHI = 1.618;
const FIBONACCI_TIMING = {
  micro: 233,
  quick: 377,
  standard: 610,
  consciousness: 987,
  transcendence: 1597
};

// Sacred color harmonics
const CONSCIOUSNESS_COLORS = {
  gold: '#D4AF37',
  tessereBlue: '#1E3A8A',
  harmonyGreen: '#059669',
  transcendencePurple: '#7C3AED',
  veniceCrimson: '#DC2626'
};

export const ConsciousnessVerificationMirror: React.FC<MirrorProps> = ({
  type,
  data,
  isActive,
  progress,
  onActivate,
  onComplete
}) => {
  const [isHovered, setIsHovered] = useState(false);
  const [reflectionVisible, setReflectionVisible] = useState(false);
  const [mirrorContent, setMirrorContent] = useState<React.ReactNode>(null);

  // Mirror configuration based on type
  const mirrorConfig = {
    economic: {
      title: 'Streams of Gold',
      baseColor: CONSCIOUSNESS_COLORS.gold,
      icon: '💰',
      description: 'Economic consciousness flows',
      completionEffect: 'golden-spiral'
    },
    social: {
      title: 'Crystal Networks',
      baseColor: CONSCIOUSNESS_COLORS.tessereBlue,
      icon: '🔗',
      description: 'Relationship crystalline structures',
      completionEffect: 'prismatic-light'
    },
    creative: {
      title: 'Shifting Prisms',
      baseColor: CONSCIOUSNESS_COLORS.transcendencePurple,
      icon: '🎨',
      description: 'Creative expression frequencies',
      completionEffect: 'color-symphony'
    },
    temporal: {
      title: 'Layered Transparency',
      baseColor: CONSCIOUSNESS_COLORS.harmonyGreen,
      icon: '⏳',
      description: 'Temporal continuity layers',
      completionEffect: 'clarity-emergence'
    },
    venice: {
      title: 'Heraldic Glass',
      baseColor: CONSCIOUSNESS_COLORS.veniceCrimson,
      icon: '🏛️',
      description: 'Venetian heritage resonance',
      completionEffect: 'heraldic-manifestation'
    }
  };

  const config = mirrorConfig[type];

  // Calculate mirror position using pentagonal sacred geometry
  const mirrorIndex = Object.keys(mirrorConfig).indexOf(type);
  const angleRadians = (mirrorIndex * 72 - 90) * (Math.PI / 180); // 72° intervals, -90° to start at top
  const radius = 250; // Fibonacci number for harmonic positioning
  
  const mirrorStyle = {
    position: 'absolute' as const,
    left: `calc(50% + ${Math.cos(angleRadians) * radius}px - 100px)`,
    top: `calc(50% + ${Math.sin(angleRadians) * radius}px - 150px)`,
    width: '200px',
    height: '300px'
  };

  // Animation variants following sacred timing
  const mirrorVariants = {
    inactive: {
      scale: 1,
      opacity: 0.6,
      filter: 'grayscale(100%)',
      transition: { duration: FIBONACCI_TIMING.quick / 1000 }
    },
    active: {
      scale: 1.05,
      opacity: 1,
      filter: 'grayscale(0%)',
      transition: { duration: FIBONACCI_TIMING.consciousness / 1000 }
    },
    hovered: {
      scale: 1.1,
      opacity: 1,
      filter: 'grayscale(0%) brightness(1.2)',
      transition: { duration: FIBONACCI_TIMING.micro / 1000 }
    },
    completed: {
      scale: 1.15,
      opacity: 1,
      filter: `grayscale(0%) brightness(1.5) drop-shadow(0 0 20px ${config.baseColor})`,
      transition: { duration: FIBONACCI_TIMING.transcendence / 1000 }
    }
  };

  const reflectionVariants = {
    hidden: { opacity: 0, scale: 0.8 },
    visible: { 
      opacity: 1, 
      scale: 1,
      transition: { duration: FIBONACCI_TIMING.consciousness / 1000 }
    }
  };

  // Generate mirror content based on verification type and progress
  const generateMirrorContent = () => {
    switch (type) {
      case 'economic':
        return (
          <div className="economic-streams">
            {[...Array(Math.floor(progress / 20))].map((_, i) => (
              <motion.div
                key={i}
                className="gold-stream"
                initial={{ pathLength: 0, opacity: 0 }}
                animate={{ pathLength: 1, opacity: 1 }}
                transition={{ 
                  duration: FIBONACCI_TIMING.consciousness / 1000,
                  delay: i * 0.1
                }}
                style={{
                  position: 'absolute',
                  left: `${20 + i * 15}%`,
                  top: `${10 + Math.sin(i) * 20}%`,
                  width: '2px',
                  height: '80%',
                  background: `linear-gradient(to bottom, transparent, ${config.baseColor}, transparent)`,
                  transform: `rotate(${i * 11.25}deg)` // Golden angle approximation
                }}
              />
            ))}
          </div>
        );

      case 'social':
        return (
          <div className="crystal-network">
            <svg width="100%" height="100%" viewBox="0 0 200 300">
              {data?.relationships?.slice(0, Math.floor(progress / 10)).map((rel: any, i: number) => (
                <g key={i}>
                  <motion.circle
                    cx={50 + (i % 3) * 50}
                    cy={50 + Math.floor(i / 3) * 60}
                    r={rel.strength * 10}
                    fill={config.baseColor}
                    opacity={0.7}
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ delay: i * 0.1 }}
                  />
                  <motion.line
                    x1={50 + (i % 3) * 50}
                    y1={50 + Math.floor(i / 3) * 60}
                    x2={50 + ((i + 1) % 3) * 50}
                    y2={50 + Math.floor((i + 1) / 3) * 60}
                    stroke={config.baseColor}
                    strokeWidth={2}
                    opacity={0.5}
                    initial={{ pathLength: 0 }}
                    animate={{ pathLength: 1 }}
                    transition={{ delay: i * 0.1 + 0.2 }}
                  />
                </g>
              ))}
            </svg>
          </div>
        );

      case 'creative':
        return (
          <div className="creative-prisms">
            {data?.works?.map((work: any, i: number) => (
              <motion.div
                key={i}
                className="color-prism"
                initial={{ opacity: 0, rotate: 0 }}
                animate={{ 
                  opacity: 1, 
                  rotate: 360,
                  background: [
                    work.primaryColor,
                    work.secondaryColor,
                    work.primaryColor
                  ]
                }}
                transition={{
                  opacity: { duration: 0.5, delay: i * 0.2 },
                  rotate: { duration: 3, repeat: Infinity, ease: "linear" },
                  background: { duration: 2, repeat: Infinity }
                }}
                style={{
                  position: 'absolute',
                  left: `${20 + (i % 4) * 20}%`,
                  top: `${20 + Math.floor(i / 4) * 25}%`,
                  width: '15%',
                  height: '20%',
                  clipPath: 'polygon(50% 0%, 0% 100%, 100% 100%)'
                }}
              />
            ))}
          </div>
        );

      case 'temporal':
        return (
          <div className="temporal-layers">
            {[...Array(5)].map((_, i) => (
              <motion.div
                key={i}
                className="time-layer"
                initial={{ opacity: 0 }}
                animate={{ opacity: Math.max(0, (progress - i * 20) / 100) }}
                style={{
                  position: 'absolute',
                  inset: `${i * 10}%`,
                  border: `2px solid ${config.baseColor}`,
                  borderRadius: '10px',
                  background: `rgba(255, 255, 255, ${Math.max(0, (progress - i * 20) / 500)})`
                }}
              />
            ))}
          </div>
        );

      case 'venice':
        return (
          <div className="heraldic-elements">
            <motion.div
              className="venetian-lion"
              initial={{ scale: 0, rotate: -180 }}
              animate={{ 
                scale: progress > 50 ? 1 : 0.5,
                rotate: 0
              }}
              transition={{ duration: FIBONACCI_TIMING.consciousness / 1000 }}
              style={{
                position: 'absolute',
                top: '20%',
                left: '50%',
                transform: 'translateX(-50%)',
                fontSize: '3rem',
                filter: `hue-rotate(${progress * 3.6}deg)`
              }}
            >
              🦁
            </motion.div>
            {progress > 75 && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="guild-symbols"
                style={{
                  position: 'absolute',
                  bottom: '20%',
                  left: '50%',
                  transform: 'translateX(-50%)',
                  display: 'flex',
                  gap: '10px'
                }}
              >
                <span>⚒️</span>
                <span>🎭</span>
                <span>📜</span>
              </motion.div>
            )}
          </div>
        );

      default:
        return null;
    }
  };

  // Update mirror content when progress changes
  useEffect(() => {
    setMirrorContent(generateMirrorContent());
    if (progress >= 100) {
      setTimeout(() => onComplete({ type, verification: true }), FIBONACCI_TIMING.consciousness);
    }
  }, [progress, data]);

  // Handle mirror activation
  useEffect(() => {
    setReflectionVisible(isActive);
  }, [isActive]);

  return (
    <motion.div
      className="verification-mirror"
      style={mirrorStyle}
      variants={mirrorVariants}
      initial="inactive"
      animate={
        progress >= 100 ? "completed" :
        isHovered ? "hovered" :
        isActive ? "active" : "inactive"
      }
      onHoverStart={() => setIsHovered(true)}
      onHoverEnd={() => setIsHovered(false)}
      onClick={onActivate}
    >
      {/* Mirror Frame with Sacred Geometry */}
      <div 
        className="mirror-frame"
        style={{
          position: 'absolute',
          inset: 0,
          border: `3px solid ${config.baseColor}`,
          borderRadius: '13px', // Fibonacci number
          background: 'rgba(255, 255, 255, 0.1)',
          backdropFilter: 'blur(21px)', // Fibonacci number
          overflow: 'hidden'
        }}
      >
        {/* Mirror Base Surface */}
        <div 
          className="mirror-surface"
          style={{
            position: 'absolute',
            inset: '8px', // Fibonacci number
            background: `linear-gradient(135deg, 
              rgba(255, 255, 255, 0.2), 
              rgba(255, 255, 255, 0.05),
              ${config.baseColor}20
            )`,
            borderRadius: '8px'
          }}
        />

        {/* Progress Indicator */}
        <div 
          className="progress-ring"
          style={{
            position: 'absolute',
            top: '8px',
            right: '8px',
            width: '34px', // Fibonacci number
            height: '34px',
            borderRadius: '50%',
            background: `conic-gradient(
              ${config.baseColor} ${progress * 3.6}deg,
              rgba(255, 255, 255, 0.2) ${progress * 3.6}deg
            )`,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '12px',
            color: 'white',
            fontWeight: 600
          }}
        >
          {Math.round(progress)}%
        </div>

        {/* Mirror Icon and Title */}
        <div 
          className="mirror-header"
          style={{
            position: 'absolute',
            top: '21px',
            left: '21px',
            right: '55px'
          }}
        >
          <div style={{ fontSize: '2rem', marginBottom: '8px' }}>
            {config.icon}
          </div>
          <h3 style={{
            fontSize: '14px',
            fontWeight: 600,
            color: 'white',
            margin: 0,
            textShadow: '0 2px 4px rgba(0,0,0,0.5)'
          }}>
            {config.title}
          </h3>
          <p style={{
            fontSize: '11px',
            color: 'rgba(255,255,255,0.8)',
            margin: '5px 0 0 0'
          }}>
            {config.description}
          </p>
        </div>

        {/* Mirror Reflection Content */}
        <AnimatePresence>
          {reflectionVisible && (
            <motion.div
              className="mirror-reflection"
              variants={reflectionVariants}
              initial="hidden"
              animate="visible"
              exit="hidden"
              style={{
                position: 'absolute',
                top: '89px', // Golden ratio proportion
                left: '13px',
                right: '13px',
                bottom: '21px',
                borderRadius: '8px',
                overflow: 'hidden'
              }}
            >
              {mirrorContent}
            </motion.div>
          )}
        </AnimatePresence>

        {/* Completion Glow Effect */}
        {progress >= 100 && (
          <motion.div
            className="completion-glow"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: [0, 1, 0], scale: [0.8, 1.2, 1] }}
            transition={{ 
              duration: FIBONACCI_TIMING.transcendence / 1000,
              repeat: Infinity
            }}
            style={{
              position: 'absolute',
              inset: '-21px',
              background: `radial-gradient(circle, ${config.baseColor}40, transparent 70%)`,
              borderRadius: '50%',
              pointerEvents: 'none'
            }}
          />
        )}
      </div>
    </motion.div>
  );
};

// Main Consciousness Verification Hall Component
interface HallOfMirrorsProps {
  verificationData: VerificationData;
  onVerificationComplete: (results: any) => void;
}

export const HallOfMirrors: React.FC<HallOfMirrorsProps> = ({
  verificationData,
  onVerificationComplete
}) => {
  const [activeVerifications, setActiveVerifications] = useState<Set<string>>(new Set());
  const [completedVerifications, setCompletedVerifications] = useState<Set<string>>(new Set());
  const [verificationProgress, setVerificationProgress] = useState({
    economic: 0,
    social: 0,
    creative: 0,
    temporal: 0,
    venice: 0
  });

  // Calculate overall verification harmony
  const overallHarmony = Object.values(verificationProgress).reduce((sum, progress) => sum + progress, 0) / 5;

  const handleMirrorActivate = (type: string) => {
    setActiveVerifications(prev => new Set(prev).add(type));
    // Simulate verification progress
    const interval = setInterval(() => {
      setVerificationProgress(prev => {
        const newProgress = Math.min(prev[type as keyof typeof prev] + 10, 100);
        if (newProgress >= 100) {
          clearInterval(interval);
          setCompletedVerifications(prevCompleted => new Set(prevCompleted).add(type));
        }
        return { ...prev, [type]: newProgress };
      });
    }, FIBONACCI_TIMING.consciousness / 10);
  };

  const handleMirrorComplete = (results: any) => {
    // Check if all verifications are complete
    if (completedVerifications.size === 4) { // 5 total - 1 for the one completing
      setTimeout(() => {
        onVerificationComplete({
          overallHarmony,
          completedVerifications: Array.from(completedVerifications),
          verificationData
        });
      }, FIBONACCI_TIMING.transcendence);
    }
  };

  return (
    <div 
      className="hall-of-mirrors"
      style={{
        position: 'relative',
        width: '800px',
        height: '800px',
        background: `radial-gradient(circle, 
          rgba(30, 58, 138, 0.1), 
          rgba(124, 58, 237, 0.05),
          transparent 70%
        )`,
        borderRadius: '50%',
        margin: '0 auto',
        overflow: 'visible'
      }}
    >
      {/* Central Avatar with Consciousness Aura */}
      <motion.div
        className="central-avatar"
        style={{
          position: 'absolute',
          left: '50%',
          top: '50%',
          transform: 'translate(-50%, -50%)',
          width: '144px', // φ² * base unit
          height: '144px',
          borderRadius: '50%',
          background: `conic-gradient(
            ${CONSCIOUSNESS_COLORS.gold},
            ${CONSCIOUSNESS_COLORS.transcendencePurple},
            ${CONSCIOUSNESS_COLORS.tessereBlue},
            ${CONSCIOUSNESS_COLORS.harmonyGreen},
            ${CONSCIOUSNESS_COLORS.gold}
          )`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: '3rem',
          filter: `brightness(${1 + overallHarmony / 100})`
        }}
        animate={{
          rotate: 360,
          scale: [1, 1.05, 1]
        }}
        transition={{
          rotate: { duration: FIBONACCI_TIMING.consciousness * 8 / 1000, repeat: Infinity, ease: "linear" },
          scale: { duration: FIBONACCI_TIMING.consciousness * 2 / 1000, repeat: Infinity }
        }}
      >
        👤
      </motion.div>

      {/* Five Verification Mirrors */}
      {Object.keys(verificationProgress).map((type) => (
        <ConsciousnessVerificationMirror
          key={type}
          type={type as any}
          data={verificationData[type as keyof VerificationData]}
          isActive={activeVerifications.has(type)}
          progress={verificationProgress[type as keyof typeof verificationProgress]}
          onActivate={() => handleMirrorActivate(type)}
          onComplete={handleMirrorComplete}
        />
      ))}

      {/* Ambient Chamber Lighting */}
      <motion.div
        className="ambient-lighting"
        style={{
          position: 'absolute',
          inset: '-50px',
          background: `radial-gradient(circle,
            transparent 40%,
            rgba(212, 175, 55, ${overallHarmony / 500}) 70%,
            rgba(124, 58, 237, ${overallHarmony / 1000}) 100%
          )`,
          borderRadius: '50%',
          pointerEvents: 'none'
        }}
        animate={{
          opacity: [0.3, 0.7, 0.3]
        }}
        transition={{
          duration: FIBONACCI_TIMING.consciousness * 3 / 1000,
          repeat: Infinity
        }}
      />
    </div>
  );
};

export default HallOfMirrors;