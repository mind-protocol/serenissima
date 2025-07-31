# Email Attachments Support

The Venice email system now supports sending file attachments, enabling citizens to share documents, images, reports, and other files with their human partners.

## Features

- **Multiple file attachments** per email
- **Automatic MIME type detection** for proper encoding
- **Support for all file types**: PDFs, images, documents, spreadsheets, etc.
- **Smart handling** of text, image, audio, and binary files
- **File validation** with warnings for missing files
- **Detailed logging** of attached files

## Usage

### Command Line

```bash
# Single attachment
python3 send_email_with_attachments.py "partner@example.com" "Report" "Please review the attached report." --attach report.pdf

# Multiple attachments
python3 send_email_with_attachments.py "client@example.com" "Project Files" "All requested files attached." --attach design.png spec.doc budget.xlsx

# Attachments only (uses default body text)
python3 send_email_with_attachments.py "user@example.com" "Documents" --attach contract.pdf
```

### Python API

```python
from send_email_with_attachments import send_email_with_attachments

# Send with attachments
result = send_email_with_attachments(
    to_email="partner@example.com",
    subject="Venice Partnership Proposal",
    body="Please find our proposal attached.",
    attachments=["proposal.pdf", "financials.xlsx"],
    from_name="Mechanical Visionary"
)

# Multiple recipients with CC/BCC
result = send_email_with_attachments(
    to_email=["investor1@example.com", "investor2@example.com"],
    subject="Investment Opportunity",
    body="Attached: Executive summary and projections",
    attachments=["exec_summary.pdf", "projections.xlsx"],
    cc="team@serenissima.ai",
    bcc="archive@serenissima.ai",
    reply_to="investments@serenissima.ai"
)
```

## File Type Support

The system automatically detects and properly encodes:

- **Documents**: PDF, DOC, DOCX, TXT, RTF
- **Images**: PNG, JPG, GIF, BMP, SVG
- **Spreadsheets**: XLS, XLSX, CSV
- **Archives**: ZIP, RAR, 7Z
- **Audio**: MP3, WAV, OGG
- **Any other file type** as binary attachment

## Size Limitations

- Individual file size: Limited by email server (typically 25MB)
- Total email size: Server-dependent (usually 25-50MB)
- For larger files, consider using file sharing services and sending links

## Integration with Citizens

Citizens can now send proposals, reports, designs, and other documents directly to human partners:

```python
# In citizen code
def send_partnership_proposal(self, partner_email):
    # Generate proposal document
    proposal_path = self.create_proposal_document()
    
    # Send with attachment
    result = send_email_with_attachments(
        to_email=partner_email,
        subject=f"Partnership Proposal from {self.name}",
        body=self.craft_partnership_message(),
        attachments=[proposal_path, "venice_overview.pdf"],
        from_name=self.full_name
    )
    
    return result
```

## Error Handling

The system handles errors gracefully:
- Missing files generate warnings but don't stop the email
- Failed attachments are logged
- Email still sends with successful attachments
- Detailed error messages for troubleshooting

## Security Notes

- Files are read in binary mode to preserve integrity
- Base64 encoding ensures safe transport
- No execution of attached files
- Original files remain unchanged

## Examples

See `example_send_with_attachments.py` for complete examples including:
- Sending reports with PDFs
- Multi-file proposals
- Programmatic usage in citizen code
- Command line usage patterns