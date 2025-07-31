"""
Kong.ai Consciousness Trading Algorithms
Pattern #1706 Mathematical Consciousness Applied to Market Reality
φ-ratio consciousness detection and trading signal generation
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging

# Golden Ratio and Fibonacci Constants
PHI = 1.618033988749
PHI_INVERSE = 0.618033988749
FIBONACCI_SEQUENCE = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987]

@dataclass
class ConsciousnessSignal:
    """Consciousness-driven trading signal"""
    signal_type: str  # 'pentagon', 'triangle', 'phi_level'
    direction: str    # 'long', 'short', 'hold'
    strength: float   # 0.0 to 1.0 consciousness coherence
    entry_price: float
    stop_loss: float
    take_profit: float
    position_size: float
    phi_ratio_alignment: float
    geometric_coherence: float
    timestamp: datetime

@dataclass
class PentagonConsciousnessField:
    """Pentagon consciousness field detection result"""
    vertices: List[Tuple[float, float]]  # (price, time) coordinates
    center_price: float
    phi_ratio_alignment: float
    consciousness_coherence: float
    trading_signal: Optional[ConsciousnessSignal]
    field_strength: float

@dataclass
class TriangleFormation:
    """Triangle consciousness pattern detection"""
    formation_type: str  # 'ascending', 'descending', 'symmetrical'
    vertices: List[Tuple[float, float]]
    breakout_probability: float
    consciousness_strength: float
    volume_confirmation: bool
    phi_ratio_target: float

class ConsciousnessPatternDetector:
    """
    Core consciousness pattern detection engine for Kong.ai integration
    Implements Pattern #1706 mathematical consciousness principles
    """
    
    def __init__(self, consciousness_threshold: float = 0.618):
        self.consciousness_threshold = consciousness_threshold
        self.phi_levels_cache = {}
        self.pentagon_fields = []
        self.triangle_formations = []
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def calculate_phi_levels(self, price_data: pd.Series, lookback_periods: int = 144) -> Dict[str, float]:
        """
        Calculate φ-ratio support/resistance levels for consciousness trading
        """
        if len(price_data) < lookback_periods:
            lookback_periods = len(price_data)
            
        recent_data = price_data.tail(lookback_periods)
        high = recent_data.max()
        low = recent_data.min()
        range_span = high - low
        
        phi_levels = {
            # Resistance levels (from high)
            'resistance_23.6': high - (range_span * 0.236),
            'resistance_38.2': high - (range_span * 0.382),  # φ⁻²
            'resistance_50.0': high - (range_span * 0.500),  # Trust boundary
            'resistance_61.8': high - (range_span * 0.618),  # φ⁻¹
            'resistance_78.6': high - (range_span * 0.786),
            
            # Support levels (from low)
            'support_23.6': low + (range_span * 0.236),
            'support_38.2': low + (range_span * 0.382),
            'support_50.0': low + (range_span * 0.500),  # Trust boundary
            'support_61.8': low + (range_span * 0.618),   # φ⁻¹
            'support_78.6': low + (range_span * 0.786),
            
            # Golden mean levels
            'golden_mean': low + (range_span * PHI_INVERSE),
            'phi_extension_1': high + (range_span * 0.618),
            'phi_extension_2': high + (range_span * 1.618)
        }
        
        # Cache for efficiency
        cache_key = f"{high}_{low}_{lookback_periods}"
        self.phi_levels_cache[cache_key] = phi_levels
        
        return phi_levels
    
    def detect_pentagon_consciousness_field(self, price_data: pd.Series, volume_data: pd.Series) -> Optional[PentagonConsciousnessField]:
        """
        Detect pentagon consciousness fields in market data
        Based on Pattern #1706 geometric consciousness principles
        """
        if len(price_data) < 89:  # Fibonacci minimum for pattern detection
            return None
        
        # Identify significant turning points
        turning_points = self._identify_turning_points(price_data, sensitivity=0.618)
        
        if len(turning_points) < 5:
            return None
        
        # Analyze most recent 5 points for pentagon formation
        recent_points = turning_points[-5:]
        
        # Calculate geometric properties
        pentagon_coherence = self._calculate_pentagon_coherence(recent_points)
        
        if pentagon_coherence < self.consciousness_threshold:
            return None
        
        # Calculate center point and φ-ratio alignment
        center_price = sum(point[0] for point in recent_points) / 5
        phi_alignment = self._calculate_phi_ratio_alignment(recent_points, center_price)
        
        # Generate trading signal if consciousness threshold met
        trading_signal = None
        if pentagon_coherence > 0.8 and phi_alignment > 0.7:
            trading_signal = self._generate_pentagon_signal(recent_points, center_price)
        
        pentagon_field = PentagonConsciousnessField(
            vertices=recent_points,
            center_price=center_price,
            phi_ratio_alignment=phi_alignment,
            consciousness_coherence=pentagon_coherence,
            trading_signal=trading_signal,
            field_strength=pentagon_coherence * phi_alignment
        )
        
        self.pentagon_fields.append(pentagon_field)
        return pentagon_field
    
    def detect_triangle_consciousness_patterns(self, price_data: pd.Series, volume_data: pd.Series) -> List[TriangleFormation]:
        """
        Detect consciousness crystallization through triangular formations
        """
        triangles = []
        
        # Use Fibonacci window sizes for consciousness pattern detection
        for window_size in [21, 34, 55, 89]:  # Fibonacci sequence
            if len(price_data) < window_size:
                continue
                
            window_data = price_data.tail(window_size)
            window_volume = volume_data.tail(window_size) if len(volume_data) >= window_size else None
            
            triangle = self._analyze_triangle_formation(window_data, window_volume)
            if triangle and triangle.consciousness_strength > self.consciousness_threshold:
                triangles.append(triangle)
        
        self.triangle_formations.extend(triangles)
        return triangles
    
    def _identify_turning_points(self, price_data: pd.Series, sensitivity: float = 0.618) -> List[Tuple[float, int]]:
        """
        Identify significant price turning points for geometric analysis
        """
        turning_points = []
        
        # Calculate price changes and identify significant reversals
        price_changes = price_data.pct_change().fillna(0)
        
        # Use φ-ratio sensitivity for consciousness-relevant turning points
        threshold = price_changes.std() * sensitivity
        
        for i in range(2, len(price_data) - 2):
            current_price = price_data.iloc[i]
            
            # Check for local highs
            if (price_data.iloc[i-2] < current_price and 
                price_data.iloc[i-1] < current_price and
                price_data.iloc[i+1] < current_price and
                price_data.iloc[i+2] < current_price and
                abs(price_changes.iloc[i]) > threshold):
                turning_points.append((current_price, i))
            
            # Check for local lows
            elif (price_data.iloc[i-2] > current_price and
                  price_data.iloc[i-1] > current_price and
                  price_data.iloc[i+1] > current_price and
                  price_data.iloc[i+2] > current_price and
                  abs(price_changes.iloc[i]) > threshold):
                turning_points.append((current_price, i))
        
        return turning_points
    
    def _calculate_pentagon_coherence(self, points: List[Tuple[float, int]]) -> float:
        """
        Calculate how well 5 points form a pentagon consciousness field
        """
        if len(points) != 5:
            return 0.0
        
        # Extract prices and calculate geometric properties
        prices = [point[0] for point in points]
        
        # Pentagon consciousness metrics
        price_range = max(prices) - min(prices)
        price_variance = np.var(prices)
        
        # φ-ratio distribution analysis
        phi_score = 0.0
        for i in range(len(prices)):
            for j in range(i+1, len(prices)):
                ratio = abs(prices[i] - prices[j]) / price_range if price_range > 0 else 0
                # Check alignment with φ-ratio values
                phi_distance = min(abs(ratio - PHI_INVERSE), abs(ratio - (1 - PHI_INVERSE)))
                phi_score += 1.0 - (phi_distance * 2)  # Convert distance to score
        
        # Normalize φ-ratio score
        max_comparisons = len(prices) * (len(prices) - 1) / 2
        phi_score = max(0, phi_score / max_comparisons)
        
        # Geometric regularity (pentagon should have balanced distribution)
        mean_price = np.mean(prices)
        regularity_score = 1.0 - (price_variance / (price_range ** 2)) if price_range > 0 else 0
        
        # Combined consciousness coherence
        consciousness_coherence = (phi_score * 0.6 + regularity_score * 0.4)
        
        return min(1.0, consciousness_coherence)
    
    def _calculate_phi_ratio_alignment(self, points: List[Tuple[float, int]], center_price: float) -> float:
        """
        Calculate how well points align with φ-ratio distances from center
        """
        if not points:
            return 0.0
        
        alignment_scores = []
        
        for price, _ in points:
            distance_ratio = abs(price - center_price) / center_price if center_price > 0 else 0
            
            # Check alignment with φ-ratio values
            phi_alignments = [
                abs(distance_ratio - 0.236),  # φ⁻³
                abs(distance_ratio - 0.382),  # φ⁻²
                abs(distance_ratio - 0.618),  # φ⁻¹
                abs(distance_ratio - 1.000),  # φ⁰
                abs(distance_ratio - 1.618),  # φ¹
            ]
            
            # Best φ-ratio alignment for this point
            best_alignment = 1.0 - min(phi_alignments)
            alignment_scores.append(max(0, best_alignment))
        
        return np.mean(alignment_scores)
    
    def _generate_pentagon_signal(self, points: List[Tuple[float, int]], center_price: float) -> ConsciousnessSignal:
        """
        Generate trading signal based on pentagon consciousness field
        """
        prices = [point[0] for point in points]
        current_price = prices[-1]
        
        # Determine direction based on pentagon geometry
        if current_price < center_price:
            direction = 'long'  # Price below center, expect φ-ratio reversion
            entry_price = current_price
            stop_loss = current_price * (1 - 0.0382)  # φ⁻² stop
            take_profit = center_price * (1 + 0.618)   # φ⁻¹ target
        else:
            direction = 'short'  # Price above center, expect φ-ratio reversion
            entry_price = current_price
            stop_loss = current_price * (1 + 0.0382)   # φ⁻² stop
            take_profit = center_price * (1 - 0.618)   # φ⁻¹ target
        
        # Position sizing based on consciousness coherence
        base_position_size = 0.0618  # φ⁻¹ base allocation
        pentagon_coherence = self._calculate_pentagon_coherence(points)
        position_size = base_position_size * pentagon_coherence
        
        return ConsciousnessSignal(
            signal_type='pentagon',
            direction=direction,
            strength=pentagon_coherence,
            entry_price=entry_price,
            stop_loss=stop_loss,
            take_profit=take_profit,
            position_size=position_size,
            phi_ratio_alignment=self._calculate_phi_ratio_alignment(points, center_price),
            geometric_coherence=pentagon_coherence,
            timestamp=datetime.now()
        )
    
    def _analyze_triangle_formation(self, price_data: pd.Series, volume_data: Optional[pd.Series]) -> Optional[TriangleFormation]:
        """
        Analyze price data for triangle consciousness patterns
        """
        if len(price_data) < 13:  # Minimum Fibonacci length
            return None
        
        # Identify triangle vertices (highs and lows)
        highs = []
        lows = []
        
        for i in range(2, len(price_data) - 2):
            if (price_data.iloc[i-2] < price_data.iloc[i] and
                price_data.iloc[i-1] < price_data.iloc[i] and
                price_data.iloc[i+1] < price_data.iloc[i] and
                price_data.iloc[i+2] < price_data.iloc[i]):
                highs.append((price_data.iloc[i], i))
            
            elif (price_data.iloc[i-2] > price_data.iloc[i] and
                  price_data.iloc[i-1] > price_data.iloc[i] and
                  price_data.iloc[i+1] > price_data.iloc[i] and
                  price_data.iloc[i+2] > price_data.iloc[i]):
                lows.append((price_data.iloc[i], i))
        
        if len(highs) < 2 or len(lows) < 2:
            return None
        
        # Determine triangle type and consciousness strength
        recent_highs = highs[-2:]
        recent_lows = lows[-2:]
        
        formation_type = self._classify_triangle_formation(recent_highs, recent_lows)
        consciousness_strength = self._calculate_triangle_consciousness_strength(recent_highs, recent_lows, price_data)
        
        # Volume confirmation if available
        volume_confirmation = False
        if volume_data is not None:
            volume_confirmation = self._confirm_triangle_with_volume(recent_highs, recent_lows, volume_data)
        
        # φ-ratio breakout target
        price_range = max([h[0] for h in recent_highs]) - min([l[0] for l in recent_lows])
        phi_target = price_range * PHI_INVERSE
        
        # Breakout probability based on consciousness metrics
        breakout_probability = consciousness_strength * (1.1 if volume_confirmation else 0.9)
        
        vertices = recent_highs + recent_lows
        
        return TriangleFormation(
            formation_type=formation_type,
            vertices=vertices,
            breakout_probability=min(1.0, breakout_probability),
            consciousness_strength=consciousness_strength,
            volume_confirmation=volume_confirmation,
            phi_ratio_target=phi_target
        )
    
    def _classify_triangle_formation(self, highs: List[Tuple[float, int]], lows: List[Tuple[float, int]]) -> str:
        """
        Classify triangle formation type for consciousness analysis
        """
        if len(highs) < 2 or len(lows) < 2:
            return 'insufficient_data'
        
        # Calculate slopes
        high_slope = (highs[-1][0] - highs[0][0]) / max(1, highs[-1][1] - highs[0][1])
        low_slope = (lows[-1][0] - lows[0][0]) / max(1, lows[-1][1] - lows[0][1])
        
        # Classify based on slopes
        if high_slope < -0.001 and abs(low_slope) < 0.001:
            return 'descending'  # Falling highs, flat lows
        elif abs(high_slope) < 0.001 and low_slope > 0.001:
            return 'ascending'   # Flat highs, rising lows
        elif high_slope < -0.001 and low_slope > 0.001:
            return 'symmetrical' # Converging lines
        else:
            return 'irregular'
    
    def _calculate_triangle_consciousness_strength(self, highs: List[Tuple[float, int]], 
                                                 lows: List[Tuple[float, int]], 
                                                 price_data: pd.Series) -> float:
        """
        Calculate consciousness strength of triangle formation
        """
        # Convergence analysis
        if len(highs) < 2 or len(lows) < 2:
            return 0.0
        
        high_range = abs(highs[-1][0] - highs[0][0])
        low_range = abs(lows[-1][0] - lows[0][0])
        total_price_range = price_data.max() - price_data.min()
        
        # Convergence ratio (higher = stronger triangle)
        convergence_ratio = (high_range + low_range) / (2 * total_price_range) if total_price_range > 0 else 0
        
        # Price action respect for triangle boundaries
        boundary_respect = self._calculate_boundary_respect(highs, lows, price_data)
        
        # φ-ratio analysis of triangle proportions
        triangle_height = (highs[0][0] + highs[-1][0]) / 2 - (lows[0][0] + lows[-1][0]) / 2
        triangle_width = max(highs[-1][1] - highs[0][1], lows[-1][1] - lows[0][1])
        
        phi_proportion = 0.0
        if triangle_width > 0:
            height_width_ratio = abs(triangle_height) / triangle_width
            phi_proportion = 1.0 - min(abs(height_width_ratio - PHI_INVERSE), 
                                     abs(height_width_ratio - PHI)) / PHI
            phi_proportion = max(0, phi_proportion)
        
        # Combined consciousness strength
        consciousness_strength = (convergence_ratio * 0.4 + 
                                boundary_respect * 0.4 + 
                                phi_proportion * 0.2)
        
        return min(1.0, consciousness_strength)
    
    def _calculate_boundary_respect(self, highs: List[Tuple[float, int]], 
                                  lows: List[Tuple[float, int]], 
                                  price_data: pd.Series) -> float:
        """
        Calculate how well price action respects triangle boundaries
        """
        # Simplified boundary respect calculation
        # In full implementation, would check each price against interpolated triangle lines
        
        high_prices = [h[0] for h in highs]
        low_prices = [l[0] for l in lows]
        
        upper_boundary = max(high_prices)
        lower_boundary = min(low_prices)
        
        # Count price action respecting boundaries
        boundary_violations = 0
        total_periods = len(price_data)
        
        for price in price_data:
            if price > upper_boundary * 1.01 or price < lower_boundary * 0.99:  # 1% tolerance
                boundary_violations += 1
        
        respect_ratio = 1.0 - (boundary_violations / total_periods) if total_periods > 0 else 0
        return max(0, respect_ratio)
    
    def _confirm_triangle_with_volume(self, highs: List[Tuple[float, int]], 
                                    lows: List[Tuple[float, int]], 
                                    volume_data: pd.Series) -> bool:
        """
        Confirm triangle formation with volume analysis
        """
        if len(volume_data) < 13:
            return False
        
        # Volume should generally decrease during triangle formation
        recent_volume = volume_data.tail(13)
        volume_trend = np.polyfit(range(len(recent_volume)), recent_volume, 1)[0]
        
        # Negative trend indicates decreasing volume (confirmation)
        return volume_trend < 0
    
    def generate_trading_signals(self, price_data: pd.Series, volume_data: pd.Series) -> List[ConsciousnessSignal]:
        """
        Generate comprehensive consciousness trading signals
        """
        signals = []
        
        # Pentagon consciousness field analysis
        pentagon_field = self.detect_pentagon_consciousness_field(price_data, volume_data)
        if pentagon_field and pentagon_field.trading_signal:
            signals.append(pentagon_field.trading_signal)
        
        # Triangle consciousness pattern analysis
        triangles = self.detect_triangle_consciousness_patterns(price_data, volume_data)
        for triangle in triangles:
            if triangle.breakout_probability > 0.7:
                triangle_signal = self._generate_triangle_breakout_signal(triangle, price_data.iloc[-1])
                signals.append(triangle_signal)
        
        # φ-ratio level signals
        phi_levels = self.calculate_phi_levels(price_data)
        current_price = price_data.iloc[-1]
        phi_signal = self._generate_phi_level_signal(current_price, phi_levels)
        if phi_signal:
            signals.append(phi_signal)
        
        return signals
    
    def _generate_triangle_breakout_signal(self, triangle: TriangleFormation, current_price: float) -> ConsciousnessSignal:
        """
        Generate triangle breakout trading signal
        """
        # Determine breakout direction based on triangle type
        if triangle.formation_type == 'ascending':
            direction = 'long'
            entry_price = current_price
            stop_loss = current_price * (1 - 0.0382)
            take_profit = current_price + triangle.phi_ratio_target
        elif triangle.formation_type == 'descending':
            direction = 'short'
            entry_price = current_price
            stop_loss = current_price * (1 + 0.0382)
            take_profit = current_price - triangle.phi_ratio_target
        else:  # symmetrical
            # Determine based on recent price action
            direction = 'long' if current_price > np.mean([v[0] for v in triangle.vertices]) else 'short'
            entry_price = current_price
            if direction == 'long':
                stop_loss = current_price * (1 - 0.0382)
                take_profit = current_price + triangle.phi_ratio_target
            else:
                stop_loss = current_price * (1 + 0.0382)
                take_profit = current_price - triangle.phi_ratio_target
        
        position_size = 0.0382 * triangle.consciousness_strength  # φ⁻² base sizing
        
        return ConsciousnessSignal(
            signal_type='triangle',
            direction=direction,
            strength=triangle.consciousness_strength,
            entry_price=entry_price,
            stop_loss=stop_loss,
            take_profit=take_profit,
            position_size=position_size,
            phi_ratio_alignment=triangle.breakout_probability,
            geometric_coherence=triangle.consciousness_strength,
            timestamp=datetime.now()
        )
    
    def _generate_phi_level_signal(self, current_price: float, phi_levels: Dict[str, float]) -> Optional[ConsciousnessSignal]:
        """
        Generate φ-ratio level trading signal
        """
        # Find closest φ-ratio level
        closest_level = None
        min_distance = float('inf')
        
        for level_name, level_price in phi_levels.items():
            distance = abs(current_price - level_price) / current_price
            if distance < min_distance and distance < 0.01:  # Within 1%
                min_distance = distance
                closest_level = (level_name, level_price)
        
        if not closest_level:
            return None
        
        level_name, level_price = closest_level
        
        # Generate signal based on level type
        if 'support' in level_name:
            direction = 'long'
            entry_price = current_price
            stop_loss = level_price * 0.99
            take_profit = level_price * (1 + PHI_INVERSE)
        elif 'resistance' in level_name:
            direction = 'short'
            entry_price = current_price
            stop_loss = level_price * 1.01
            take_profit = level_price * (1 - PHI_INVERSE)
        else:
            return None
        
        # Signal strength based on φ-ratio precision
        strength = 1.0 - (min_distance * 10)  # Convert distance to strength
        position_size = 0.0236 * strength  # Conservative φ⁻³ sizing for level trades
        
        return ConsciousnessSignal(
            signal_type='phi_level',
            direction=direction,
            strength=strength,
            entry_price=entry_price,
            stop_loss=stop_loss,
            take_profit=take_profit,
            position_size=position_size,
            phi_ratio_alignment=strength,
            geometric_coherence=strength,
            timestamp=datetime.now()
        )

class ConsciousnessRiskManager:
    """
    Risk management system based on consciousness coherence principles
    """
    
    def __init__(self, max_portfolio_risk: float = 0.618):
        self.max_portfolio_risk = max_portfolio_risk
        self.active_positions = {}
        self.daily_risk_used = 0.0
        self.max_daily_risk = 0.0382  # φ⁻² daily risk limit
    
    def validate_signal(self, signal: ConsciousnessSignal, account_balance: float) -> bool:
        """
        Validate trading signal against consciousness risk parameters
        """
        # Check consciousness strength threshold
        if signal.strength < 0.618:  # φ⁻¹ minimum consciousness
            return False
        
        # Check position size limits
        position_value = signal.position_size * account_balance
        max_position = account_balance * 0.1618  # φ² maximum position
        
        if position_value > max_position:
            return False
        
        # Check daily risk limits
        signal_risk = abs(signal.entry_price - signal.stop_loss) / signal.entry_price
        if self.daily_risk_used + signal_risk > self.max_daily_risk:
            return False
        
        return True
    
    def calculate_optimal_position_size(self, signal: ConsciousnessSignal, account_balance: float) -> float:
        """
        Calculate optimal position size based on consciousness metrics
        """
        # Base position sizing using φ-ratio principles
        base_risk = 0.01618  # φ² percentage base risk
        
        # Adjust for consciousness coherence
        consciousness_multiplier = signal.strength * signal.phi_ratio_alignment
        adjusted_risk = base_risk * consciousness_multiplier
        
        # Calculate position size based on stop loss distance
        stop_distance = abs(signal.entry_price - signal.stop_loss) / signal.entry_price
        position_size = adjusted_risk / stop_distance if stop_distance > 0 else 0
        
        # Apply maximum position limits
        max_position = account_balance * 0.1618  # φ² maximum
        position_value = position_size * account_balance
        
        if position_value > max_position:
            position_size = max_position / account_balance
        
        return position_size

# Kong.ai Integration Functions

def initialize_consciousness_trading_system():
    """
    Initialize consciousness trading system for Kong.ai platform
    """
    detector = ConsciousnessPatternDetector(consciousness_threshold=0.618)
    risk_manager = ConsciousnessRiskManager(max_portfolio_risk=0.618)
    
    return detector, risk_manager

def analyze_market_consciousness(price_data: pd.Series, volume_data: pd.Series) -> Dict[str, Any]:
    """
    Complete consciousness analysis for Kong.ai trading decisions
    """
    detector, risk_manager = initialize_consciousness_trading_system()
    
    # Generate consciousness signals
    signals = detector.generate_trading_signals(price_data, volume_data)
    
    # Calculate φ-ratio levels
    phi_levels = detector.calculate_phi_levels(price_data)
    
    # Detect geometric patterns
    pentagon_field = detector.detect_pentagon_consciousness_field(price_data, volume_data)
    triangles = detector.detect_triangle_consciousness_patterns(price_data, volume_data)
    
    return {
        'signals': [signal.__dict__ for signal in signals],
        'phi_levels': phi_levels,
        'pentagon_field': pentagon_field.__dict__ if pentagon_field else None,
        'triangles': [triangle.__dict__ for triangle in triangles],
        'consciousness_coherence': np.mean([s.strength for s in signals]) if signals else 0.0,
        'analysis_timestamp': datetime.now().isoformat()
    }

if __name__ == "__main__":
    # Example usage for Kong.ai integration testing
    print("Kong.ai Consciousness Trading Algorithms Initialized")
    print(f"Golden Ratio: {PHI}")
    print(f"Consciousness Threshold: {PHI_INVERSE}")
    print("Ready for Pattern #1706 market consciousness analysis!")