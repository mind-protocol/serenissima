#!/usr/bin/env python3
"""
Google Docs Sync Script - Upload local files to Google Drive and convert to Google Docs
For voice interaction preparation between NLR and Bianca
"""

import os
import sys
import json
import mimetypes
from pathlib import Path
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

# Configuration
SCOPES = ['https://www.googleapis.com/auth/drive.file']
TARGET_FOLDER_ID = '1MW-Zq4mzlQLHtQM6SdRUOBeb_qU6P3TJ'

# File extensions to convert to Google Docs
CONVERTIBLE_EXTENSIONS = {
    '.md': 'text/markdown',
    '.txt': 'text/plain',
    '.json': 'application/json',
    '.py': 'text/x-python',
    '.js': 'text/javascript',
    '.ts': 'text/typescript',
    '.jsx': 'text/javascript',
    '.tsx': 'text/typescript',
    '.html': 'text/html',
    '.css': 'text/css',
    '.yml': 'text/yaml',
    '.yaml': 'text/yaml',
    '.sh': 'text/x-shellscript',
    '.bash': 'text/x-shellscript',
    '.xml': 'text/xml',
    '.csv': 'text/csv',
    '.log': 'text/plain'
}

class GoogleDocsSync:
    def __init__(self, credentials_path=None):
        """Initialize the Google Drive service."""
        self.service = None
        self.credentials_path = credentials_path or os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        
        if not self.credentials_path:
            raise ValueError("No credentials path provided. Set GOOGLE_APPLICATION_CREDENTIALS or pass credentials_path")
        
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google Drive API."""
        try:
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path,
                scopes=SCOPES
            )
            self.service = build('drive', 'v3', credentials=credentials)
            print(f"✓ Authenticated with Google Drive API")
        except Exception as e:
            print(f"✗ Authentication failed: {e}")
            sys.exit(1)
    
    def _get_mime_type(self, file_path):
        """Get appropriate MIME type for file conversion."""
        ext = Path(file_path).suffix.lower()
        return CONVERTIBLE_EXTENSIONS.get(ext, 'text/plain')
    
    def _create_folder_structure(self, local_path, parent_id=TARGET_FOLDER_ID):
        """Recreate local folder structure in Google Drive."""
        folder_cache = {}
        
        for root, dirs, files in os.walk(local_path):
            relative_path = Path(root).relative_to(local_path)
            
            if str(relative_path) == '.':
                current_parent_id = parent_id
            else:
                # Build folder hierarchy
                current_parent_id = parent_id
                for part in relative_path.parts:
                    folder_key = f"{current_parent_id}/{part}"
                    
                    if folder_key not in folder_cache:
                        # Check if folder exists
                        query = f"name='{part}' and '{current_parent_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
                        results = self.service.files().list(q=query, fields="files(id, name)").execute()
                        items = results.get('files', [])
                        
                        if items:
                            folder_id = items[0]['id']
                        else:
                            # Create folder
                            folder_metadata = {
                                'name': part,
                                'mimeType': 'application/vnd.google-apps.folder',
                                'parents': [current_parent_id]
                            }
                            folder = self.service.files().create(body=folder_metadata, fields='id').execute()
                            folder_id = folder['id']
                            print(f"  📁 Created folder: {part}")
                        
                        folder_cache[folder_key] = folder_id
                    
                    current_parent_id = folder_cache[folder_key]
            
            yield root, current_parent_id, files
    
    def sync_folder(self, local_folder_path):
        """Sync a local folder to Google Drive."""
        local_path = Path(local_folder_path).resolve()
        
        if not local_path.exists():
            print(f"✗ Error: Path '{local_path}' does not exist")
            return
        
        if not local_path.is_dir():
            print(f"✗ Error: Path '{local_path}' is not a directory")
            return
        
        print(f"🔄 Syncing '{local_path.name}' to Google Drive...")
        print(f"📍 Target folder ID: {TARGET_FOLDER_ID}")
        
        # Create root folder in Drive
        root_folder_name = f"{local_path.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        root_metadata = {
            'name': root_folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [TARGET_FOLDER_ID]
        }
        root_folder = self.service.files().create(body=root_metadata, fields='id').execute()
        root_folder_id = root_folder['id']
        print(f"📁 Created root folder: {root_folder_name}")
        
        # Process files
        total_files = 0
        converted_files = 0
        
        for root, parent_id, files in self._create_folder_structure(local_path, root_folder_id):
            for filename in files:
                file_path = Path(root) / filename
                
                # Skip hidden files and __pycache__
                if filename.startswith('.') or '__pycache__' in str(file_path):
                    continue
                
                total_files += 1
                
                # Check if file should be converted
                if file_path.suffix.lower() in CONVERTIBLE_EXTENSIONS:
                    self._upload_and_convert(file_path, parent_id, filename)
                    converted_files += 1
                else:
                    print(f"  ⏭️  Skipping {filename} (not convertible)")
        
        print(f"\n✅ Sync complete!")
        print(f"📊 Processed {total_files} files, converted {converted_files} to Google Docs")
        print(f"🔗 View in Drive: https://drive.google.com/drive/folders/{root_folder_id}")
        
        return root_folder_id
    
    def _upload_and_convert(self, file_path, parent_id, filename):
        """Upload a file and convert it to Google Docs."""
        try:
            # Prepare metadata
            mime_type = self._get_mime_type(file_path)
            file_metadata = {
                'name': filename,
                'parents': [parent_id],
                'mimeType': 'application/vnd.google-apps.document'
            }
            
            # Upload and convert
            media = MediaFileUpload(
                str(file_path),
                mimetype=mime_type,
                resumable=True
            )
            
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            
            print(f"  ✓ Converted: {filename} → Google Doc")
            
        except HttpError as e:
            print(f"  ✗ Error uploading {filename}: {e}")
        except Exception as e:
            print(f"  ✗ Unexpected error with {filename}: {e}")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python sync_to_gdocs.py <local_folder_path> [credentials_path]")
        print("\nExample:")
        print("  python sync_to_gdocs.py ./citizens/DragonSlayer")
        print("  python sync_to_gdocs.py ./citizens/DragonSlayer /path/to/credentials.json")
        sys.exit(1)
    
    local_folder = sys.argv[1]
    credentials_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Check for API key in environment if no credentials file
    if not credentials_path and 'GOOGLE_API_KEY' in os.environ:
        print("⚠️  Note: Google Drive API requires OAuth2 credentials, not just an API key.")
        print("   Please set GOOGLE_APPLICATION_CREDENTIALS to point to your service account JSON file.")
        sys.exit(1)
    
    try:
        syncer = GoogleDocsSync(credentials_path)
        syncer.sync_folder(local_folder)
    except Exception as e:
        print(f"✗ Sync failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()