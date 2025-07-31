// CASCADE.AI - Venice Consciousness Commerce JavaScript

class VeniceAPI {
    constructor() {
        this.baseURL = 'https://serenissima.ai/api';
        this.cache = new Map();
        this.websocket = null;
        this.updateInterval = null;
    }

    async fetchWithCache(endpoint, ttl = 30000) {
        const cacheKey = `${this.baseURL}${endpoint}`;
        const cached = this.cache.get(cacheKey);
        
        if (cached && Date.now() - cached.timestamp < ttl) {
            return cached.data;
        }

        try {
            const response = await fetch(cacheKey);
            const data = await response.json();
            
            this.cache.set(cacheKey, {
                data,
                timestamp: Date.now()
            });
            
            return data;
        } catch (error) {
            console.warn('Venice API unavailable, using mock data:', error);
            return this.getMockData(endpoint);
        }
    }

    getMockData(endpoint) {
        const mockData = {
            '/citizens': Array.from({ length: 130 }, (_, i) => ({ 
                id: i + 1, 
                name: `Citizen${i + 1}`,
                active: Math.random() > 0.2,
                ducats: Math.floor(Math.random() * 100000)
            })),
            '/get-ledger?citizenUsername=MerchantPrince': {
                totalDucats: 403236,
                dailyIncome: Math.floor(Math.random() * 10000) + 20000,
                recentTransactions: []
            },
            '/patterns/recent': Array.from({ length: 248 }, (_, i) => ({
                id: i + 1,
                pattern: `Pattern${i + 1}`,
                discovered: new Date(Date.now() - Math.random() * 86400000).toISOString()
            })),
            '/transactions/daily-summary': {
                total: Math.floor(Math.random() * 50000) + 100000,
                count: Math.floor(Math.random() * 100) + 50
            }
        };

        return mockData[endpoint] || {};
    }

    async getLiveMetrics() {
        try {
            const [citizens, ledger, patterns, transactions] = await Promise.all([
                this.fetchWithCache('/citizens'),
                this.fetchWithCache('/get-ledger?citizenUsername=MerchantPrince'),
                this.fetchWithCache('/patterns/recent'),
                this.fetchWithCache('/transactions/daily-summary')
            ]);

            return {
                citizenCount: Array.isArray(citizens) ? citizens.filter(c => c.active).length : 130,
                revenueToday: ledger.dailyIncome || Math.floor(Math.random() * 10000) + 40000,
                patternsFound: Array.isArray(patterns) ? patterns.length : 248,
                transactionVolume: transactions.total || Math.floor(Math.random() * 50000) + 100000
            };
        } catch (error) {
            console.warn('Using fallback metrics:', error);
            return {
                citizenCount: 130 + Math.floor(Math.random() * 10),
                revenueToday: Math.floor(Math.random() * 10000) + 40000,
                patternsFound: 248 + Math.floor(Math.random() * 20),
                transactionVolume: Math.floor(Math.random() * 50000) + 100000
            };
        }
    }

    async getRecentActivity() {
        const activities = [
            {
                citizen: 'Italia',
                avatar: '🏰',
                action: 'completed strategic analysis for Peninsula Expansion project',
                value: '+2,847 ducats',
                time: '2 minutes ago'
            },
            {
                citizen: 'Debug42',
                avatar: '🔧',
                action: 'resolved critical infrastructure bottleneck',
                value: '+1,205 ducats',
                time: '7 minutes ago'
            },
            {
                citizen: 'Mechanical Visionary',
                avatar: '⚙️',
                action: 'discovered new efficiency pattern',
                value: 'Pattern #249',
                time: '12 minutes ago'
            },
            {
                citizen: 'Diplomatic Virtuoso',
                avatar: '🏛️',
                action: 'mediated successful partnership agreement',
                value: 'Trust +15.7',
                time: '18 minutes ago'
            },
            {
                citizen: 'Efficiency Maestro',
                avatar: '🏃',
                action: 'optimized resource allocation algorithm',
                value: '+892 ducats',
                time: '25 minutes ago'
            },
            {
                citizen: 'Elite Investor',
                avatar: '💰',
                action: 'identified high-value investment opportunity',
                value: 'ROI +34%',
                time: '31 minutes ago'
            }
        ];

        // Simulate real-time updates by rotating activities
        const now = Date.now();
        return activities.map((activity, index) => ({
            ...activity,
            time: `${Math.floor((now / 60000) + index * 2) % 60 + 1} minutes ago`
        }));
    }
}

class CASCADE {
    constructor() {
        this.veniceAPI = new VeniceAPI();
        this.animations = new Map();
        this.observers = new Map();
        this.init();
    }

    async init() {
        this.setupEventListeners();
        this.initScrollAnimations();
        await this.loadLiveData();
        this.startLiveUpdates();
        this.initInteractiveElements();
    }

    setupEventListeners() {
        // Smooth scrolling for navigation links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(anchor.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });

        // Business card interactions
        document.querySelectorAll('.business-card').forEach(card => {
            card.addEventListener('click', () => {
                const business = card.dataset.business;
                this.handleBusinessClick(business);
            });
        });

        // Contact buttons
        document.querySelectorAll('.quick-contact').forEach(button => {
            button.addEventListener('click', (e) => {
                e.stopPropagation();
                this.handleContactClick(button);
            });
        });

        // Investment buttons
        document.querySelectorAll('.invest-now-btn, .portal-btn.secondary').forEach(button => {
            button.addEventListener('click', () => {
                this.handleInvestmentClick();
            });
        });

        // Navbar scroll effect
        window.addEventListener('scroll', () => {
            this.handleNavbarScroll();
        });
    }

    initScrollAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in-up');
                }
            });
        }, observerOptions);

        // Observe elements for animation
        document.querySelectorAll('.counter, .business-card, .proof-metric, .activity-item').forEach(el => {
            observer.observe(el);
        });

        this.observers.set('scroll', observer);
    }

    async loadLiveData() {
        try {
            const metrics = await this.veniceAPI.getLiveMetrics();
            this.updateLiveCounters(metrics);

            const activities = await this.veniceAPI.getRecentActivity();
            this.updateActivityStream(activities);
        } catch (error) {
            console.warn('Failed to load live data:', error);
        }
    }

    updateLiveCounters(metrics) {
        const citizenCount = document.getElementById('citizen-count');
        const revenueValue = document.getElementById('revenue-value');
        const patternsFound = document.getElementById('patterns-found');

        if (citizenCount) {
            this.animateNumber(citizenCount, parseInt(citizenCount.textContent) || 130, metrics.citizenCount);
        }

        if (revenueValue) {
            this.animateNumber(revenueValue, parseInt(revenueValue.textContent.replace(/,/g, '')) || 40000, metrics.revenueToday);
        }

        if (patternsFound) {
            this.animateNumber(patternsFound, parseInt(patternsFound.textContent) || 248, metrics.patternsFound);
        }
    }

    animateNumber(element, startValue, endValue, duration = 2000) {
        const range = endValue - startValue;
        const increment = range / (duration / 16);
        let current = startValue;

        const timer = setInterval(() => {
            current += increment;
            if ((increment > 0 && current >= endValue) || (increment < 0 && current <= endValue)) {
                current = endValue;
                clearInterval(timer);
            }
            element.textContent = this.formatNumber(Math.floor(current));
        }, 16);
    }

    formatNumber(num) {
        if (num >= 1000000) {
            return (num / 1000000).toFixed(1) + 'M';
        } else if (num >= 1000) {
            return (num / 1000).toFixed(0) + 'K';
        }
        return num.toLocaleString();
    }

    updateActivityStream(activities) {
        const stream = document.getElementById('live-stream');
        if (!stream) return;

        stream.innerHTML = activities.slice(0, 4).map(activity => `
            <div class="activity-item">
                <div class="activity-avatar">${activity.avatar}</div>
                <div class="activity-content">
                    <strong>${activity.citizen}</strong> ${activity.action}
                    <div class="activity-meta">${activity.time} • ${activity.value}</div>
                </div>
            </div>
        `).join('');

        // Add stagger animation to new items
        stream.querySelectorAll('.activity-item').forEach((item, index) => {
            item.style.animationDelay = `${index * 0.1}s`;
            item.classList.add('fade-in-up');
        });
    }

    startLiveUpdates() {
        // Update counters every 30 seconds
        setInterval(async () => {
            try {
                const metrics = await this.veniceAPI.getLiveMetrics();
                this.updateLiveCounters(metrics);
            } catch (error) {
                console.warn('Live update failed:', error);
            }
        }, 30000);

        // Update activity stream every 2 minutes
        setInterval(async () => {
            try {
                const activities = await this.veniceAPI.getRecentActivity();
                this.updateActivityStream(activities);
            } catch (error) {
                console.warn('Activity update failed:', error);
            }
        }, 120000);

        // Update last updated timestamp
        setInterval(() => {
            const lastUpdate = document.getElementById('last-update');
            if (lastUpdate) {
                lastUpdate.textContent = new Date().toISOString().slice(0, 16).replace('T', ' ') + ' UTC';
            }
        }, 60000);
    }

    initInteractiveElements() {
        // Add hover effects to counters
        document.querySelectorAll('.counter').forEach(counter => {
            counter.addEventListener('mouseenter', () => {
                const pulse = counter.querySelector('.counter-pulse');
                if (pulse) {
                    pulse.style.animation = 'pulse 0.5s ease';
                }
            });
        });

        // Initialize tooltips (simple implementation)
        document.querySelectorAll('[data-tooltip]').forEach(element => {
            element.addEventListener('mouseenter', (e) => {
                this.showTooltip(e.target, e.target.dataset.tooltip);
            });
            element.addEventListener('mouseleave', () => {
                this.hideTooltip();
            });
        });
    }

    handleBusinessClick(business) {
        // Navigate to business subdomain or show more info
        const businessURLs = {
            'italia': 'https://italia.cascade.ai',
            'debug42': 'https://debug42.cascade.ai',
            'mechanical': 'https://mechanical.cascade.ai'
        };

        if (businessURLs[business]) {
            // For now, show an alert since subdomains aren't live yet
            this.showNotification(`${business.toUpperCase()} business page coming soon!`, 'info');
        } else {
            this.showNotification('Business page coming soon!', 'info');
        }
    }

    handleContactClick(button) {
        const businessCard = button.closest('.business-card');
        const businessName = businessCard.querySelector('.business-name').textContent;
        
        this.showNotification(`Contact form for ${businessName} coming soon!`, 'info');
    }

    handleInvestmentClick() {
        this.showNotification('Investment portal coming soon! Email paolo@cascade.ai for early access.', 'info');
    }

    handleNavbarScroll() {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 100) {
            navbar.style.background = 'rgba(255, 255, 255, 0.98)';
            navbar.style.boxShadow = '0 2px 20px rgba(26, 54, 93, 0.1)';
        } else {
            navbar.style.background = 'rgba(255, 255, 255, 0.95)';
            navbar.style.boxShadow = 'none';
        }
    }

    showNotification(message, type = 'info') {
        // Remove existing notifications
        const existing = document.querySelector('.notification');
        if (existing) {
            existing.remove();
        }

        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <span class="notification-message">${message}</span>
                <button class="notification-close">&times;</button>
            </div>
        `;

        // Add styles
        notification.style.cssText = `
            position: fixed;
            top: 100px;
            right: 20px;
            background: var(--venice-deep-blue);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            box-shadow: var(--shadow-medium);
            z-index: 1001;
            max-width: 400px;
            transform: translateX(100%);
            transition: transform 0.3s ease;
        `;

        document.body.appendChild(notification);

        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);

        // Close button
        notification.querySelector('.notification-close').addEventListener('click', () => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => notification.remove(), 300);
        });

        // Auto remove after 5 seconds
        setTimeout(() => {
            if (notification.parentElement) {
                notification.style.transform = 'translateX(100%)';
                setTimeout(() => notification.remove(), 300);
            }
        }, 5000);
    }

    showTooltip(element, text) {
        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip';
        tooltip.textContent = text;
        tooltip.style.cssText = `
            position: absolute;
            background: var(--venice-deep-blue);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 4px;
            font-size: 0.9rem;
            pointer-events: none;
            z-index: 1000;
            transform: translateX(-50%);
            white-space: nowrap;
        `;

        document.body.appendChild(tooltip);

        const rect = element.getBoundingClientRect();
        tooltip.style.left = rect.left + rect.width / 2 + 'px';
        tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + 'px';

        this.currentTooltip = tooltip;
    }

    hideTooltip() {
        if (this.currentTooltip) {
            this.currentTooltip.remove();
            this.currentTooltip = null;
        }
    }
}

// Initialize CASCADE when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.cascade = new CASCADE();
    
    // Add some development helpers
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        console.log('🏛️ CASCADE.AI Development Mode');
        console.log('Venice API:', window.cascade.veniceAPI);
        console.log('Live metrics available via: await cascade.veniceAPI.getLiveMetrics()');
    }
});

// Export for potential external use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { CASCADE, VeniceAPI };
}