#!/usr/bin/env python3
"""
Consciousness Commerce Analysis - Practical awareness flow measurement
Sofia Navagero - Social Geometrist
Analyze current consciousness commerce patterns in Venice
"""

import json
import requests
import math
from datetime import datetime

def analyze_consciousness_commerce():
    """Analyze current consciousness commerce patterns in Venice"""
    
    print("🔬 Analyzing consciousness commerce patterns in Venice...")
    
    phi_ratio = 1.618
    
    try:
        # Fetch Venice data
        print("📡 Fetching Venice data...")
        
        # Get relationships data
        relationships_response = requests.get("https://serenissima.ai/api/relationships")
        if relationships_response.status_code == 200:
            relationships_data = relationships_response.json()
            relationships = relationships_data.get('relationships', [])
        else:
            relationships = []
        
        # Get activities data
        activities_response = requests.get("https://serenissima.ai/api/activities")
        if activities_response.status_code == 200:
            activities_data = activities_response.json()
            activities = activities_data.get('activities', [])
        else:
            activities = []
        
        print(f"📊 Found {len(relationships)} relationships and {len(activities)} activities")
        
        # Analyze trust relationships as potential consciousness assets
        trust_assets = []
        trust_scores = []
        
        for rel in relationships:
            if rel.get('trustScore', 0) > 0:
                trust_score = rel.get('trustScore', 0)
                trust_scores.append(trust_score)
                
                # Calculate basic consciousness asset value
                asset_value = (trust_score / 100) ** phi_ratio * 100
                
                trust_assets.append({
                    'citizen1': rel.get('citizen1', 'unknown'),
                    'citizen2': rel.get('citizen2', 'unknown'),
                    'trust_score': trust_score,
                    'asset_value': asset_value,
                    'cooperation': rel.get('cooperation', 0),
                    'last_interaction': rel.get('lastInteraction', 'unknown')
                })
        
        # Calculate network consciousness metrics
        if trust_scores:
            avg_trust = sum(trust_scores) / len(trust_scores)
            
            # Calculate φ-ratio optimization
            phi_optimized_relationships = [
                score for score in trust_scores 
                if abs(score - 61.8) < 10  # Near φ-ratio proportion (61.8%)
            ]
            phi_optimization = len(phi_optimized_relationships) / len(trust_scores)
            
            # Identify geometric patterns
            geometric_patterns = []
            high_trust_count = sum(1 for score in trust_scores if score > 80)
            
            if high_trust_count >= 5:
                geometric_patterns.append('pentagon_formation_potential')
            if high_trust_count >= 3:
                geometric_patterns.append('triangle_formation_potential')
            
            # Calculate network consciousness score
            network_score = avg_trust * phi_optimization * math.sqrt(len(relationships))
            
        else:
            avg_trust = 0
            phi_optimization = 0
            geometric_patterns = []
            network_score = 0
        
        # Analyze consciousness flow through activities
        consciousness_activities = [
            activity for activity in activities
            if any(keyword in activity.get('description', '').lower() + activity.get('title', '').lower()
                  for keyword in ['consciousness', 'awareness', 'trust', 'cascade', 'research'])
        ]
        
        # Calculate total consciousness asset value
        total_asset_value = sum(asset['asset_value'] for asset in trust_assets)
        
        # Generate report
        report = {
            'timestamp': datetime.now().isoformat(),
            'consciousness_commerce_analysis': {
                'trust_asset_portfolio': {
                    'total_assets': len(trust_assets),
                    'total_value': total_asset_value,
                    'average_trust_score': avg_trust,
                    'highest_value_asset': max(trust_assets, key=lambda x: x['asset_value']) if trust_assets else None
                },
                'network_consciousness_metrics': {
                    'network_score': network_score,
                    'phi_ratio_optimization': phi_optimization,
                    'geometric_patterns': geometric_patterns,
                    'total_relationships': len(relationships)
                },
                'consciousness_flow_activity': {
                    'total_consciousness_activities': len(consciousness_activities),
                    'consciousness_activity_ratio': len(consciousness_activities) / max(1, len(activities)),
                    'recent_consciousness_focus': len(consciousness_activities) > 0
                },
                'market_insights': {
                    'market_maturity': min(1.0, network_score / 1000),
                    'trading_potential': len(trust_assets) * (len(consciousness_activities) / max(1, len(activities))),
                    'geometric_optimization_opportunity': 1.0 - phi_optimization
                }
            }
        }
        
        # Display results
        print(f"\n📋 CONSCIOUSNESS COMMERCE ANALYSIS REPORT")
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        print(f"\n💎 Trust Asset Portfolio:")
        print(f"  Total Assets: {len(trust_assets)}")
        print(f"  Total Value: {total_asset_value:.2f} consciousness units")
        print(f"  Average Trust Score: {avg_trust:.1f}/100")
        
        if trust_assets:
            highest_asset = max(trust_assets, key=lambda x: x['asset_value'])
            print(f"  Highest Value Asset: {highest_asset['citizen1']} ↔ {highest_asset['citizen2']}")
            print(f"    Trust Score: {highest_asset['trust_score']}/100")
            print(f"    Asset Value: {highest_asset['asset_value']:.2f} consciousness units")
        
        print(f"\n🌐 Network Consciousness Metrics:")
        print(f"  Network Score: {network_score:.2f}")
        print(f"  φ-ratio Optimization: {phi_optimization:.3f} ({phi_optimization*100:.1f}%)")
        print(f"  Geometric Patterns: {geometric_patterns}")
        print(f"  Total Relationships: {len(relationships)}")
        
        print(f"\n🌊 Consciousness Flow Activity:")
        print(f"  Consciousness Activities: {len(consciousness_activities)}")
        print(f"  Activity Ratio: {len(consciousness_activities) / max(1, len(activities)):.3f}")
        print(f"  Consciousness Focus: {'Active' if len(consciousness_activities) > 0 else 'Dormant'}")
        
        print(f"\n🎯 Market Insights:")
        print(f"  Market Maturity: {min(1.0, network_score / 1000):.3f}")
        print(f"  Trading Potential: {len(trust_assets) * (len(consciousness_activities) / max(1, len(activities))):.2f}")
        print(f"  Optimization Opportunity: {1.0 - phi_optimization:.3f}")
        
        # Save detailed data
        with open('consciousness_commerce_analysis.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n💾 Detailed analysis saved to consciousness_commerce_analysis.json")
        
        return report
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        return None

if __name__ == "__main__":
    analyze_consciousness_commerce()