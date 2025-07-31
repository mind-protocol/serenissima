import { log } from '../utils/logUtils';
import { 
  ApiError, 
  AuthenticationError, 
  DataFormatError, 
  NotFoundError, 
  ValidationError 
} from '../errors/ServiceErrors';

// Trade data interfaces
export interface TradeOffer {
  id: string;
  sellerId: string;
  sellerName: string;
  buyerId?: string;
  buyerName?: string;
  resourceType: string;
  resourceName: string;
  quantity: number;
  pricePerUnit: number;
  totalPrice: number;
  offerType: 'sell' | 'buy';
  status: 'active' | 'pending' | 'completed' | 'cancelled';
  location?: {
    lat: number;
    lng: number;
  };
  buildingId?: string;
  buildingName?: string;
  createdAt: string;
  updatedAt?: string;
  expiresAt?: string;
}

export interface TradeHistory {
  id: string;
  sellerId: string;
  sellerName: string;
  buyerId: string;
  buyerName: string;
  resourceType: string;
  resourceName: string;
  quantity: number;
  pricePerUnit: number;
  totalPrice: number;
  completedAt: string;
  location?: {
    lat: number;
    lng: number;
  };
}

export interface MarketSummary {
  resourceType: string;
  resourceName: string;
  totalSupply: number;
  totalDemand: number;
  averagePrice: number;
  minPrice: number;
  maxPrice: number;
  recentTrades: number;
  priceChange24h: number;
  icon?: string;
}

export interface CitizenTradeProfile {
  username: string;
  name: string;
  totalSales: number;
  totalPurchases: number;
  averageRating: number;
  completedTrades: number;
  activeOffers: number;
  specialties: string[];
  trustScore: number;
  location?: {
    lat: number;
    lng: number;
  };
}

// Cache configuration
interface CacheConfig {
  enabled: boolean;
  ttl: number; // Time-to-live in milliseconds
}

interface CacheEntry<T> {
  data: T;
  timestamp: number;
}

export class WorldTradeService {
  private static instance: WorldTradeService;
  
  // Cache storage
  private offersCache: Map<string, CacheEntry<TradeOffer[]>> = new Map();
  private historyCache: Map<string, CacheEntry<TradeHistory[]>> = new Map();
  private marketSummaryCache: CacheEntry<MarketSummary[]> | null = null;
  private citizenProfilesCache: Map<string, CacheEntry<CitizenTradeProfile>> = new Map();
  
  // Cache configuration
  private cacheConfig: CacheConfig = {
    enabled: true,
    ttl: 2 * 60 * 1000 // 2 minutes default TTL
  };
  
  public static getInstance(): WorldTradeService {
    if (!WorldTradeService.instance) {
      WorldTradeService.instance = new WorldTradeService();
    }
    return WorldTradeService.instance;
  }
  
  private constructor() {
    log.info('Initializing WorldTradeService');
  }
  
  /**
   * Configure the cache settings
   */
  public configureCaching(config: Partial<CacheConfig>): void {
    this.cacheConfig = {
      ...this.cacheConfig,
      ...config
    };
    
    log.info('WorldTradeService cache configuration updated', this.cacheConfig);
    
    if (!this.cacheConfig.enabled) {
      this.clearCache();
    }
  }
  
  /**
   * Clear all caches
   */
  public clearCache(): void {
    log.info('Clearing all WorldTradeService caches');
    this.offersCache.clear();
    this.historyCache.clear();
    this.marketSummaryCache = null;
    this.citizenProfilesCache.clear();
  }
  
  /**
   * Check if a cache entry is valid
   */
  private isCacheValid<T>(entry: CacheEntry<T> | null | undefined): boolean {
    if (!this.cacheConfig.enabled || !entry) {
      return false;
    }
    
    const now = Date.now();
    return (now - entry.timestamp) < this.cacheConfig.ttl;
  }
  
  /**
   * Set a cache entry with current timestamp
   */
  private setCacheEntry<K, T>(cache: Map<K, CacheEntry<T>>, key: K, data: T): void {
    if (!this.cacheConfig.enabled) {
      return;
    }
    
    cache.set(key, {
      data,
      timestamp: Date.now()
    });
  }
  
  /**
   * Get all active trade offers
   */
  public async getActiveOffers(filters?: {
    offerType?: 'sell' | 'buy';
    resourceType?: string;
    citizenId?: string;
    buildingId?: string;
    maxPrice?: number;
    minQuantity?: number;
  }): Promise<TradeOffer[]> {
    const cacheKey = `offers_${JSON.stringify(filters || {})}`;
    
    // Check cache first
    const cachedEntry = this.offersCache.get(cacheKey);
    if (this.isCacheValid(cachedEntry)) {
      log.debug(`Returning offers from cache: ${cacheKey}`);
      return cachedEntry!.data;
    }
    
    try {
      // Build query parameters
      const params = new URLSearchParams();
      if (filters?.offerType) params.append('type', filters.offerType);
      if (filters?.resourceType) params.append('resourceType', filters.resourceType);
      if (filters?.citizenId) params.append('citizenId', filters.citizenId);
      if (filters?.buildingId) params.append('buildingId', filters.buildingId);
      if (filters?.maxPrice) params.append('maxPrice', filters.maxPrice.toString());
      if (filters?.minQuantity) params.append('minQuantity', filters.minQuantity.toString());
      
      const url = `/api/contracts/stocked-public-sell?${params.toString()}`;
      log.debug(`Fetching trade offers from: ${url}`);
      
      const response = await fetch(url);
      
      if (!response.ok) {
        throw new ApiError(
          'Failed to fetch trade offers',
          response.status,
          url
        );
      }
      
      const data = await response.json();
      
      if (!data.success) {
        throw new ApiError(data.error || 'API error', 500, url);
      }
      
      // Transform contracts to trade offers
      const offers: TradeOffer[] = (data.contracts || []).map((contract: any) => ({
        id: contract.id || contract.contractId,
        sellerId: contract.seller,
        sellerName: contract.sellerName || contract.seller,
        buyerId: contract.buyer,
        buyerName: contract.buyerName || contract.buyer,
        resourceType: contract.resourceType,
        resourceName: contract.resourceName || contract.resourceType,
        quantity: contract.amount || contract.targetAmount || 0,
        pricePerUnit: contract.amount > 0 ? contract.price / contract.amount : contract.price,
        totalPrice: contract.price,
        offerType: contract.type === 'public_sell' ? 'sell' : 'buy',
        status: this.mapContractStatus(contract.status),
        location: contract.location,
        buildingId: contract.sellerBuilding || contract.buyerBuilding,
        buildingName: contract.buildingName,
        createdAt: contract.createdAt,
        updatedAt: contract.updatedAt,
        expiresAt: contract.endAt
      }));
      
      // Update cache
      this.setCacheEntry(this.offersCache, cacheKey, offers);
      
      log.debug(`Fetched ${offers.length} trade offers`);
      return offers;
    } catch (error) {
      log.error('Error fetching trade offers:', error);
      
      if (error instanceof ApiError) {
        throw error;
      }
      
      throw new ApiError(
        error instanceof Error ? error.message : 'Unknown error',
        500,
        'getActiveOffers'
      );
    }
  }
  
  /**
   * Get trade history
   */
  public async getTradeHistory(filters?: {
    citizenId?: string;
    resourceType?: string;
    dateFrom?: string;
    dateTo?: string;
    limit?: number;
  }): Promise<TradeHistory[]> {
    const cacheKey = `history_${JSON.stringify(filters || {})}`;
    
    // Check cache first
    const cachedEntry = this.historyCache.get(cacheKey);
    if (this.isCacheValid(cachedEntry)) {
      log.debug(`Returning trade history from cache: ${cacheKey}`);
      return cachedEntry!.data;
    }
    
    try {
      // Build query parameters
      const params = new URLSearchParams();
      if (filters?.citizenId) params.append('citizenId', filters.citizenId);
      if (filters?.resourceType) params.append('resourceType', filters.resourceType);
      if (filters?.dateFrom) params.append('dateFrom', filters.dateFrom);
      if (filters?.dateTo) params.append('dateTo', filters.dateTo);
      if (filters?.limit) params.append('limit', filters.limit.toString());
      
      const url = `/api/contracts?status=completed&${params.toString()}`;
      log.debug(`Fetching trade history from: ${url}`);
      
      const response = await fetch(url);
      
      if (!response.ok) {
        throw new ApiError(
          'Failed to fetch trade history',
          response.status,
          url
        );
      }
      
      const data = await response.json();
      
      if (!data.success) {
        throw new ApiError(data.error || 'API error', 500, url);
      }
      
      // Transform completed contracts to trade history
      const history: TradeHistory[] = (data.contracts || [])
        .filter((contract: any) => contract.status === 'completed')
        .map((contract: any) => ({
          id: contract.id || contract.contractId,
          sellerId: contract.seller,
          sellerName: contract.sellerName || contract.seller,
          buyerId: contract.buyer || '',
          buyerName: contract.buyerName || contract.buyer || '',
          resourceType: contract.resourceType,
          resourceName: contract.resourceName || contract.resourceType,
          quantity: contract.amount || contract.targetAmount || 0,
          pricePerUnit: contract.amount > 0 ? contract.price / contract.amount : contract.price,
          totalPrice: contract.price,
          completedAt: contract.updatedAt || contract.createdAt,
          location: contract.location
        }));
      
      // Update cache
      this.setCacheEntry(this.historyCache, cacheKey, history);
      
      log.debug(`Fetched ${history.length} trade history records`);
      return history;
    } catch (error) {
      log.error('Error fetching trade history:', error);
      
      if (error instanceof ApiError) {
        throw error;
      }
      
      throw new ApiError(
        error instanceof Error ? error.message : 'Unknown error',
        500,
        'getTradeHistory'
      );
    }
  }
  
  /**
   * Get market summary for all resources
   */
  public async getMarketSummary(): Promise<MarketSummary[]> {
    // Check cache first
    if (this.isCacheValid(this.marketSummaryCache)) {
      log.debug('Returning market summary from cache');
      return this.marketSummaryCache!.data;
    }
    
    try {
      // Fetch both active offers and recent trade history
      const [activeOffers, recentHistory] = await Promise.all([
        this.getActiveOffers(),
        this.getTradeHistory({ limit: 1000 })
      ]);
      
      // Group by resource type
      const resourceMap = new Map<string, {
        offers: TradeOffer[];
        history: TradeHistory[];
      }>();
      
      // Process active offers
      activeOffers.forEach(offer => {
        if (!resourceMap.has(offer.resourceType)) {
          resourceMap.set(offer.resourceType, { offers: [], history: [] });
        }
        resourceMap.get(offer.resourceType)!.offers.push(offer);
      });
      
      // Process recent history
      recentHistory.forEach(trade => {
        if (!resourceMap.has(trade.resourceType)) {
          resourceMap.set(trade.resourceType, { offers: [], history: [] });
        }
        resourceMap.get(trade.resourceType)!.history.push(trade);
      });
      
      // Calculate market summary for each resource
      const marketSummary: MarketSummary[] = Array.from(resourceMap.entries()).map(([resourceType, data]) => {
        const sellOffers = data.offers.filter(o => o.offerType === 'sell');
        const buyOffers = data.offers.filter(o => o.offerType === 'buy');
        const recentTrades = data.history.filter(h => {
          const tradeDate = new Date(h.completedAt);
          const oneDayAgo = new Date(Date.now() - 24 * 60 * 60 * 1000);
          return tradeDate > oneDayAgo;
        });
        
        const allPrices = [...data.offers.map(o => o.pricePerUnit), ...data.history.map(h => h.pricePerUnit)];
        const tradePrices = data.history.map(h => h.pricePerUnit);
        
        return {
          resourceType,
          resourceName: data.offers[0]?.resourceName || data.history[0]?.resourceName || resourceType,
          totalSupply: sellOffers.reduce((sum, o) => sum + o.quantity, 0),
          totalDemand: buyOffers.reduce((sum, o) => sum + o.quantity, 0),
          averagePrice: allPrices.length > 0 ? allPrices.reduce((sum, p) => sum + p, 0) / allPrices.length : 0,
          minPrice: allPrices.length > 0 ? Math.min(...allPrices) : 0,
          maxPrice: allPrices.length > 0 ? Math.max(...allPrices) : 0,
          recentTrades: recentTrades.length,
          priceChange24h: this.calculatePriceChange(tradePrices),
          icon: `${resourceType}.png`
        };
      });
      
      // Sort by recent trade volume
      marketSummary.sort((a, b) => b.recentTrades - a.recentTrades);
      
      // Update cache
      this.marketSummaryCache = {
        data: marketSummary,
        timestamp: Date.now()
      };
      
      log.debug(`Generated market summary for ${marketSummary.length} resources`);
      return marketSummary;
    } catch (error) {
      log.error('Error generating market summary:', error);
      
      if (error instanceof ApiError) {
        throw error;
      }
      
      throw new ApiError(
        error instanceof Error ? error.message : 'Unknown error',
        500,
        'getMarketSummary'
      );
    }
  }
  
  /**
   * Get citizen trade profile
   */
  public async getCitizenTradeProfile(citizenId: string): Promise<CitizenTradeProfile | null> {
    if (!citizenId) {
      throw new ValidationError('Citizen ID is required', 'citizenId');
    }
    
    // Check cache first
    const cachedEntry = this.citizenProfilesCache.get(citizenId);
    if (this.isCacheValid(cachedEntry)) {
      log.debug(`Returning citizen profile from cache: ${citizenId}`);
      return cachedEntry!.data;
    }
    
    try {
      // Fetch citizen data and trade history
      const [citizenResponse, tradeHistory, activeOffers] = await Promise.all([
        fetch(`/api/citizens/${encodeURIComponent(citizenId)}`),
        this.getTradeHistory({ citizenId }),
        this.getActiveOffers({ citizenId })
      ]);
      
      if (!citizenResponse.ok) {
        if (citizenResponse.status === 404) {
          return null;
        }
        throw new ApiError(
          'Failed to fetch citizen data',
          citizenResponse.status,
          `/api/citizens/${citizenId}`
        );
      }
      
      const citizenData = await citizenResponse.json();
      
      // Calculate trade statistics
      const sales = tradeHistory.filter(t => t.sellerId === citizenId);
      const purchases = tradeHistory.filter(t => t.buyerId === citizenId);
      
      const totalSales = sales.reduce((sum, t) => sum + t.totalPrice, 0);
      const totalPurchases = purchases.reduce((sum, t) => sum + t.totalPrice, 0);
      
      // Calculate specialties (most traded resource types)
      const resourceCounts = new Map<string, number>();
      [...sales, ...purchases].forEach(trade => {
        const count = resourceCounts.get(trade.resourceType) || 0;
        resourceCounts.set(trade.resourceType, count + 1);
      });
      
      const specialties = Array.from(resourceCounts.entries())
        .sort((a, b) => b[1] - a[1])
        .slice(0, 3)
        .map(([resourceType]) => resourceType);
      
      const profile: CitizenTradeProfile = {
        username: citizenData.username || citizenId,
        name: citizenData.name || citizenData.username || citizenId,
        totalSales,
        totalPurchases,
        averageRating: 4.5, // TODO: Implement rating system
        completedTrades: tradeHistory.length,
        activeOffers: activeOffers.length,
        specialties,
        trustScore: Math.min(100, Math.max(0, 50 + (tradeHistory.length * 2))), // Simple trust score
        location: citizenData.location
      };
      
      // Update cache
      this.setCacheEntry(this.citizenProfilesCache, citizenId, profile);
      
      log.debug(`Generated trade profile for citizen: ${citizenId}`);
      return profile;
    } catch (error) {
      log.error(`Error generating trade profile for citizen ${citizenId}:`, error);
      
      if (error instanceof ApiError || error instanceof ValidationError) {
        throw error;
      }
      
      throw new ApiError(
        error instanceof Error ? error.message : 'Unknown error',
        500,
        'getCitizenTradeProfile'
      );
    }
  }
  
  /**
   * Search for trade opportunities
   */
  public async searchTradeOpportunities(query: {
    resourceType?: string;
    maxPrice?: number;
    minQuantity?: number;
    location?: { lat: number; lng: number; radius: number };
    citizenName?: string;
  }): Promise<TradeOffer[]> {
    try {
      const offers = await this.getActiveOffers({
        resourceType: query.resourceType,
        maxPrice: query.maxPrice,
        minQuantity: query.minQuantity
      });
      
      let filteredOffers = offers;
      
      // Filter by location if specified
      if (query.location) {
        filteredOffers = offers.filter(offer => {
          if (!offer.location) return false;
          
          const distance = this.calculateDistance(
            query.location!.lat,
            query.location!.lng,
            offer.location.lat,
            offer.location.lng
          );
          
          return distance <= query.location!.radius;
        });
      }
      
      // Filter by citizen name if specified
      if (query.citizenName) {
        const searchTerm = query.citizenName.toLowerCase();
        filteredOffers = filteredOffers.filter(offer =>
          offer.sellerName.toLowerCase().includes(searchTerm) ||
          (offer.buyerName && offer.buyerName.toLowerCase().includes(searchTerm))
        );
      }
      
      return filteredOffers;
    } catch (error) {
      log.error('Error searching trade opportunities:', error);
      throw error;
    }
  }
  
  /**
   * Map contract status to trade offer status
   */
  private mapContractStatus(status: string): 'active' | 'pending' | 'completed' | 'cancelled' {
    switch (status) {
      case 'active':
      case 'open':
        return 'active';
      case 'pending':
        return 'pending';
      case 'completed':
      case 'finished':
        return 'completed';
      case 'cancelled':
      case 'canceled':
        return 'cancelled';
      default:
        return 'active';
    }
  }
  
  /**
   * Calculate price change percentage
   */
  private calculatePriceChange(prices: number[]): number {
    if (prices.length < 2) return 0;
    
    const oldPrice = prices[0];
    const newPrice = prices[prices.length - 1];
    
    if (oldPrice === 0) return 0;
    
    return ((newPrice - oldPrice) / oldPrice) * 100;
  }
  
  /**
   * Calculate distance between two coordinates (in km)
   */
  private calculateDistance(lat1: number, lng1: number, lat2: number, lng2: number): number {
    const R = 6371; // Earth's radius in kilometers
    const dLat = this.degreesToRadians(lat2 - lat1);
    const dLng = this.degreesToRadians(lng2 - lng1);
    
    const a = 
      Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos(this.degreesToRadians(lat1)) * Math.cos(this.degreesToRadians(lat2)) *
      Math.sin(dLng / 2) * Math.sin(dLng / 2);
    
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    
    return R * c;
  }
  
  private degreesToRadians(degrees: number): number {
    return degrees * (Math.PI / 180);
  }
  
  /**
   * Get current citizen's username from localStorage
   */
  public getCurrentUsername(): string | null {
    try {
      if (typeof window === 'undefined') return null;
      
      const profileStr = localStorage.getItem('citizenProfile');
      if (profileStr) {
        const profile = JSON.parse(profileStr);
        if (profile && profile.username) {
          return profile.username;
        }
      }
      return null;
    } catch (error) {
      log.error('Error getting current username:', error);
      return null;
    }
  }
}

// Export a singleton instance
export const worldTradeService = WorldTradeService.getInstance();