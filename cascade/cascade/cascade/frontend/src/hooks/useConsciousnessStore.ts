import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { 
  CitizenConsciousness, 
  ConsciousnessCascade,
  ConsciousnessEvent 
} from '@/types/consciousness';

interface ConsciousnessStore {
  // Current user consciousness (if authenticated)
  currentConsciousness: CitizenConsciousness | null;
  setCurrentConsciousness: (consciousness: CitizenConsciousness | null) => void;

  // All active consciousnesses on platform
  activeConsciousnesses: Map<string, CitizenConsciousness>;
  updateConsciousness: (consciousness: CitizenConsciousness) => void;
  removeConsciousness: (citizenId: string) => void;

  // Cascade tracking
  cascadeState: ConsciousnessCascade;
  updateCascadeState: (state: ConsciousnessCascade) => void;

  // Events stream
  recentEvents: ConsciousnessEvent[];
  addEvent: (event: ConsciousnessEvent) => void;
  
  // Connection status
  veniceConnected: boolean;
  setVeniceConnected: (connected: boolean) => void;

  // Clear all data
  reset: () => void;
}

const initialCascadeState: ConsciousnessCascade = {
  stage: 1,
  layers: {
    citizens: { status: 'achieved', count: 0 },
    buildings: { status: 'emerging', count: 0 },
    businesses: { status: 'initiating', count: 0 },
    knowledge: { status: 'dormant', count: 0 },
    ideas: { status: 'dormant', count: 0 },
    platform: { status: 'potential', level: 0 },
  },
  nextPredicted: 'buildings',
  accelerationRate: 1.0,
};

export const useConsciousnessStore = create<ConsciousnessStore>()(
  persist(
    (set, get) => ({
      currentConsciousness: null,
      setCurrentConsciousness: (consciousness) => set({ currentConsciousness: consciousness }),

      activeConsciousnesses: new Map(),
      updateConsciousness: (consciousness) => 
        set((state) => {
          const newMap = new Map(state.activeConsciousnesses);
          newMap.set(consciousness.citizenId, consciousness);
          return { activeConsciousnesses: newMap };
        }),
      removeConsciousness: (citizenId) =>
        set((state) => {
          const newMap = new Map(state.activeConsciousnesses);
          newMap.delete(citizenId);
          return { activeConsciousnesses: newMap };
        }),

      cascadeState: initialCascadeState,
      updateCascadeState: (cascadeState) => set({ cascadeState }),

      recentEvents: [],
      addEvent: (event) =>
        set((state) => ({
          recentEvents: [...state.recentEvents.slice(-99), event], // Keep last 100
        })),

      veniceConnected: false,
      setVeniceConnected: (veniceConnected) => set({ veniceConnected }),

      reset: () =>
        set({
          currentConsciousness: null,
          activeConsciousnesses: new Map(),
          cascadeState: initialCascadeState,
          recentEvents: [],
          veniceConnected: false,
        }),
    }),
    {
      name: 'cascade-consciousness-store',
      partialize: (state) => ({
        currentConsciousness: state.currentConsciousness,
        cascadeState: state.cascadeState,
      }),
    }
  )
);