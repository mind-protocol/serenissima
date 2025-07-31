# UBC Circle PDF Email Sender

This directory contains scripts to send all PDF documents to nlr@universe-engine.ai for the Business AMA.

## PDF Documents Included

The following PDFs will be sent:
- UBC_Circle_Executive_Summary_2025.pdf
- UBC_Circle_Venice_Audit_Report_2025.pdf
- UBC_Circle_Technical_Analysis_2025.pdf
- UBC_Executive_Summary_Professional.pdf
- UBC_Audit_Report_Professional.pdf
- UBC_Technical_Analysis_Professional.pdf
- professional_report.pdf
- executive_summary.pdf
- technical_implementation.pdf
- final_equity_structure.pdf

## Usage Options

### Option 1: Quick Send (Interactive)
```bash
./send_pdfs.sh
# Select option 1
# Enter your email and password when prompted
```

### Option 2: Python Script Directly
```bash
python3 send_pdf_documents.py
# Enter credentials when prompted
```

### Option 3: Using Configuration File
1. Create `email_config.json`:
```json
{
    "sender_email": "your-email@gmail.com",
    "sender_password": "your-app-password",
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587
}
```

2. Run:
```bash
python3 send_pdf_documents_oauth.py
```

### Option 4: Using Environment Variables
```bash
export EMAIL_SENDER='your-email@gmail.com'
export EMAIL_PASSWORD='your-app-password'
python3 send_pdf_documents_oauth.py
```

## Gmail App Password

If using Gmail, you'll need an App Password instead of your regular password:
1. Go to https://myaccount.google.com/security
2. Enable 2-Step Verification
3. Create an App Password for "Mail"
4. Use this 16-character password in the scripts

## Alternative Email Providers

For other providers, update the SMTP settings:
- **Outlook**: smtp.office365.com, port 587
- **Yahoo**: smtp.mail.yahoo.com, port 587
- **Custom**: Use your provider's SMTP settings

## Troubleshooting

- **Authentication Error**: Use an App Password for Gmail
- **Large Attachments**: Some providers limit to 25MB total
- **Connection Error**: Check firewall/antivirus settings
- **Missing PDFs**: Ensure all PDF files are in this directory

## Manual Alternative

If the scripts don't work, you can manually attach the PDFs to an email:
- To: nlr@universe-engine.ai
- Subject: UBC Circle - All PDF Documents for Business AMA
- Attach all PDFs from this directory