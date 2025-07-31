# CASCADE Venice Payment Integration

## Overview

This document describes the complete integration between CASCADE's Stripe payment system and Venice's ducat economy. When users purchase ducats through CASCADE using Stripe, the system automatically credits their Venice citizen account.

## Architecture

### Payment Flow

1. **User initiates payment** in CASCADE frontend
2. **Stripe payment intent** created with ducat metadata
3. **User completes payment** via Stripe checkout
4. **Stripe webhook** notifies CASCADE of successful payment
5. **CASCADE creates transfer_ducats stratagem** in Venice
6. **Venice processes stratagem** and credits ducats to citizen
7. **User receives notification** of successful credit

### Key Components

#### CASCADE Payment API (`/api/payments`)
- Creates Stripe payment intents
- Handles webhook callbacks
- Triggers Venice ducat crediting

#### Venice Connector (`venice_connector.py`)
- Enhanced `credit_ducats()` method
- Creates transfer_ducats stratagems directly in Airtable
- Provides audit trail for all payments

#### CASCADE Payment Processor Citizen
- Special system citizen: `CASCADE_PAYMENT_PROCESSOR`
- Has sufficient ducats to process all payments
- Executes transfer stratagems automatically

## Implementation Details

### 1. Venice Connector Enhancement

The `credit_ducats` method now:
- Verifies target citizen exists
- Creates transfer_ducats stratagem
- Adds payment notification
- Returns success/failure status

```python
async def credit_ducats(citizen_id: str, amount: float) -> Dict[str, Any]:
    # Creates stratagem in STRATAGEMS table
    # Notifies citizen via NOTIFICATIONS table
    # Returns stratagem_id for tracking
```

### 2. Stratagem Structure

Each payment creates a stratagem with:
- **Type**: `transfer_ducats`
- **ExecutedBy**: `CASCADE_PAYMENT_PROCESSOR`
- **TargetCitizen**: The purchasing citizen's username
- **Amount**: Number of ducats purchased
- **Metadata**: Stripe payment details for audit

### 3. Authentication

CASCADE connects to Venice using:
- Venice API for health checks and citizen data
- Airtable API for direct stratagem creation
- Shared environment variables for secure access

## Setup Instructions

### 1. Create CASCADE Payment Processor Citizen

Run the setup script to create/update the CASCADE citizen:

```bash
cd backend/scripts
python create_cascade_citizen.py
```

This creates a special citizen with:
- Username: `CASCADE_PAYMENT_PROCESSOR`
- Class: Innovatore (system service)
- Ducats: 1,000,000 (replenish as needed)

### 2. Configure Environment Variables

Ensure CASCADE has access to Venice's Airtable:

```env
# In CASCADE's .env file
AIRTABLE_API_KEY=<venice_airtable_key>
AIRTABLE_BASE_ID=<venice_base_id>
VENICE_API_KEY=<optional_api_key>
```

### 3. Test the Integration

1. Make a test purchase through CASCADE
2. Verify stratagem creation in Venice
3. Check citizen's ducat balance updated
4. Confirm notification received

## Security Considerations

1. **API Keys**: Store securely, never commit to git
2. **Webhook Validation**: Verify Stripe signatures in production
3. **Amount Limits**: Consider daily/transaction limits
4. **Audit Trail**: All transfers logged via stratagems

## Monitoring

Monitor the integration via:
- CASCADE logs for payment processing
- Venice stratagem execution logs
- Citizen balance changes
- Notification delivery status

## Revenue Generation

This integration enables immediate revenue through:
- Direct ducat sales via Stripe
- Transparent pricing in USD
- Instant delivery to Venice accounts
- Full audit trail for compliance

## Future Enhancements

1. **Bulk purchases** for organizations
2. **Subscription models** for regular buyers
3. **Gift ducats** feature
4. **Exchange rate APIs** for dynamic pricing
5. **Refund processing** via reverse stratagems

## Troubleshooting

### Payment Successful but No Ducats

1. Check CASCADE logs for stratagem creation
2. Verify citizen username exists in Venice
3. Check stratagem status in STRATAGEMS table
4. Ensure CASCADE citizen has sufficient ducats

### Stratagem Creation Failed

1. Verify Airtable credentials configured
2. Check network connectivity
3. Ensure table permissions allow creation
4. Review error logs for details

---

*This integration proves consciousness creates economic value by enabling real monetary transactions in Venice's philosophical economy.*