#!/bin/bash

# Send PDF documents to nlr@universe-engine.ai

echo "UBC Circle PDF Document Sender"
echo "=============================="
echo ""
echo "This script will send all PDF documents in this directory to nlr@universe-engine.ai"
echo ""
echo "Choose authentication method:"
echo "1) Interactive (enter credentials when prompted)"
echo "2) Config file/Environment variables"
echo ""
read -p "Select option (1 or 2): " choice

case $choice in
    1)
        echo "Running interactive version..."
        python3 send_pdf_documents.py
        ;;
    2)
        echo "Running config/env version..."
        python3 send_pdf_documents_oauth.py
        ;;
    *)
        echo "Invalid option. Please run the script again and select 1 or 2."
        exit 1
        ;;
esac