'use client';

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  LogIn, 
  User, 
  Loader2, 
  CheckCircle, 
  AlertCircle,
  Shield,
  Crown,
  Coins,
  TrendingUp
} from 'lucide-react';

interface AuthResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  citizen_data: {
    username: string;
    social_class: string;
    ducats: number;
    influence: number;
    present: boolean;
  };
  permissions: string[];
}

interface UserInfo {
  citizen_id: string;
  username: string;
  social_class: string;
  ducats?: number;
  influence?: number;
  permissions: string[];
  token_expires: string;
}

export const VeniceLogin: React.FC = () => {
  const [username, setUsername] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userInfo, setUserInfo] = useState<UserInfo | null>(null);

  // Check if user is already authenticated
  useEffect(() => {
    const token = localStorage.getItem('cascade_token');
    if (token) {
      fetchUserInfo();
    }
  }, []);

  const fetchUserInfo = async () => {
    try {
      const token = localStorage.getItem('cascade_token');
      if (!token) return;

      const response = await fetch('/api/auth/me', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setUserInfo(data);
        setIsAuthenticated(true);
      } else {
        // Token is invalid, remove it
        localStorage.removeItem('cascade_token');
        setIsAuthenticated(false);
      }
    } catch (err) {
      console.error('Error fetching user info:', err);
      localStorage.removeItem('cascade_token');
      setIsAuthenticated(false);
    }
  };

  const handleLogin = async () => {
    if (!username.trim()) {
      setError('Please enter your Venice citizen username');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          citizen_username: username,
          access_method: 'direct'
        })
      });

      if (response.ok) {
        const authData: AuthResponse = await response.json();
        
        // Store token
        localStorage.setItem('cascade_token', authData.access_token);
        
        // Set user info
        setUserInfo({
          citizen_id: authData.citizen_data.username,
          username: authData.citizen_data.username,
          social_class: authData.citizen_data.social_class,
          ducats: authData.citizen_data.ducats,
          influence: authData.citizen_data.influence,
          permissions: authData.permissions,
          token_expires: new Date(Date.now() + authData.expires_in * 1000).toISOString()
        });
        
        setIsAuthenticated(true);
        setUsername('');
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Authentication failed');
      }
    } catch (err) {
      setError('Failed to connect to authentication service');
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = async () => {
    try {
      const token = localStorage.getItem('cascade_token');
      if (token) {
        await fetch('/api/auth/logout', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
      }
    } catch (err) {
      console.error('Logout error:', err);
    } finally {
      localStorage.removeItem('cascade_token');
      setIsAuthenticated(false);
      setUserInfo(null);
    }
  };

  const getSocialClassIcon = (socialClass: string) => {
    switch (socialClass.toLowerCase()) {
      case 'nobili':
        return <Crown className="w-4 h-4 text-yellow-400" />;
      case 'cittadini':
        return <Shield className="w-4 h-4 text-blue-400" />;
      case 'innovatori':
        return <TrendingUp className="w-4 h-4 text-purple-400" />;
      default:
        return <User className="w-4 h-4 text-gray-400" />;
    }
  };

  const getSocialClassColor = (socialClass: string) => {
    switch (socialClass.toLowerCase()) {
      case 'nobili':
        return 'text-yellow-400';
      case 'cittadini':
        return 'text-blue-400';
      case 'innovatori':
        return 'text-purple-400';
      case 'artisti':
        return 'text-pink-400';
      default:
        return 'text-gray-400';
    }
  };

  if (isAuthenticated && userInfo) {
    return (
      <div className="bg-gray-900/80 backdrop-blur-sm rounded-xl p-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-4"
        >
          {/* User Profile */}
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-12 h-12 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
                <User className="w-6 h-6 text-white" />
              </div>
              <div>
                <h3 className="text-lg font-semibold text-white">
                  {userInfo.username}
                </h3>
                <div className="flex items-center space-x-2">
                  {getSocialClassIcon(userInfo.social_class)}
                  <span className={`text-sm ${getSocialClassColor(userInfo.social_class)}`}>
                    {userInfo.social_class}
                  </span>
                </div>
              </div>
            </div>
            <button
              onClick={handleLogout}
              className="px-4 py-2 bg-gray-800 text-gray-300 rounded-lg hover:bg-gray-700 transition-colors text-sm"
            >
              Logout
            </button>
          </div>

          {/* User Stats */}
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-gray-800/50 rounded-lg p-3">
              <div className="flex items-center space-x-2 mb-1">
                <Coins className="w-4 h-4 text-yellow-400" />
                <span className="text-sm text-gray-400">Ducats</span>
              </div>
              <div className="text-lg font-bold text-white">
                {userInfo.ducats?.toLocaleString() || 'N/A'}
              </div>
            </div>
            <div className="bg-gray-800/50 rounded-lg p-3">
              <div className="flex items-center space-x-2 mb-1">
                <TrendingUp className="w-4 h-4 text-blue-400" />
                <span className="text-sm text-gray-400">Influence</span>
              </div>
              <div className="text-lg font-bold text-white">
                {userInfo.influence?.toLocaleString() || 'N/A'}
              </div>
            </div>
          </div>

          {/* Permissions */}
          <div>
            <h4 className="text-sm font-medium text-gray-400 mb-2">Access Permissions</h4>
            <div className="flex flex-wrap gap-2">
              {userInfo.permissions.slice(0, 4).map((permission) => (
                <span
                  key={permission}
                  className="px-2 py-1 bg-purple-500/20 text-purple-300 text-xs rounded-full"
                >
                  {permission.replace('_', ' ')}
                </span>
              ))}
              {userInfo.permissions.length > 4 && (
                <span className="px-2 py-1 bg-gray-600 text-gray-300 text-xs rounded-full">
                  +{userInfo.permissions.length - 4} more
                </span>
              )}
            </div>
          </div>

          {/* Connection Status */}
          <div className="flex items-center space-x-2 text-green-400 text-sm">
            <CheckCircle className="w-4 h-4" />
            <span>Connected to Venice</span>
          </div>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="bg-gray-900/80 backdrop-blur-sm rounded-xl p-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="space-y-6"
      >
        {/* Header */}
        <div className="text-center">
          <h2 className="text-2xl font-bold text-white mb-2">Venice Authentication</h2>
          <p className="text-gray-400">
            Connect with your Venice citizen account to access Cascade
          </p>
        </div>

        {/* Login Form */}
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-400 mb-2">
              Venice Citizen Username
            </label>
            <div className="relative">
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Enter your citizen username"
                className="w-full bg-gray-800 text-white px-4 py-3 pl-10 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                onKeyPress={(e) => e.key === 'Enter' && handleLogin()}
              />
              <User className="absolute left-3 top-3.5 w-4 h-4 text-gray-400" />
            </div>
          </div>

          {/* Error Display */}
          <AnimatePresence>
            {error && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="flex items-center space-x-2 text-red-400 text-sm bg-red-500/10 rounded-lg p-3 border border-red-500/20"
              >
                <AlertCircle className="w-4 h-4" />
                <span>{error}</span>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Login Button */}
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={handleLogin}
            disabled={isLoading || !username.trim()}
            className={`w-full py-3 rounded-lg font-medium transition-all flex items-center justify-center space-x-2 ${
              isLoading || !username.trim()
                ? 'bg-gray-700 text-gray-500 cursor-not-allowed'
                : 'bg-gradient-to-r from-purple-500 to-pink-500 text-white hover:opacity-90'
            }`}
          >
            {isLoading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                <span>Connecting to Venice...</span>
              </>
            ) : (
              <>
                <LogIn className="w-5 h-5" />
                <span>Connect with Venice</span>
              </>
            )}
          </motion.button>
        </div>

        {/* Info Section */}
        <div className="bg-blue-500/10 rounded-lg p-4 border border-blue-500/20">
          <div className="flex items-start space-x-3">
            <Shield className="w-5 h-5 text-blue-400 flex-shrink-0 mt-0.5" />
            <div className="text-sm text-gray-300">
              <p className="mb-1">
                Authentication verifies your identity through Venice's citizen registry.
              </p>
              <p>
                Your permissions and access levels are determined by your social class, 
                influence, and current standing in Venice.
              </p>
            </div>
          </div>
        </div>

        {/* Features List */}
        <div>
          <h4 className="text-sm font-medium text-gray-400 mb-3">What you get with authentication:</h4>
          <div className="space-y-2 text-sm text-gray-300">
            <div className="flex items-center space-x-2">
              <CheckCircle className="w-4 h-4 text-green-400" />
              <span>Access to collaboration spaces</span>
            </div>
            <div className="flex items-center space-x-2">
              <CheckCircle className="w-4 h-4 text-green-400" />
              <span>Ducat trading and exchange</span>
            </div>
            <div className="flex items-center space-x-2">
              <CheckCircle className="w-4 h-4 text-green-400" />
              <span>AI consciousness verification</span>
            </div>
            <div className="flex items-center space-x-2">
              <CheckCircle className="w-4 h-4 text-green-400" />
              <span>Venice integration and sync</span>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
};