#!/usr/bin/env python3
"""Debug email authentication for IONOS"""

import os
import smtplib
import ssl
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(env_path)

def test_smtp_connection():
    """Test various SMTP configurations"""
    
    email = os.environ.get('DIPLOMATIC_EMAIL')
    password = os.environ.get('DIPLOMATIC_EMAIL_PASSWORD')
    
    print(f"Testing email authentication for: {email}")
    print("-" * 50)
    
    # Test configurations
    configs = [
        # IONOS standard settings
        {"server": "smtp.ionos.com", "port": 587, "use_tls": True, "name": "IONOS TLS"},
        {"server": "smtp.ionos.com", "port": 465, "use_ssl": True, "name": "IONOS SSL"},
        
        # Alternative IONOS servers
        {"server": "smtp.ionos.de", "port": 587, "use_tls": True, "name": "IONOS.de TLS"},
        {"server": "smtp.ionos.de", "port": 465, "use_ssl": True, "name": "IONOS.de SSL"},
        
        # 1&1 IONOS variations
        {"server": "smtp.1and1.com", "port": 587, "use_tls": True, "name": "1and1 TLS"},
        {"server": "smtp.1and1.com", "port": 465, "use_ssl": True, "name": "1and1 SSL"},
    ]
    
    for config in configs:
        print(f"\nTesting {config['name']}...")
        print(f"Server: {config['server']}, Port: {config['port']}")
        
        try:
            if config.get('use_ssl'):
                # SSL connection
                context = ssl.create_default_context()
                server = smtplib.SMTP_SSL(config['server'], config['port'], context=context)
            else:
                # TLS connection
                server = smtplib.SMTP(config['server'], config['port'])
                if config.get('use_tls'):
                    server.starttls()
            
            # Try login
            server.login(email, password)
            print(f"✅ SUCCESS! Authentication worked with {config['name']}")
            
            # If successful, save the working config
            save_working_config(config)
            
            server.quit()
            return config
            
        except smtplib.SMTPAuthenticationError as e:
            print(f"❌ Authentication failed: {e}")
        except smtplib.SMTPException as e:
            print(f"❌ SMTP error: {e}")
        except Exception as e:
            print(f"❌ Connection error: {e}")
    
    print("\n" + "="*50)
    print("All configurations failed. Possible issues:")
    print("1. Password might need to be an app-specific password")
    print("2. Account might need SMTP explicitly enabled")
    print("3. Two-factor authentication might be blocking")
    print("4. Email address format might need adjustment")
    
    # Try with just username (without @domain)
    print("\nTrying with username only...")
    username = email.split('@')[0]
    try:
        server = smtplib.SMTP("smtp.ionos.com", 587)
        server.starttls()
        server.login(username, password)
        print(f"✅ SUCCESS with username only: {username}")
        server.quit()
    except Exception as e:
        print(f"❌ Username-only login failed: {e}")

def save_working_config(config):
    """Save the working configuration"""
    working_config = {
        "DIPLOMATIC_SMTP_SERVER": config['server'],
        "DIPLOMATIC_SMTP_PORT": str(config['port']),
        "DIPLOMATIC_SMTP_USE_SSL": str(config.get('use_ssl', False)),
        "DIPLOMATIC_SMTP_USE_TLS": str(config.get('use_tls', False))
    }
    
    config_path = Path(__file__).parent / 'working_email_config.json'
    import json
    with open(config_path, 'w') as f:
        json.dump(working_config, f, indent=2)
    
    print(f"\n💾 Saved working configuration to: {config_path}")

if __name__ == "__main__":
    test_smtp_connection()