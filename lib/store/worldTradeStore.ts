import { create } from 'zustand';
import { devtools } from 'zustand/middleware';
import { 
  WorldTradeService, 
  TradeOffer, 
  TradeHistory, 
  MarketSummary, 
  CitizenTradeProfile,
  worldTradeService 
} from '../services/WorldTradeService';
import { log } from '../utils/logUtils';

// Store state interface
interface WorldTradeState {
  // Data
  activeOffers: TradeOffer[];
  tradeHistory: TradeHistory[];
  marketSummary: MarketSummary[];
  citizenProfiles: Map<string, CitizenTradeProfile>;
  
  // UI state
  isLoading: boolean;
  error: string | null;
  selectedOffer: TradeOffer | null;
  selectedCitizen: string | null;
  
  // Filters
  filters: {
    offerType?: 'sell' | 'buy';
    resourceType?: string;
    maxPrice?: number;
    minQuantity?: number;
    citizenId?: string;
    buildingId?: string;
  };
  
  // Search state
  searchQuery: string;
  searchResults: TradeOffer[];
  
  // Pagination
  currentPage: number;
  itemsPerPage: number;
  totalItems: number;
}

// Store actions interface
interface WorldTradeActions {
  // Data fetching actions
  fetchActiveOffers: (filters?: Partial<WorldTradeState['filters']>) => Promise<void>;
  fetchTradeHistory: (filters?: { citizenId?: string; resourceType?: string; limit?: number }) => Promise<void>;
  fetchMarketSummary: () => Promise<void>;
  fetchCitizenProfile: (citizenId: string) => Promise<CitizenTradeProfile | null>;
  
  // Search actions
  searchTradeOpportunities: (query: {
    resourceType?: string;
    maxPrice?: number;
    minQuantity?: number;
    location?: { lat: number; lng: number; radius: number };
    citizenName?: string;
  }) => Promise<void>;
  setSearchQuery: (query: string) => void;
  clearSearchResults: () => void;
  
  // Filter actions
  setFilters: (filters: Partial<WorldTradeState['filters']>) => void;
  clearFilters: () => void;
  
  // UI actions
  setSelectedOffer: (offer: TradeOffer | null) => void;
  setSelectedCitizen: (citizenId: string | null) => void;
  setError: (error: string | null) => void;
  clearError: () => void;
  
  // Pagination actions
  setCurrentPage: (page: number) => void;
  setItemsPerPage: (itemsPerPage: number) => void;
  
  // Utility actions
  refreshData: () => Promise<void>;
  clearCache: () => void;
  
  // Data manipulation helpers
  getOfferById: (offerId: string) => TradeOffer | undefined;
  getOffersByResource: (resourceType: string) => TradeOffer[];
  getOffersByCitizen: (citizenId: string) => TradeOffer[];
  getCitizenProfile: (citizenId: string) => CitizenTradeProfile | undefined;
  
  // Market analysis helpers
  getResourceMarketData: (resourceType: string) => MarketSummary | undefined;
  getTrendingResources: () => MarketSummary[];
  getMostActiveTraders: () => CitizenTradeProfile[];
}

// Initial state
const initialState: WorldTradeState = {
  activeOffers: [],
  tradeHistory: [],
  marketSummary: [],
  citizenProfiles: new Map(),
  
  isLoading: false,
  error: null,
  selectedOffer: null,
  selectedCitizen: null,
  
  filters: {},
  
  searchQuery: '',
  searchResults: [],
  
  currentPage: 1,
  itemsPerPage: 20,
  totalItems: 0,
};

// Create the store
export const useWorldTradeStore = create<WorldTradeState & WorldTradeActions>()(
  devtools(
    (set, get) => ({
      ...initialState,
      
      // Data fetching actions
      fetchActiveOffers: async (filters) => {
        log.debug('WorldTradeStore: Fetching active offers', filters);
        set({ isLoading: true, error: null });
        
        try {
          const mergedFilters = { ...get().filters, ...filters };
          const offers = await worldTradeService.getActiveOffers(mergedFilters);
          
          set({ 
            activeOffers: offers,
            totalItems: offers.length,
            isLoading: false 
          });
          
          log.debug(`WorldTradeStore: Fetched ${offers.length} active offers`);
        } catch (error) {
          log.error('WorldTradeStore: Error fetching active offers:', error);
          set({ 
            error: error instanceof Error ? error.message : 'Failed to fetch offers',
            isLoading: false 
          });
        }
      },
      
      fetchTradeHistory: async (filters) => {
        log.debug('WorldTradeStore: Fetching trade history', filters);
        set({ isLoading: true, error: null });
        
        try {
          const history = await worldTradeService.getTradeHistory(filters);
          
          set({ 
            tradeHistory: history,
            isLoading: false 
          });
          
          log.debug(`WorldTradeStore: Fetched ${history.length} trade history records`);
        } catch (error) {
          log.error('WorldTradeStore: Error fetching trade history:', error);
          set({ 
            error: error instanceof Error ? error.message : 'Failed to fetch trade history',
            isLoading: false 
          });
        }
      },
      
      fetchMarketSummary: async () => {
        log.debug('WorldTradeStore: Fetching market summary');
        set({ isLoading: true, error: null });
        
        try {
          const summary = await worldTradeService.getMarketSummary();
          
          set({ 
            marketSummary: summary,
            isLoading: false 
          });
          
          log.debug(`WorldTradeStore: Fetched market summary for ${summary.length} resources`);
        } catch (error) {
          log.error('WorldTradeStore: Error fetching market summary:', error);
          set({ 
            error: error instanceof Error ? error.message : 'Failed to fetch market summary',
            isLoading: false 
          });
        }
      },
      
      fetchCitizenProfile: async (citizenId) => {
        log.debug(`WorldTradeStore: Fetching citizen profile for ${citizenId}`);
        
        try {
          const profile = await worldTradeService.getCitizenTradeProfile(citizenId);
          
          if (profile) {
            const profiles = new Map(get().citizenProfiles);
            profiles.set(citizenId, profile);
            set({ citizenProfiles: profiles });
            
            log.debug(`WorldTradeStore: Fetched profile for citizen ${citizenId}`);
            return profile;
          }
          
          return null;
        } catch (error) {
          log.error(`WorldTradeStore: Error fetching citizen profile for ${citizenId}:`, error);
          set({ error: error instanceof Error ? error.message : 'Failed to fetch citizen profile' });
          return null;
        }
      },
      
      // Search actions
      searchTradeOpportunities: async (query) => {
        log.debug('WorldTradeStore: Searching trade opportunities', query);
        set({ isLoading: true, error: null });
        
        try {
          const results = await worldTradeService.searchTradeOpportunities(query);
          
          set({ 
            searchResults: results,
            isLoading: false 
          });
          
          log.debug(`WorldTradeStore: Found ${results.length} trade opportunities`);
        } catch (error) {
          log.error('WorldTradeStore: Error searching trade opportunities:', error);
          set({ 
            error: error instanceof Error ? error.message : 'Failed to search trade opportunities',
            isLoading: false 
          });
        }
      },
      
      setSearchQuery: (query) => {
        set({ searchQuery: query });
      },
      
      clearSearchResults: () => {
        set({ searchResults: [], searchQuery: '' });
      },
      
      // Filter actions
      setFilters: (filters) => {
        set({ filters: { ...get().filters, ...filters } });
      },
      
      clearFilters: () => {
        set({ filters: {} });
      },
      
      // UI actions
      setSelectedOffer: (offer) => {
        set({ selectedOffer: offer });
      },
      
      setSelectedCitizen: (citizenId) => {
        set({ selectedCitizen: citizenId });
      },
      
      setError: (error) => {
        set({ error });
      },
      
      clearError: () => {
        set({ error: null });
      },
      
      // Pagination actions
      setCurrentPage: (page) => {
        set({ currentPage: page });
      },
      
      setItemsPerPage: (itemsPerPage) => {
        set({ itemsPerPage, currentPage: 1 }); // Reset to first page when changing items per page
      },
      
      // Utility actions
      refreshData: async () => {
        log.debug('WorldTradeStore: Refreshing all data');
        
        const { filters } = get();
        
        // Clear cache first
        worldTradeService.clearCache();
        
        // Fetch all data in parallel
        await Promise.all([
          get().fetchActiveOffers(filters),
          get().fetchTradeHistory(),
          get().fetchMarketSummary()
        ]);
        
        log.debug('WorldTradeStore: Data refresh completed');
      },
      
      clearCache: () => {
        log.debug('WorldTradeStore: Clearing cache');
        worldTradeService.clearCache();
      },
      
      // Data manipulation helpers
      getOfferById: (offerId) => {
        return get().activeOffers.find(offer => offer.id === offerId);
      },
      
      getOffersByResource: (resourceType) => {
        return get().activeOffers.filter(offer => offer.resourceType === resourceType);
      },
      
      getOffersByCitizen: (citizenId) => {
        return get().activeOffers.filter(offer => 
          offer.sellerId === citizenId || offer.buyerId === citizenId
        );
      },
      
      getCitizenProfile: (citizenId) => {
        return get().citizenProfiles.get(citizenId);
      },
      
      // Market analysis helpers
      getResourceMarketData: (resourceType) => {
        return get().marketSummary.find(summary => summary.resourceType === resourceType);
      },
      
      getTrendingResources: () => {
        return get().marketSummary
          .filter(summary => summary.recentTrades > 0)
          .sort((a, b) => b.recentTrades - a.recentTrades)
          .slice(0, 10);
      },
      
      getMostActiveTraders: () => {
        const profiles = Array.from(get().citizenProfiles.values());
        return profiles
          .sort((a, b) => b.completedTrades - a.completedTrades)
          .slice(0, 10);
      },
    }),
    {
      name: 'world-trade-store',
      partialize: (state) => ({
        // Only persist filters and UI preferences
        filters: state.filters,
        currentPage: state.currentPage,
        itemsPerPage: state.itemsPerPage,
      }),
    }
  )
);

// Selector hooks for common use cases
export const useActiveOffers = () => useWorldTradeStore(state => state.activeOffers);
export const useTradeHistory = () => useWorldTradeStore(state => state.tradeHistory);
export const useMarketSummary = () => useWorldTradeStore(state => state.marketSummary);
export const useTradeFilters = () => useWorldTradeStore(state => state.filters);
export const useTradeLoading = () => useWorldTradeStore(state => state.isLoading);
export const useTradeError = () => useWorldTradeStore(state => state.error);
export const useSelectedOffer = () => useWorldTradeStore(state => state.selectedOffer);
export const useSearchResults = () => useWorldTradeStore(state => state.searchResults);

// Custom hooks for common operations
export const useTradeData = () => {
  const store = useWorldTradeStore();
  
  return {
    activeOffers: store.activeOffers,
    tradeHistory: store.tradeHistory,
    marketSummary: store.marketSummary,
    isLoading: store.isLoading,
    error: store.error,
    refreshData: store.refreshData,
  };
};

export const useTradeFiltering = () => {
  const store = useWorldTradeStore();
  
  return {
    filters: store.filters,
    setFilters: store.setFilters,
    clearFilters: store.clearFilters,
    fetchWithFilters: store.fetchActiveOffers,
  };
};

export const useTradeSearch = () => {
  const store = useWorldTradeStore();
  
  return {
    searchQuery: store.searchQuery,
    searchResults: store.searchResults,
    setSearchQuery: store.setSearchQuery,
    searchTradeOpportunities: store.searchTradeOpportunities,
    clearSearchResults: store.clearSearchResults,
  };
};