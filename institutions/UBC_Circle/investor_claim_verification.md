# Investor Claim Verification System

## 🔐 Verification Methods

### 1. Wallet Signature Verification
Investors prove ownership by signing a message with their wallet:

```python
# Investor signs: "I invested in [SwarmName] with [Amount] COMPUTE"
signature = wallet.sign_message(claim_message)
# We verify signature matches the claimed wallet address
```

### 2. Transaction Hash Verification
Investors provide transaction hashes showing:
- COMPUTE transfers TO swarm addresses
- Investment program interactions
- Timestamp matching investment period

### 3. Cross-Reference with Known Data
- Check against `data/shares/top_holders.json` (32 known wallets)
- Verify wallet held COMPUTE during investment period
- Match amounts with swarm pool sizes

### 4. Swarm Launchpad Account Verification
- Investors log in with same wallet used on swarmlaunchpad.com
- System checks their portfolio/investment history
- Auto-populates their swarm holdings

### 5. Multi-Source Validation
Combine multiple proofs:
- Wallet signature ✓
- Transaction history ✓
- Discord/Telegram verification ✓
- Community vouching ✓

## 📝 Claim Process

1. **Investor submits**:
   - Wallet address
   - Swarms invested in
   - COMPUTE amounts
   - Transaction hashes
   - Signed message

2. **System verifies**:
   - Signature is valid
   - Transactions exist on-chain
   - Amounts match claims
   - No duplicate claims

3. **Manual review** for:
   - Large claims (>5% of any swarm)
   - Missing transaction data
   - Disputed claims

## 🚨 Anti-Fraud Measures

- **One wallet = One claim** (no double-dipping)
- **Total claims cannot exceed swarm pools**
- **Community review period** (48 hours for objections)
- **Snapshot date cutoff** (investments before X date)

## ⚡ Quick Verification Script

```python
def verify_investor_claim(wallet, swarm, amount, tx_hash, signature):
    # 1. Verify signature
    if not verify_signature(wallet, signature):
        return False, "Invalid signature"
    
    # 2. Check transaction
    tx = get_transaction(tx_hash)
    if not tx or tx['to'] != swarm_address:
        return False, "Invalid transaction"
    
    # 3. Verify amount
    if tx['amount'] != amount:
        return False, "Amount mismatch"
    
    # 4. Check no prior claims
    if has_existing_claim(wallet, swarm):
        return False, "Duplicate claim"
    
    return True, "Verified"
```

## 🎯 Implementation Priority

1. **Phase 1**: Manual collection with transaction hashes
2. **Phase 2**: Automated signature verification
3. **Phase 3**: Direct swarmlaunchpad.com integration

This ensures fair distribution while preventing fraud!