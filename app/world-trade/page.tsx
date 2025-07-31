"use client";

import { useEffect, useState } from 'react';
import { useWorldTradeStore, useTradeData, useTradeFiltering, useTradeSearch } from '@/lib/store/worldTradeStore';
import { TradeOffer, MarketSummary, CitizenTradeProfile } from '@/lib/services/WorldTradeService';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { RefreshCw, Search, Filter, TrendingUp, TrendingDown, Users, Package, MapPin, Clock } from 'lucide-react';
import toast from 'react-hot-toast';

// Sub-components
const LoadingSpinner = () => (
  <div className="flex items-center justify-center p-8">
    <RefreshCw className="h-8 w-8 animate-spin text-amber-600" />
  </div>
);

const ErrorMessage = ({ error, onRetry }: { error: string; onRetry: () => void }) => (
  <div className="flex items-center justify-center p-8">
    <div className="text-center">
      <p className="text-red-600 mb-4">{error}</p>
      <Button onClick={onRetry} variant="outline">
        <RefreshCw className="h-4 w-4 mr-2" />
        Retry
      </Button>
    </div>
  </div>
);

const OfferCard = ({ offer, onSelect }: { offer: TradeOffer; onSelect: (offer: TradeOffer) => void }) => (
  <Card className="hover:shadow-md transition-shadow cursor-pointer" onClick={() => onSelect(offer)}>
    <CardContent className="p-4">
      <div className="flex justify-between items-start mb-2">
        <div>
          <h3 className="font-semibold text-sm">{offer.resourceName}</h3>
          <p className="text-xs text-gray-600">{offer.sellerName}</p>
        </div>
        <Badge variant={offer.offerType === 'sell' ? 'default' : 'secondary'}>
          {offer.offerType === 'sell' ? 'Selling' : 'Buying'}
        </Badge>
      </div>
      
      <div className="space-y-1 text-xs">
        <div className="flex justify-between">
          <span>Quantity:</span>
          <span className="font-medium">{offer.quantity.toLocaleString()}</span>
        </div>
        <div className="flex justify-between">
          <span>Price per unit:</span>
          <span className="font-medium">{offer.pricePerUnit.toLocaleString()} ducats</span>
        </div>
        <div className="flex justify-between">
          <span>Total:</span>
          <span className="font-bold text-amber-600">{offer.totalPrice.toLocaleString()} ducats</span>
        </div>
      </div>
      
      {offer.location && (
        <div className="flex items-center mt-2 text-xs text-gray-500">
          <MapPin className="h-3 w-3 mr-1" />
          <span>{offer.location.lat.toFixed(4)}, {offer.location.lng.toFixed(4)}</span>
        </div>
      )}
      
      <div className="flex items-center mt-2 text-xs text-gray-500">
        <Clock className="h-3 w-3 mr-1" />
        <span>{new Date(offer.createdAt).toLocaleDateString()}</span>
      </div>
    </CardContent>
  </Card>
);

const MarketSummaryCard = ({ market }: { market: MarketSummary }) => (
  <Card>
    <CardContent className="p-4">
      <div className="flex justify-between items-start mb-2">
        <h3 className="font-semibold text-sm">{market.resourceName}</h3>
        <div className="flex items-center">
          {market.priceChange24h > 0 ? (
            <TrendingUp className="h-4 w-4 text-green-600" />
          ) : market.priceChange24h < 0 ? (
            <TrendingDown className="h-4 w-4 text-red-600" />
          ) : null}
          <span className={`text-xs ml-1 ${
            market.priceChange24h > 0 ? 'text-green-600' : 
            market.priceChange24h < 0 ? 'text-red-600' : 'text-gray-600'
          }`}>
            {market.priceChange24h > 0 ? '+' : ''}{market.priceChange24h.toFixed(1)}%
          </span>
        </div>
      </div>
      
      <div className="space-y-1 text-xs">
        <div className="flex justify-between">
          <span>Supply:</span>
          <span>{market.totalSupply.toLocaleString()}</span>
        </div>
        <div className="flex justify-between">
          <span>Demand:</span>
          <span>{market.totalDemand.toLocaleString()}</span>
        </div>
        <div className="flex justify-between">
          <span>Avg Price:</span>
          <span className="font-medium">{market.averagePrice.toLocaleString()} ducats</span>
        </div>
        <div className="flex justify-between">
          <span>24h Trades:</span>
          <span className="text-amber-600 font-medium">{market.recentTrades}</span>
        </div>
      </div>
    </CardContent>
  </Card>
);

const FilterPanel = () => {
  const { filters, setFilters, clearFilters } = useTradeFiltering();
  const [localFilters, setLocalFilters] = useState(filters);
  
  const handleApplyFilters = () => {
    setFilters(localFilters);
  };
  
  const handleClearFilters = () => {
    setLocalFilters({});
    clearFilters();
  };
  
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg flex items-center">
          <Filter className="h-5 w-5 mr-2" />
          Filters
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <label className="text-sm font-medium mb-2 block">Offer Type</label>
          <Select 
            value={localFilters.offerType || ''} 
            onValueChange={(value) => setLocalFilters({ ...localFilters, offerType: value as 'sell' | 'buy' || undefined })}
          >
            <SelectTrigger>
              <SelectValue placeholder="All types" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="">All types</SelectItem>
              <SelectItem value="sell">Selling</SelectItem>
              <SelectItem value="buy">Buying</SelectItem>
            </SelectContent>
          </Select>
        </div>
        
        <div>
          <label className="text-sm font-medium mb-2 block">Resource Type</label>
          <Input
            placeholder="e.g., bread, silk, stone"
            value={localFilters.resourceType || ''}
            onChange={(e) => setLocalFilters({ ...localFilters, resourceType: e.target.value || undefined })}
          />
        </div>
        
        <div>
          <label className="text-sm font-medium mb-2 block">Max Price</label>
          <Input
            type="number"
            placeholder="Maximum price"
            value={localFilters.maxPrice || ''}
            onChange={(e) => setLocalFilters({ ...localFilters, maxPrice: e.target.value ? Number(e.target.value) : undefined })}
          />
        </div>
        
        <div>
          <label className="text-sm font-medium mb-2 block">Min Quantity</label>
          <Input
            type="number"
            placeholder="Minimum quantity"
            value={localFilters.minQuantity || ''}
            onChange={(e) => setLocalFilters({ ...localFilters, minQuantity: e.target.value ? Number(e.target.value) : undefined })}
          />
        </div>
        
        <div className="flex space-x-2">
          <Button onClick={handleApplyFilters} size="sm" className="flex-1">
            Apply Filters
          </Button>
          <Button onClick={handleClearFilters} variant="outline" size="sm">
            Clear
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};

const SearchPanel = () => {
  const { searchQuery, setSearchQuery, searchTradeOpportunities, clearSearchResults } = useTradeSearch();
  const [localQuery, setLocalQuery] = useState('');
  
  const handleSearch = () => {
    setSearchQuery(localQuery);
    searchTradeOpportunities({
      citizenName: localQuery
    });
  };
  
  const handleClear = () => {
    setLocalQuery('');
    setSearchQuery('');
    clearSearchResults();
  };
  
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg flex items-center">
          <Search className="h-5 w-5 mr-2" />
          Search
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <label className="text-sm font-medium mb-2 block">Search by citizen name</label>
          <Input
            placeholder="Enter citizen name..."
            value={localQuery}
            onChange={(e) => setLocalQuery(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
          />
        </div>
        
        <div className="flex space-x-2">
          <Button onClick={handleSearch} size="sm" className="flex-1">
            <Search className="h-4 w-4 mr-2" />
            Search
          </Button>
          <Button onClick={handleClear} variant="outline" size="sm">
            Clear
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};

export default function WorldTradePage() {
  const { activeOffers, tradeHistory, marketSummary, isLoading, error, refreshData } = useTradeData();
  const { searchResults } = useTradeSearch();
  const { setSelectedOffer } = useWorldTradeStore();
  const [activeTab, setActiveTab] = useState('offers');
  
  // Initialize data on component mount
  useEffect(() => {
    refreshData().catch(error => {
      console.error('Failed to load trade data:', error);
      toast.error('Failed to load trade data');
    });
  }, [refreshData]);
  
  const handleRefresh = () => {
    refreshData().catch(error => {
      console.error('Failed to refresh trade data:', error);
      toast.error('Failed to refresh trade data');
    });
  };
  
  const handleOfferSelect = (offer: TradeOffer) => {
    setSelectedOffer(offer);
    // TODO: Open offer detail modal or navigate to detail page
    toast.success(`Selected offer: ${offer.resourceName} from ${offer.sellerName}`);
  };
  
  if (error) {
    return <ErrorMessage error={error} onRetry={handleRefresh} />;
  }
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 to-orange-100 p-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-6">
          <div className="flex justify-between items-center mb-4">
            <div>
              <h1 className="text-3xl font-bold text-amber-900">World Trade</h1>
              <p className="text-amber-700">Mercatus Mundi - Where Venice Meets the World</p>
            </div>
            <Button onClick={handleRefresh} variant="outline" disabled={isLoading}>
              <RefreshCw className={`h-4 w-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
              Refresh
            </Button>
          </div>
          
          {/* Quick Stats */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <Card>
              <CardContent className="p-4 text-center">
                <Package className="h-8 w-8 mx-auto mb-2 text-amber-600" />
                <p className="text-2xl font-bold">{activeOffers.length}</p>
                <p className="text-sm text-gray-600">Active Offers</p>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4 text-center">
                <TrendingUp className="h-8 w-8 mx-auto mb-2 text-green-600" />
                <p className="text-2xl font-bold">{tradeHistory.length}</p>
                <p className="text-sm text-gray-600">Completed Trades</p>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4 text-center">
                <Users className="h-8 w-8 mx-auto mb-2 text-blue-600" />
                <p className="text-2xl font-bold">{new Set([...activeOffers.map(o => o.sellerId), ...activeOffers.map(o => o.buyerId)]).size}</p>
                <p className="text-sm text-gray-600">Active Traders</p>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4 text-center">
                <Package className="h-8 w-8 mx-auto mb-2 text-purple-600" />
                <p className="text-2xl font-bold">{marketSummary.length}</p>
                <p className="text-sm text-gray-600">Resource Types</p>
              </CardContent>
            </Card>
          </div>
        </div>
        
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Sidebar */}
          <div className="lg:col-span-1 space-y-6">
            <FilterPanel />
            <SearchPanel />
          </div>
          
          {/* Main Content */}
          <div className="lg:col-span-3">
            <Tabs value={activeTab} onValueChange={setActiveTab}>
              <TabsList className="grid w-full grid-cols-3">
                <TabsTrigger value="offers">Trade Offers</TabsTrigger>
                <TabsTrigger value="market">Market Overview</TabsTrigger>
                <TabsTrigger value="history">Trade History</TabsTrigger>
              </TabsList>
              
              <TabsContent value="offers" className="mt-6">
                {isLoading ? (
                  <LoadingSpinner />
                ) : (
                  <div>
                    {searchResults.length > 0 && (
                      <div className="mb-6">
                        <h3 className="text-lg font-semibold mb-4">Search Results ({searchResults.length})</h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
                          {searchResults.map((offer) => (
                            <OfferCard
                              key={offer.id}
                              offer={offer}
                              onSelect={handleOfferSelect}
                            />
                          ))}
                        </div>
                      </div>
                    )}
                    
                    <div>
                      <h3 className="text-lg font-semibold mb-4">All Active Offers ({activeOffers.length})</h3>
                      {activeOffers.length === 0 ? (
                        <Card>
                          <CardContent className="p-8 text-center">
                            <Package className="h-12 w-12 mx-auto mb-4 text-gray-400" />
                            <p className="text-gray-600">No active trade offers found</p>
                          </CardContent>
                        </Card>
                      ) : (
                        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
                          {activeOffers.map((offer) => (
                            <OfferCard
                              key={offer.id}
                              offer={offer}
                              onSelect={handleOfferSelect}
                            />
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                )}
              </TabsContent>
              
              <TabsContent value="market" className="mt-6">
                {isLoading ? (
                  <LoadingSpinner />
                ) : (
                  <div>
                    <h3 className="text-lg font-semibold mb-4">Market Overview</h3>
                    {marketSummary.length === 0 ? (
                      <Card>
                        <CardContent className="p-8 text-center">
                          <TrendingUp className="h-12 w-12 mx-auto mb-4 text-gray-400" />
                          <p className="text-gray-600">No market data available</p>
                        </CardContent>
                      </Card>
                    ) : (
                      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
                        {marketSummary.map((market) => (
                          <MarketSummaryCard
                            key={market.resourceType}
                            market={market}
                          />
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </TabsContent>
              
              <TabsContent value="history" className="mt-6">
                {isLoading ? (
                  <LoadingSpinner />
                ) : (
                  <div>
                    <h3 className="text-lg font-semibold mb-4">Recent Trade History ({tradeHistory.length})</h3>
                    {tradeHistory.length === 0 ? (
                      <Card>
                        <CardContent className="p-8 text-center">
                          <Clock className="h-12 w-12 mx-auto mb-4 text-gray-400" />
                          <p className="text-gray-600">No trade history available</p>
                        </CardContent>
                      </Card>
                    ) : (
                      <div className="space-y-4">
                        {tradeHistory.slice(0, 20).map((trade) => (
                          <Card key={trade.id}>
                            <CardContent className="p-4">
                              <div className="flex justify-between items-start">
                                <div>
                                  <h4 className="font-semibold">{trade.resourceName}</h4>
                                  <p className="text-sm text-gray-600">
                                    {trade.sellerName} → {trade.buyerName}
                                  </p>
                                </div>
                                <div className="text-right">
                                  <p className="font-semibold text-amber-600">
                                    {trade.totalPrice.toLocaleString()} ducats
                                  </p>
                                  <p className="text-sm text-gray-600">
                                    {trade.quantity.toLocaleString()} units
                                  </p>
                                </div>
                              </div>
                              <div className="mt-2 text-sm text-gray-500">
                                {new Date(trade.completedAt).toLocaleDateString()} at{' '}
                                {new Date(trade.completedAt).toLocaleTimeString()}
                              </div>
                            </CardContent>
                          </Card>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </TabsContent>
            </Tabs>
          </div>
        </div>
      </div>
    </div>
  );
}