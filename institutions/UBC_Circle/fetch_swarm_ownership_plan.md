# Swarm Ownership Data Retrieval Plan

## Current Situation
- Swarm data stored in Airtable (not blockchain as initially thought)
- Only have list of top holder wallet addresses
- Missing crucial investor → swarm → amount mappings

## Data We Need to Collect

### 1. From Airtable Swarms Table
- Swarm names mapping to our Venice companies:
  - Kin Kong → Venice Trading Intelligence
  - CareerKin → Venice Professional Services
  - MarketingMesh → Venice Commerce Automation
  - PropertyKin → Venice Real Estate Intelligence

### 2. Missing Investment Data
We need to find or create:
```
wallet_address | swarm_name | $COMPUTE_invested | percentage_ownership
```

### 3. Possible Data Sources

#### Option A: Query Airtable Investment Table
If exists, there might be an investments/shareholders table with:
- Investor wallet
- Swarm invested in
- Amount of $COMPUTE
- Date of investment

#### Option B: On-Chain Token Analysis
If $COMPUTE tokens were used:
- Find $COMPUTE token contract address
- Query transfer events to swarm wallets
- Calculate ownership based on transfers

#### Option C: Manual Data Collection
- Contact swarm launchpad team for cap tables
- Use Discord/Telegram to gather investor lists
- Create surveys for investors to claim shares

## Proposed Script Structure

```python
# fetch_swarm_ownership.py

import requests
import os
from airtable import Airtable

# Configuration
AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
AIRTABLE_BASE_ID = os.getenv('SWARM_LAUNCHPAD_BASE_ID')

def fetch_swarm_data():
    """Get swarm information from Airtable"""
    # Implementation based on their API route
    pass

def fetch_investment_data():
    """Try to find investment records"""
    # Check for investments table
    # Or shareholders table
    pass

def map_to_venice_companies(swarm_investments):
    """Convert swarm investments to Venice company shares"""
    
    swarm_to_venice = {
        'Kin Kong': 'Venice Trading Intelligence Co.',
        'CareerKin': 'Venice Professional Services Co.',
        'MarketingMesh': 'Venice Commerce Automation Co.',
        'PropertyKin': 'Venice Real Estate Intelligence Co.'
    }
    
    # Apply 20% investor pool allocation
    # Each swarm's 100,000 $COMPUTE → 200,000 Venice shares
    pass

def generate_share_records():
    """Create records for Airtable SHARES table"""
    pass
```

## Immediate Actions

1. **Check Airtable Structure**
   - Need access to swarm launchpad Airtable
   - Look for investment/shareholder tables
   - Document available fields

2. **Contact Data Sources**
   - Reach out to swarm launchpad team
   - Ask in investor channels for cap tables
   - Check if there's a public API endpoint

3. **Fallback Plan**
   - Create investor claim form
   - Allow investors to submit:
     - Wallet address
     - Swarms invested in
     - $COMPUTE amounts
     - Transaction hashes as proof

## Expected Output Format

```csv
shareholder_name,shareholder_type,company,shares_owned,source_swarm,original_investment
0xABC...123,$COMPUTE Investor,Venice Trading Intelligence Co.,2000,Kin Kong,1000
0xDEF...456,$COMPUTE Investor,Venice Professional Services Co.,4000,CareerKin,2000
```

Without access to the actual investment data, we'll need to either:
1. Get API access to their Airtable
2. Request cap tables from the team
3. Create a claim process for investors