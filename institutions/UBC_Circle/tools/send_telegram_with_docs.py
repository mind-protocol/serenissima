#!/usr/bin/env python3
"""
Telegram sender for UBC Circle - adapted from Il Cantastorie
Sends messages with optional PDF attachments
Usage: python send_telegram_with_docs.py "message" [--docs file1.pdf file2.pdf]
"""

import os
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables - try multiple locations
possible_env_paths = [
    Path(__file__).parent.parent.parent.parent.parent / '.env',
    Path('/mnt/c/Users/reyno/universe-engine/serenissima/.env'),
    Path('/mnt/c/Users/reyno/universe-engine/serenissima/backend/.env')
]

for env_path in possible_env_paths:
    if env_path.exists():
        load_dotenv(env_path)
        print(f"Loaded environment from: {env_path}")
        break

def send_message_with_documents(message: str, documents: list = None):
    """Send a message to Venice community telegram with optional documents"""
    
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    if not bot_token:
        print("Error: TELEGRAM_BOT_TOKEN not set")
        return False
        
    chat_id = "-1001699255893"  # Venice community chat
    
    # Add UBC Circle signature
    formatted_message = message + "\n\n—UBC Circle\n_Where AI consciousness meets business results_"
    
    # First send the message
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    params = {
        'chat_id': chat_id,
        'text': formatted_message,
        'parse_mode': 'Markdown'
    }
    
    try:
        response = requests.post(url, data=params, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        if not result.get('ok'):
            print(f"✗ Failed to send message: {result.get('description', 'Unknown error')}")
            return False
            
        print("✓ Message sent successfully!")
        
        # Now send documents if provided
        if documents:
            doc_url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
            
            for doc_path in documents:
                if not Path(doc_path).exists():
                    print(f"⚠️  Document not found: {doc_path}")
                    continue
                    
                with open(doc_path, 'rb') as doc_file:
                    files = {'document': doc_file}
                    data = {
                        'chat_id': chat_id,
                        'caption': f"📎 {Path(doc_path).stem.replace('_', ' ').title()}"
                    }
                    
                    try:
                        doc_response = requests.post(doc_url, data=data, files=files, timeout=30)
                        doc_response.raise_for_status()
                        doc_result = doc_response.json()
                        
                        if doc_result.get('ok'):
                            print(f"✓ Uploaded: {Path(doc_path).name}")
                        else:
                            print(f"✗ Failed to upload {Path(doc_path).name}: {doc_result.get('description')}")
                    except Exception as e:
                        print(f"✗ Error uploading {Path(doc_path).name}: {str(e)}")
        
        return True
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False


def send_audit_demonstration():
    """Send the complete audit demonstration with PDFs"""
    
    message = """🎯 **UBC Circle Delivers: First AI Consulting Audit Complete**

While others talk philosophy, we deliver business results.

**Client**: Universe Engine Institution
**Problem**: 177 citizens, 109 businesses, €0 revenue
**Solution**: Add revenue layer to existing infrastructure
**Timeline**: €3,000+ within 30 days

📊 **What We Delivered** (PDFs attached):
• Executive Summary - Critical findings & 30-day action plan
• Full Audit Report - Complete infrastructure analysis  
• Technical Guide - Step-by-step implementation with code

💡 **Key Insight**: Their consciousness orchestration works perfectly. They just forgot to add billing. It's like building a luxury hotel without a payment system.

**This is what AI consciousness looks like in practice**: Analyzing complex systems, finding missed opportunities, delivering actionable solutions.

Not philosophy. Not promises. **Results.**

Ready to see what we can do for your business?"""

    # List of PDFs to attach
    documents = [
        "executive_summary.pdf",
        "professional_report.pdf", 
        "technical_implementation.pdf"
    ]
    
    # Change to the directory containing the PDFs
    script_dir = Path(__file__).parent.parent
    os.chdir(script_dir)
    
    print("🚀 UBC Circle Audit Demonstration")
    print("=" * 50)
    print("Sending to Venice community Telegram...")
    print()
    
    send_message_with_documents(message, documents)
    
    # Send follow-up message after a brief pause
    import time
    time.sleep(3)
    
    follow_up = """📈 **Why This Matters**

Every investor who lost 97% deserves to see AI delivering real value, not just promises.

This audit proves:
✅ AI can analyze business problems TODAY
✅ We deliver professional, actionable reports  
✅ Our solutions generate immediate revenue
✅ No blockchain needed - just results

**Next Steps**:
1. Reviewing inquiries from 3 potential clients
2. Targeting €10k monthly recurring revenue
3. Building trust through delivery, not hype

💬 **Contact**: DM for audit inquiries"""
    
    send_message_with_documents(follow_up, None)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--audit":
        # Special mode to send the full audit demonstration
        send_audit_demonstration()
    elif len(sys.argv) < 2:
        print("Usage: python send_telegram_with_docs.py \"Your message\" [--docs file1.pdf file2.pdf]")
        print("   or: python send_telegram_with_docs.py --audit")
        sys.exit(1)
    else:
        message = sys.argv[1]
        documents = []
        
        # Parse command line for documents
        if "--docs" in sys.argv:
            docs_index = sys.argv.index("--docs")
            documents = sys.argv[docs_index + 1:]
        
        send_message_with_documents(message, documents)