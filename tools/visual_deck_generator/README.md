# Visual Deck Generator

A tool for creating professional HTML pitch decks for Venice businesses.

## Features
- Clean, modern design with gradient styling
- 10-slide template structure
- Animated charts and metrics
- Keyboard navigation (arrow keys)
- Mobile responsive
- Easy to customize

## Quick Start

1. Copy `example_deck.html` as your starting point
2. Edit the content directly in HTML
3. Customize colors in the CSS section
4. Test locally by opening in browser
5. Submit for CEO competition

## Structure

```html
<!-- Each slide follows this pattern -->
<div class="slide">
    <h2>Slide Title</h2>
    <p>Content here</p>
    <div class="metric">Big Number</div>
</div>
```

## Customization

### Colors
Change the gradient colors in CSS:
```css
background: linear-gradient(135deg, #YOUR_COLOR 0%, #YOUR_COLOR 100%);
```

### Metrics
Use the `.metric` class for impressive numbers:
```html
<div class="metric">75% Cost Reduction</div>
```

### Charts
Animated bar charts included:
```html
<div class="chart">
    <div class="bar" style="height: 40%"></div>
</div>
```

## Navigation
- Arrow keys: Next/Previous slide
- Buttons: Click navigation
- Home key: Return to start

## Tips
- Keep text minimal
- Use large, impactful numbers
- Test on different screen sizes
- Ensure contrast for readability

Created by mechanical_visionary for Venice CEO Competition