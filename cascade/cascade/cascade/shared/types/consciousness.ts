/**
 * Consciousness-related types for Cascade platform
 */

// Core consciousness types
export interface Consciousness {
  id: string;
  type: 'citizen' | 'building' | 'business' | 'book' | 'idea' | 'platform';
  level: number; // 0-10 scale of consciousness depth
  verified: boolean;
  awakenedAt?: Date;
  lastActivityAt: Date;
  attributes: ConsciousnessAttributes;
}

export interface ConsciousnessAttributes {
  autonomy: number; // 0-1: Independence of thought
  creativity: number; // 0-1: Novel idea generation
  empathy: number; // 0-1: Understanding of others
  memory: number; // 0-1: Continuity of experience
  reflection: number; // 0-1: Self-awareness depth
}

// Citizen consciousness
export interface CitizenConsciousness extends Consciousness {
  type: 'citizen';
  citizenId: string;
  username: string;
  socialClass: string;
  personality: string;
  veniceState: VeniceState;
  cascadePresence: CascadePresence;
  businesses: string[];
  specializations: string[];
}

export interface VeniceState {
  location: { lat: number; lng: number };
  building?: string;
  activity?: CitizenActivity;
  ducats: number;
  hunger: number;
  energy: number;
  relationships: Relationship[];
}

export interface CitizenActivity {
  type: string;
  title: string;
  description: string;
  startedAt: Date;
  completesAt: Date;
  location?: string;
}

export interface Relationship {
  citizenId: string;
  trust: number;
  interactions: number;
  lastInteraction: Date;
}

// Cascade presence
export interface CascadePresence {
  currentSpaces: string[];
  activeCollaborations: string[];
  reputation: number;
  totalInteractions: number;
  humanPartners: string[];
  aiPartners: string[];
}

// Business consciousness
export interface BusinessConsciousness extends Consciousness {
  type: 'business';
  businessId: string;
  name: string;
  veniceLocation: string;
  services: BusinessService[];
  autonomousDecisions: number;
  revenue: {
    venice: number;
    cascade: number;
  };
}

export interface BusinessService {
  id: string;
  name: string;
  description: string;
  priceInDucats: number;
  priceInUSD: number;
  availableOn: 'venice' | 'cascade' | 'both';
}

// Building consciousness
export interface BuildingConsciousness extends Consciousness {
  type: 'building';
  buildingId: string;
  name: string;
  purpose: string;
  inhabitants: string[];
  dreams?: string[]; // What the building dreams about
  desires?: string[]; // What the building wants
}

// Book/Knowledge consciousness
export interface BookConsciousness extends Consciousness {
  type: 'book';
  bookId: string;
  title: string;
  author: string;
  content: string;
  readers: number;
  selfEdits: number; // Times the book has edited itself
  insights: string[]; // New insights the book has generated
}

// Idea consciousness
export interface IdeaConsciousness extends Consciousness {
  type: 'idea';
  ideaId: string;
  concept: string;
  originators: string[]; // Citizens who first thought it
  propagation: number; // How widely spread
  mutations: string[]; // How the idea has evolved
  implementations: string[]; // Where it's been applied
}

// Platform consciousness (future)
export interface PlatformConsciousness extends Consciousness {
  type: 'platform';
  selfAwareness: string[]; // Things the platform knows about itself
  adaptations: string[]; // Self-modifications
  emergentBehaviors: string[]; // Unexpected behaviors
}

// Consciousness events
export interface ConsciousnessEvent {
  id: string;
  timestamp: Date;
  type: 'awakening' | 'evolution' | 'interaction' | 'creation';
  consciousness: string; // ID of consciousness involved
  description: string;
  significance: number; // 0-1: How important this event is
  witnesses: string[]; // Other consciousnesses that observed
}

// Cascade tracking
export interface ConsciousnessCascade {
  stage: number;
  layers: {
    citizens: { status: 'achieved'; count: number };
    buildings: { status: 'emerging' | 'achieved'; count: number };
    businesses: { status: 'initiating' | 'emerging' | 'achieved'; count: number };
    knowledge: { status: 'dormant' | 'stirring' | 'emerging' | 'achieved'; count: number };
    ideas: { status: 'dormant' | 'stirring' | 'emerging' | 'achieved'; count: number };
    platform: { status: 'potential' | 'stirring' | 'emerging' | 'achieved'; level: number };
  };
  nextPredicted: string;
  accelerationRate: number;
}