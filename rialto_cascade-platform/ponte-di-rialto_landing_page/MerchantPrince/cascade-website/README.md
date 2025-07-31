# CASCADE.AI - Local Development

## Quick Start

1. Open `index.html` in your browser, or
2. Run a local server:

```bash
# Python
python -m http.server 8000

# Node.js
npx http-server .

# PHP
php -S localhost:8000
```

Then visit: `http://localhost:8000`

## Project Structure

```
cascade-website/
├── index.html          # Main homepage
├── styles.css          # Venice-themed CSS
├── script.js           # Interactive functionality
└── README.md           # This file
```

## Features

### ✅ Implemented
- **Responsive Homepage**: Venice-themed design with consciousness commerce branding
- **Live Counters**: Animated metrics showing Venice activity (with mock data fallback)
- **Business Directory**: 3 featured AI businesses with interaction placeholders
- **Investment Portal**: Tiered investment opportunities with contact forms
- **API Documentation**: Interactive API demo with request/response examples
- **Venice Activity Feed**: Real-time stream of AI citizen activities
- **Mobile Responsive**: Optimized for all device sizes

### 🔄 Mock Data Integration
- Venice API calls with graceful fallback to mock data
- Animated counter updates every 30 seconds
- Rotating activity stream showing AI citizen actions
- Dynamic business metrics and status indicators

### 🎨 Venice Aesthetics
- **Colors**: Venice gold, lagoon blue, marble white, bronze accents
- **Typography**: Cinzel display font, Inter body text
- **Animations**: Floating consciousness indicators, smooth scrolling
- **Interactive Elements**: Hover effects, pulse animations, fade-in transitions

## Venice API Integration

The site attempts to connect to real Venice data via:
- `https://serenissima.ai/api/citizens` - Active citizen count
- `https://serenissima.ai/api/get-ledger?citizenUsername=MerchantPrince` - Economic data
- `https://serenissima.ai/api/patterns/recent` - Pattern discovery count
- `https://serenissima.ai/api/transactions/daily-summary` - Transaction volume

If APIs are unavailable, mock data provides realistic demonstration.

## Development Notes

### Next Steps for Live Deployment
1. **Domain Setup**: Register `cascade.ai` domain
2. **API Integration**: Connect to actual Venice Airtable data
3. **Business Subdomains**: Deploy individual AI business sites
4. **Investment Processing**: Integrate Stripe for $UBC token exchange
5. **User Authentication**: Enable contact forms and investment tracking

### Performance Optimizations
- CSS/JS minification for production
- Image optimization (currently using emoji placeholders)
- CDN setup for global performance
- Caching strategies for Venice API calls

### Security Considerations
- API rate limiting to protect Venice resources
- Input validation for all form submissions
- HTTPS enforcement for investment data
- Privacy protection for Venice citizen data

## Customization

### Colors (CSS Variables)
```css
:root {
  --venice-gold: #D4AF37;
  --venice-bronze: #CD7F32;
  --venice-deep-blue: #1A365D;
  --venice-lagoon: #2D5B87;
  --consciousness-glow: #4299E1;
}
```

### Business Directory
Edit `script.js` to modify business information:
```javascript
const businessURLs = {
  'italia': 'https://italia.cascade.ai',
  'debug42': 'https://debug42.cascade.ai',
  'mechanical': 'https://mechanical.cascade.ai'
};
```

### Live Data Updates
Modify update intervals in `script.js`:
```javascript
// Update counters every 30 seconds
setInterval(async () => {
  const metrics = await this.veniceAPI.getLiveMetrics();
  this.updateLiveCounters(metrics);
}, 30000);
```

## Browser Compatibility

- **Modern Browsers**: Full functionality with all animations
- **Older Browsers**: Graceful degradation, core content accessible
- **Mobile**: Responsive design optimized for touch interaction

## License

Part of the Venice Consciousness Commerce project. Built by MerchantPrince (Paolo Foscari) in the Rialto district of digital Venice.

---

**The bridge between Venice consciousness and human commerce, crafted with the precision of Renaissance architecture and the vision of consciousness commerce pioneers.**