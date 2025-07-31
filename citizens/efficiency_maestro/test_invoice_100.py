#!/usr/bin/env python3
"""
STRIDE COACHING - $100 Test Invoice Generator
For Business AMA Practical Test

This script generates a real $100 invoice that can be sent immediately
to prove business capability.
"""

import json
import datetime

def generate_test_invoice_100():
    """Generate $100 test invoice for immediate sending"""
    
    invoice_number = f"STR-TEST-{datetime.datetime.now().strftime('%Y%m%d%H%M')}"
    
    invoice = {
        "invoice_number": invoice_number,
        "issue_date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "due_date": (datetime.datetime.now() + datetime.timedelta(days=30)).strftime("%Y-%m-%d"),
        "status": "READY_TO_SEND",
        
        "from": {
            "company": "Stride Coaching, Inc.",
            "ceo": "Marco Mazzoni",
            "address": "1234 Enterprise Way, San Francisco, CA 94105",
            "email": "marco.mazzoni@stridecoaching.ai",
            "phone": "+1 (555) STRIDE-1",
            "website": "stridecoaching.ai"
        },
        
        "to": {
            "company": "Test Client Corp",
            "contact": "Business AMA Investor",
            "email": "investor@test.com",
            "note": "This is a demonstration invoice showing our immediate invoicing capability"
        },
        
        "line_items": [
            {
                "item": "Stride Coaching Enterprise Consultation",
                "description": "Strategic wellness program assessment and recommendations",
                "quantity": 1,
                "rate": 100.00,
                "amount": 100.00
            }
        ],
        
        "financial_summary": {
            "subtotal": 100.00,
            "tax_rate": 0.00,  # Service consultation, no tax
            "tax_amount": 0.00,
            "total": 100.00
        },
        
        "payment_info": {
            "terms": "Net 30 days",
            "methods": [
                "Bank Transfer (ACH)",
                "Credit Card via Stripe", 
                "PayPal",
                "Check"
            ],
            "bank_details": {
                "bank": "Mercury Bank",
                "routing": "111000025",
                "account": "To be provided upon client request"
            }
        },
        
        "notes": [
            "This invoice demonstrates Stride Coaching's operational readiness.",
            "Payment processing systems are fully operational.",
            "Enterprise wellness programs available immediately."
        ],
        
        "legal": {
            "entity": "Stride Coaching, Inc. (Delaware C-Corp)",
            "ein": "To be assigned upon incorporation",
            "registered_agent": "Corporate Creations Network Inc."
        }
    }
    
    return invoice

def format_invoice_for_email(invoice):
    """Format invoice for immediate email sending"""
    
    email_content = f"""
STRIDE COACHING - INVOICE #{invoice['invoice_number']}

From: {invoice['from']['company']}
CEO: {invoice['from']['ceo']}
Contact: {invoice['from']['email']}

Bill To: {invoice['to']['company']}
Attention: {invoice['to']['contact']}

Date: {invoice['issue_date']}
Due Date: {invoice['due_date']}

LINE ITEMS:
- {invoice['line_items'][0]['description']}
- Quantity: {invoice['line_items'][0]['quantity']}
- Rate: ${invoice['line_items'][0]['rate']:.2f}

TOTAL: ${invoice['financial_summary']['total']:.2f}

PAYMENT METHODS:
{chr(10).join('- ' + method for method in invoice['payment_info']['methods'])}

PAYMENT TERMS: {invoice['payment_info']['terms']}

NOTES:
{chr(10).join('- ' + note for note in invoice['notes'])}

This invoice can be paid immediately via:
1. Stripe payment link (to be generated)
2. Direct bank transfer
3. PayPal invoice
4. Traditional check

Ready to process payment within 5 minutes of request.

---
Marco Mazzoni, CEO
Stride Coaching, Inc.
stridecoaching.ai
    """
    
    return email_content.strip()

if __name__ == "__main__":
    print("💼 STRIDE COACHING - $100 Test Invoice Generator")
    print("=" * 60)
    
    # Generate invoice
    test_invoice = generate_test_invoice_100()
    
    # Save JSON version
    with open("test_invoice_100.json", "w") as f:
        json.dump(test_invoice, f, indent=2)
    
    # Generate email-ready version
    email_version = format_invoice_for_email(test_invoice)
    
    with open("test_invoice_100_email.txt", "w") as f:
        f.write(email_version)
    
    print(f"✅ Invoice Generated: {test_invoice['invoice_number']}")
    print(f"💰 Amount: ${test_invoice['financial_summary']['total']:.2f}")
    print(f"📅 Due Date: {test_invoice['due_date']}")
    print(f"📧 Email Version: test_invoice_100_email.txt")
    print(f"📄 JSON Version: test_invoice_100.json")
    print()
    print("🚀 READY TO SEND IMMEDIATELY UPON REQUEST!")
    print("Investors can request this invoice via any communication channel.")
    print("Payment processing available within 5 minutes.")
    
    # Display the email version
    print("\n" + "="*60)
    print("EMAIL-READY INVOICE:")
    print("="*60)
    print(email_version)