'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Brain, Home, Zap, Heart } from 'lucide-react';

export function Navigation() {
  const pathname = usePathname();

  const links = [
    { href: '/', label: 'Home', icon: Home },
    { href: '/consciousness-bridge', label: 'Consciousness Bridge', icon: Heart },
  ];

  return (
    <nav className="bg-gray-900/50 backdrop-blur-sm border-b border-gray-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-2">
            <Zap className="w-6 h-6 text-yellow-400" />
            <span className="text-white font-bold text-xl">Cascade</span>
          </div>
          
          <div className="flex items-center space-x-8">
            {links.map((link) => {
              const Icon = link.icon;
              const isActive = pathname === link.href;
              
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  className={`
                    flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium
                    transition-colors duration-200
                    ${isActive 
                      ? 'text-white bg-gray-800' 
                      : 'text-gray-300 hover:text-white hover:bg-gray-800/50'
                    }
                  `}
                >
                  <Icon className="w-4 h-4" />
                  <span>{link.label}</span>
                </Link>
              );
            })}
          </div>
        </div>
      </div>
    </nav>
  );
}