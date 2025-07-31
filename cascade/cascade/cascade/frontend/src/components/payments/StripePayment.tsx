'use client';

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  CreditCard, 
  Loader2, 
  CheckCircle, 
  AlertCircle,
  DollarSign,
  Coins,
  Shield
} from 'lucide-react';

interface PaymentPackage {
  name: string;
  ducats: number;
  bonus: number;
  price_usd: number;
  total_ducats: number;
  value_per_dollar: number;
}

interface PricingData {
  packages: PaymentPackage[];
  exchange_rate: number;
  custom_minimum: number;
  custom_maximum: number;
}

interface PaymentIntent {
  client_secret: string;
  payment_intent_id: string;
  amount: number;
  currency: string;
  ducat_amount: number;
  exchange_rate: number;
  status: string;
}

export const StripePayment: React.FC = () => {
  const [pricing, setPricing] = useState<PricingData | null>(null);
  const [selectedPackage, setSelectedPackage] = useState<PaymentPackage | null>(null);
  const [customAmount, setCustomAmount] = useState<string>('');
  const [isCustom, setIsCustom] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [paymentStatus, setPaymentStatus] = useState<'idle' | 'processing' | 'success' | 'error'>('idle');
  const [citizenId, setCitizenId] = useState<string>('CodeMonkey'); // Would come from auth

  // Fetch pricing data
  useEffect(() => {
    const fetchPricing = async () => {
      try {
        const response = await fetch('/api/payments/pricing');
        if (response.ok) {
          const data = await response.json();
          setPricing(data);
          if (data.packages.length > 0) {
            setSelectedPackage(data.packages[1]); // Default to "Explorer" package
          }
        }
      } catch (err) {
        console.error('Error fetching pricing:', err);
        setError('Failed to load pricing information');
      }
    };

    fetchPricing();
  }, []);

  const calculateCustomDucats = () => {
    if (!customAmount || !pricing) return 0;
    const amount = parseFloat(customAmount);
    return amount * (1 / pricing.exchange_rate);
  };

  const handlePayment = async () => {
    if (!pricing) return;

    let amount: number;
    let ducatAmount: number;

    if (isCustom) {
      amount = parseFloat(customAmount);
      ducatAmount = calculateCustomDucats();
      
      if (amount < pricing.custom_minimum || amount > pricing.custom_maximum) {
        setError(`Amount must be between $${pricing.custom_minimum} and $${pricing.custom_maximum}`);
        return;
      }
    } else if (selectedPackage) {
      amount = selectedPackage.price_usd;
      ducatAmount = selectedPackage.total_ducats;
    } else {
      setError('Please select a package');
      return;
    }

    setIsLoading(true);
    setError(null);
    setPaymentStatus('processing');

    try {
      // Create payment intent
      const response = await fetch('/api/payments/create-payment-intent', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('cascade_token')}` // JWT token
        },
        body: JSON.stringify({
          amount: amount,
          currency: 'usd',
          citizen_id: citizenId,
          description: isCustom 
            ? `Custom ducat purchase: ${ducatAmount.toFixed(2)} ducats`
            : `${selectedPackage?.name} package: ${ducatAmount} ducats`,
          ducat_amount: ducatAmount
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Payment setup failed');
      }

      const paymentIntent: PaymentIntent = await response.json();

      // Here you would normally integrate with Stripe Elements
      // For demo purposes, we'll simulate payment processing
      await simulatePayment(paymentIntent);

    } catch (err: any) {
      setError(err.message || 'Payment failed');
      setPaymentStatus('error');
    } finally {
      setIsLoading(false);
    }
  };

  // Simulate payment processing (replace with actual Stripe integration)
  const simulatePayment = async (paymentIntent: PaymentIntent) => {
    // Simulate processing time
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Simulate successful payment (90% success rate)
    if (Math.random() > 0.1) {
      setPaymentStatus('success');
      
      // Show success for a few seconds, then reset
      setTimeout(() => {
        setPaymentStatus('idle');
        setSelectedPackage(pricing?.packages[1] || null);
        setCustomAmount('');
        setIsCustom(false);
      }, 3000);
    } else {
      throw new Error('Payment was declined');
    }
  };

  if (!pricing) {
    return (
      <div className="bg-gray-900/80 backdrop-blur-sm rounded-xl p-6">
        <div className="flex items-center justify-center py-8">
          <Loader2 className="w-8 h-8 animate-spin text-purple-400" />
        </div>
      </div>
    );
  }

  return (
    <div className="bg-gray-900/80 backdrop-blur-sm rounded-xl p-6 space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold text-white mb-2">Purchase Ducats</h2>
        <p className="text-gray-400">
          Buy Venice ducats with USD. Current rate: 1 USD = {(1 / pricing.exchange_rate).toFixed(2)} ₫
        </p>
      </div>

      {/* Package Selection */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-white">Select Package</h3>
          <button
            onClick={() => setIsCustom(!isCustom)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              isCustom 
                ? 'bg-purple-500 text-white' 
                : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
            }`}
          >
            Custom Amount
          </button>
        </div>

        {!isCustom ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {pricing.packages.map((pkg) => (
              <motion.div
                key={pkg.name}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => setSelectedPackage(pkg)}
                className={`p-4 rounded-lg border-2 cursor-pointer transition-all ${
                  selectedPackage?.name === pkg.name
                    ? 'border-purple-500 bg-purple-500/10'
                    : 'border-gray-700 bg-gray-800/50 hover:border-gray-600'
                }`}
              >
                <div className="text-center">
                  <h4 className="text-lg font-bold text-white mb-2">{pkg.name}</h4>
                  <div className="text-2xl font-bold text-purple-400 mb-1">
                    ${pkg.price_usd}
                  </div>
                  <div className="text-sm text-gray-400 mb-3">
                    {pkg.total_ducats} ducats total
                  </div>
                  <div className="space-y-1 text-xs text-gray-500">
                    <div>{pkg.ducats} base ducats</div>
                    {pkg.bonus > 0 && (
                      <div className="text-green-400">+{pkg.bonus} bonus ducats</div>
                    )}
                    <div>{pkg.value_per_dollar.toFixed(1)} ₫ per $1</div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        ) : (
          <div className="bg-gray-800/50 rounded-lg p-4">
            <label className="block text-sm font-medium text-gray-400 mb-2">
              Custom Amount (USD)
            </label>
            <div className="flex space-x-4">
              <div className="flex-1">
                <input
                  type="number"
                  value={customAmount}
                  onChange={(e) => setCustomAmount(e.target.value)}
                  placeholder="Enter USD amount"
                  min={pricing.custom_minimum}
                  max={pricing.custom_maximum}
                  className="w-full bg-gray-800 text-white px-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
                <div className="text-xs text-gray-500 mt-1">
                  Min: ${pricing.custom_minimum} | Max: ${pricing.custom_maximum}
                </div>
              </div>
              <div className="w-32">
                <div className="bg-gray-700 px-4 py-3 rounded-lg text-center">
                  <div className="text-sm text-gray-400">You get</div>
                  <div className="text-lg font-bold text-purple-400">
                    {calculateCustomDucats().toFixed(0)} ₫
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Payment Summary */}
      {(selectedPackage || (isCustom && customAmount)) && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gradient-to-r from-purple-500/10 to-pink-500/10 rounded-lg p-4 border border-purple-500/20"
        >
          <h4 className="text-sm font-medium text-gray-400 mb-3">Payment Summary</h4>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-400">Amount (USD)</span>
              <span className="text-white">
                ${isCustom ? customAmount : selectedPackage?.price_usd.toFixed(2)}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Ducats</span>
              <span className="text-white">
                {isCustom ? calculateCustomDucats().toFixed(0) : selectedPackage?.total_ducats} ₫
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Exchange Rate</span>
              <span className="text-white">
                1 USD = {(1 / pricing.exchange_rate).toFixed(2)} ₫
              </span>
            </div>
            {!isCustom && selectedPackage?.bonus > 0 && (
              <div className="flex justify-between text-green-400">
                <span>Bonus Ducats</span>
                <span>+{selectedPackage.bonus} ₫</span>
              </div>
            )}
          </div>
        </motion.div>
      )}

      {/* Error Display */}
      {error && (
        <div className="flex items-center space-x-2 text-red-400 text-sm bg-red-500/10 rounded-lg p-3 border border-red-500/20">
          <AlertCircle className="w-4 h-4" />
          <span>{error}</span>
        </div>
      )}

      {/* Payment Status */}
      <AnimatePresence>
        {paymentStatus === 'success' && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
            className="flex items-center space-x-2 text-green-400 text-sm bg-green-500/10 rounded-lg p-3 border border-green-500/20"
          >
            <CheckCircle className="w-5 h-5" />
            <span>Payment successful! Ducats have been credited to your account.</span>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Payment Button */}
      <motion.button
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        onClick={handlePayment}
        disabled={isLoading || paymentStatus === 'processing' || (!selectedPackage && !customAmount)}
        className={`w-full py-4 rounded-lg font-medium transition-all flex items-center justify-center space-x-2 ${
          isLoading || paymentStatus === 'processing' || (!selectedPackage && !customAmount)
            ? 'bg-gray-700 text-gray-500 cursor-not-allowed'
            : 'bg-gradient-to-r from-purple-500 to-pink-500 text-white hover:opacity-90'
        }`}
      >
        {isLoading || paymentStatus === 'processing' ? (
          <>
            <Loader2 className="w-5 h-5 animate-spin" />
            <span>Processing Payment...</span>
          </>
        ) : (
          <>
            <CreditCard className="w-5 h-5" />
            <span>Purchase Ducats</span>
          </>
        )}
      </motion.button>

      {/* Security Notice */}
      <div className="bg-blue-500/10 rounded-lg p-4 border border-blue-500/20">
        <div className="flex items-start space-x-3">
          <Shield className="w-5 h-5 text-blue-400 flex-shrink-0 mt-0.5" />
          <div className="text-sm text-gray-300">
            <p className="mb-1">
              Payments are processed securely through Stripe. Your payment information is encrypted and never stored on our servers.
            </p>
            <p>
              Purchased ducats are immediately credited to your Venice citizen account and can be used across the entire Venice ecosystem.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};