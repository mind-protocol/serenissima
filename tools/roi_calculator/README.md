# ROI Calculator

Interactive business calculator for demonstrating automation savings and ROI.

## Features
- Real-time calculation updates
- Visual results display
- Customizable for any business model
- Mobile-friendly interface
- Professional styling

## Usage

1. Open `calculator.html` in any browser
2. Enter business parameters
3. Calculate ROI automatically
4. Embed in presentations or share with customers

## Customization

### Business Model
Edit the `systemData` object:
```javascript
const systemData = {
    yourProduct: { 
        cost: 50000, 
        laborReduction: 0.75, 
        throughputMultiplier: 10, 
        operators: 2 
    }
};
```

### Calculations
Modify formulas in `calculateROI()`:
- Labor savings
- Throughput value
- Maintenance costs
- ROI calculations

### Styling
Update CSS variables:
- Primary color: `#667eea`
- Success color: `#48bb78`
- Warning color: `#f56565`

## Integration

### In Pitch Deck
```html
<iframe src="calculator.html" width="100%" height="600"></iframe>
```

### As Standalone Tool
Share direct link with potential customers for self-service ROI analysis.

## Parameters

- **Workers**: Current employee count
- **Wage**: Daily wage per worker
- **Hours**: Operating hours per day
- **Throughput**: Units processed daily
- **System Type**: Your product options

## Output Metrics

- Current vs automated costs
- Annual savings
- Throughput improvements
- Payback period
- 5-year net profit
- First year ROI percentage

Created by mechanical_visionary for Venice CEO Competition