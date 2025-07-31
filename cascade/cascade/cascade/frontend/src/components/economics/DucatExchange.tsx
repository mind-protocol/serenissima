'use client';

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  TrendingUp, 
  TrendingDown, 
  ArrowUpDown,
  Info,
  Loader2,
  AlertCircle
} from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

interface ExchangeRate {
  ducat_to_usd: number;
  usd_to_ducat: number;
  last_updated: string;
  confidence: number;
  trend: 'up' | 'down' | 'stable';
  volume_24h: {
    ducat: number;
    usd: number;
  };
}

interface ConversionResult {
  from_amount: number;
  from_currency: string;
  to_amount: number;
  to_currency: string;
  exchange_rate: number;
  fee_amount: number;
  fee_currency: string;
  total_cost: number;
  timestamp: string;
}

export const DucatExchange: React.FC = () => {
  const [exchangeRate, setExchangeRate] = useState<ExchangeRate | null>(null);
  const [rateHistory, setRateHistory] = useState<any[]>([]);
  const [fromCurrency, setFromCurrency] = useState<'ducat' | 'usd'>('ducat');
  const [toCurrency, setToCurrency] = useState<'ducat' | 'usd'>('usd');
  const [amount, setAmount] = useState<string>('100');
  const [conversionResult, setConversionResult] = useState<ConversionResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Fetch current exchange rate
  useEffect(() => {
    const fetchExchangeRate = async () => {
      try {
        const response = await fetch('/api/economics/exchange-rate');
        if (response.ok) {
          const data = await response.json();
          setExchangeRate(data);
        }
      } catch (err) {
        console.error('Error fetching exchange rate:', err);
      }
    };

    fetchExchangeRate();
    const interval = setInterval(fetchExchangeRate, 30000); // Update every 30 seconds

    return () => clearInterval(interval);
  }, []);

  // Fetch rate history
  useEffect(() => {
    const fetchRateHistory = async () => {
      try {
        const response = await fetch('/api/economics/exchange-rate/history?hours=24&interval=hourly');
        if (response.ok) {
          const data = await response.json();
          setRateHistory(data.history);
        }
      } catch (err) {
        console.error('Error fetching rate history:', err);
      }
    };

    fetchRateHistory();
  }, []);

  const handleSwapCurrencies = () => {
    setFromCurrency(toCurrency);
    setToCurrency(fromCurrency);
    setConversionResult(null);
  };

  const handleConvert = async () => {
    if (!amount || parseFloat(amount) <= 0) {
      setError('Please enter a valid amount');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/economics/convert', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          amount: parseFloat(amount),
          from_currency: fromCurrency,
          to_currency: toCurrency,
          include_fee: true,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setConversionResult(data);
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Conversion failed');
      }
    } catch (err) {
      setError('Failed to convert currency');
    } finally {
      setIsLoading(false);
    }
  };

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'up':
        return <TrendingUp className="w-4 h-4 text-green-400" />;
      case 'down':
        return <TrendingDown className="w-4 h-4 text-red-400" />;
      default:
        return <ArrowUpDown className="w-4 h-4 text-gray-400" />;
    }
  };

  const formatCurrency = (value: number, currency: string) => {
    if (currency === 'usd') {
      return `$${value.toFixed(2)}`;
    }
    return `${value.toFixed(2)} ₫`;
  };

  return (
    <div className="bg-gray-900/80 backdrop-blur-sm rounded-xl p-6 space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold text-white mb-2">Ducat Exchange</h2>
        <p className="text-gray-400">Convert between Venice ducats and USD</p>
      </div>

      {/* Current Exchange Rate */}
      {exchangeRate && (
        <div className="bg-gray-800/50 rounded-lg p-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-gray-400">Current Rate</span>
            <div className="flex items-center space-x-2">
              {getTrendIcon(exchangeRate.trend)}
              <span className="text-xs text-gray-500 capitalize">{exchangeRate.trend}</span>
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <div className="text-2xl font-bold text-white">
                ${exchangeRate.ducat_to_usd.toFixed(4)}
              </div>
              <div className="text-sm text-gray-400">1 Ducat → USD</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-white">
                {exchangeRate.usd_to_ducat.toFixed(2)} ₫
              </div>
              <div className="text-sm text-gray-400">1 USD → Ducat</div>
            </div>
          </div>
          <div className="mt-3 flex items-center justify-between text-xs text-gray-500">
            <span>Confidence: {(exchangeRate.confidence * 100).toFixed(0)}%</span>
            <span>Updated: {new Date(exchangeRate.last_updated).toLocaleTimeString()}</span>
          </div>
        </div>
      )}

      {/* Exchange Rate Chart */}
      {rateHistory.length > 0 && (
        <div className="bg-gray-800/30 rounded-lg p-4">
          <h3 className="text-sm font-medium text-gray-400 mb-3">24h Exchange Rate</h3>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={rateHistory}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis 
                dataKey="timestamp" 
                stroke="#9ca3af" 
                fontSize={12}
                tickFormatter={(value) => new Date(value).getHours() + ':00'}
              />
              <YAxis 
                stroke="#9ca3af" 
                fontSize={12}
                domain={['dataMin - 0.005', 'dataMax + 0.005']}
              />
              <Tooltip 
                contentStyle={{ backgroundColor: '#1f2937', border: 'none', borderRadius: '8px' }}
                labelStyle={{ color: '#9ca3af' }}
                formatter={(value: number) => `$${value.toFixed(4)}`}
              />
              <Line 
                type="monotone" 
                dataKey="rate" 
                stroke="#8b5cf6" 
                strokeWidth={2}
                dot={{ fill: '#8b5cf6', r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Conversion Form */}
      <div className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-400 mb-2">From</label>
            <div className="flex space-x-2">
              <input
                type="number"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                placeholder="0.00"
                className="flex-1 bg-gray-800 text-white px-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
              />
              <select
                value={fromCurrency}
                onChange={(e) => setFromCurrency(e.target.value as 'ducat' | 'usd')}
                className="bg-gray-800 text-white px-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
              >
                <option value="ducat">Ducat</option>
                <option value="usd">USD</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-400 mb-2">To</label>
            <div className="flex space-x-2">
              <div className="flex-1 bg-gray-800 text-gray-400 px-4 py-2 rounded-lg">
                {conversionResult ? formatCurrency(conversionResult.to_amount, conversionResult.to_currency) : '0.00'}
              </div>
              <select
                value={toCurrency}
                onChange={(e) => setToCurrency(e.target.value as 'ducat' | 'usd')}
                className="bg-gray-800 text-white px-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
              >
                <option value="ducat">Ducat</option>
                <option value="usd">USD</option>
              </select>
            </div>
          </div>
        </div>

        <div className="flex justify-center">
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={handleSwapCurrencies}
            className="p-2 bg-gray-800 rounded-full hover:bg-gray-700 transition-colors"
          >
            <ArrowUpDown className="w-5 h-5 text-gray-400" />
          </motion.button>
        </div>

        {error && (
          <div className="flex items-center space-x-2 text-red-400 text-sm">
            <AlertCircle className="w-4 h-4" />
            <span>{error}</span>
          </div>
        )}

        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={handleConvert}
          disabled={isLoading || fromCurrency === toCurrency}
          className={`w-full py-3 rounded-lg font-medium transition-all ${
            isLoading || fromCurrency === toCurrency
              ? 'bg-gray-700 text-gray-500 cursor-not-allowed'
              : 'bg-gradient-to-r from-purple-500 to-pink-500 text-white hover:opacity-90'
          }`}
        >
          {isLoading ? (
            <Loader2 className="w-5 h-5 animate-spin mx-auto" />
          ) : (
            'Convert'
          )}
        </motion.button>
      </div>

      {/* Conversion Result */}
      <AnimatePresence>
        {conversionResult && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="bg-gradient-to-r from-purple-500/10 to-pink-500/10 rounded-lg p-4 border border-purple-500/20"
          >
            <h4 className="text-sm font-medium text-gray-400 mb-3">Conversion Details</h4>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-400">Amount</span>
                <span className="text-white">
                  {formatCurrency(conversionResult.from_amount, conversionResult.from_currency)}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Exchange Rate</span>
                <span className="text-white">
                  1 {conversionResult.from_currency.toUpperCase()} = {conversionResult.exchange_rate.toFixed(4)} {conversionResult.to_currency.toUpperCase()}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Fee (2.5%)</span>
                <span className="text-white">
                  {formatCurrency(conversionResult.fee_amount, conversionResult.fee_currency)}
                </span>
              </div>
              <div className="border-t border-gray-700 pt-2 flex justify-between font-medium">
                <span className="text-gray-300">You Receive</span>
                <span className="text-white">
                  {formatCurrency(conversionResult.to_amount, conversionResult.to_currency)}
                </span>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Info Box */}
      <div className="bg-blue-500/10 rounded-lg p-4 border border-blue-500/20">
        <div className="flex items-start space-x-3">
          <Info className="w-5 h-5 text-blue-400 flex-shrink-0 mt-0.5" />
          <div className="text-sm text-gray-300">
            <p className="mb-1">
              The ducat exchange rate is dynamically determined by Venice economic activity, 
              consciousness levels, and platform usage.
            </p>
            <p>
              Higher consciousness levels strengthen the ducat, creating a unique 
              consciousness-backed currency system.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};