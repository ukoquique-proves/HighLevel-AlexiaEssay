#!/usr/bin/env python3
"""
HighLevel Token Manager
Automates OAuth 2.0 token generation and refresh for HighLevel API
"""

import requests
import json
import os
import webbrowser
from urllib.parse import urlparse, parse_qs
import time

class HighLevelTokenManager:
    def __init__(self, client_id, client_secret, redirect_uri="http://localhost:8080"):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.token_file = "/home/uko/COLOMBIA/ALEXIA/Proyecto-/.highlevel_tokens.json"
        self.base_url = "https://api.gohighlevel.com"
        
    def generate_auth_url(self):
        """Generate the authorization URL for manual approval"""
        auth_url = (
            f"https://marketplace.gohighlevel.com/oauth/chooselocation?"
            f"response_type=code&"
            f"redirect_uri={self.redirect_uri}&"
            f"client_id={self.client_id}&"
            f"scope=contacts.write opportunities.write"
        )
        return auth_url
    
    def get_tokens_from_code(self, auth_code):
        """Exchange authorization code for access and refresh tokens"""
        token_url = f"{self.base_url}/OAuth/token"
        
        data = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': auth_code,
            'redirect_uri': self.redirect_uri
        }
        
        response = requests.post(token_url, data=data)
        
        if response.status_code == 200:
            tokens = response.json()
            self.save_tokens(tokens)
            return tokens
        else:
            raise Exception(f"Failed to get tokens: {response.text}")
    
    def refresh_access_token(self):
        """Use refresh token to get new access token"""
        tokens = self.load_tokens()
        if not tokens or 'refresh_token' not in tokens:
            raise Exception("No refresh token found. Run manual authorization first.")
        
        token_url = f"{self.base_url}/OAuth/token"
        
        data = {
            'grant_type': 'refresh_token',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': tokens['refresh_token']
        }
        
        response = requests.post(token_url, data=data)
        
        if response.status_code == 200:
            new_tokens = response.json()
            # Preserve refresh token if not provided
            if 'refresh_token' not in new_tokens:
                new_tokens['refresh_token'] = tokens['refresh_token']
            self.save_tokens(new_tokens)
            return new_tokens
        else:
            raise Exception(f"Failed to refresh token: {response.text}")
    
    def save_tokens(self, tokens):
        """Save tokens to file"""
        with open(self.token_file, 'w') as f:
            json.dump(tokens, f, indent=2)
    
    def load_tokens(self):
        """Load tokens from file"""
        if os.path.exists(self.token_file):
            with open(self.token_file, 'r') as f:
                return json.load(f)
        return None
    
    def get_valid_token(self):
        """Get a valid access token, refreshing if necessary"""
        tokens = self.load_tokens()
        if not tokens:
            raise Exception("No tokens found. Run manual authorization first.")
        
        # Check if token is expired (with 5 minute buffer)
        if 'expires_at' in tokens:
            expires_at = tokens['expires_at']
            if time.time() > expires_at - 300:  # 5 minute buffer
                print("Token expired, refreshing...")
                tokens = self.refresh_access_token()
        
        return tokens['access_token']
    
    def manual_authorization_flow(self):
        """Complete manual authorization flow"""
        print("=== HighLevel Token Manager ===")
        print("1. Opening authorization URL in browser...")
        
        auth_url = self.generate_auth_url()
        print(f"Authorization URL: {auth_url}")
        print("\n2. Please visit this URL in your browser and authorize the app.")
        print("3. After authorization, you'll be redirected to a URL.")
        print("4. Copy the 'code' parameter from the redirect URL.")
        
        # Open browser
        webbrowser.open(auth_url)
        
        auth_code = input("\nEnter the authorization code from the redirect URL: ").strip()
        
        print("5. Exchanging code for tokens...")
        tokens = self.get_tokens_from_code(auth_code)
        
        # Add expiration time
        tokens['expires_at'] = time.time() + tokens['expires_in']
        self.save_tokens(tokens)
        
        print("✅ Tokens saved successfully!")
        print(f"Access Token: {tokens['access_token'][:20]}...")
        print(f"Refresh Token: {tokens['refresh_token'][:20]}...")
        print(f"Location ID: {tokens.get('locationId', 'Not provided')}")
        
        return tokens

def main():
    """Main CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='HighLevel Token Manager')
    parser.add_argument('--setup', action='store_true', help='Run manual authorization setup')
    parser.add_argument('--refresh', action='store_true', help='Refresh access token')
    parser.add_argument('--get-token', action='store_true', help='Get current valid token')
    
    args = parser.parse_args()
    
    # Get credentials from environment
    client_id = os.getenv('HIGHLEVEL_CLIENT_ID')
    client_secret = os.getenv('HIGHLEVEL_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        print("❌ Please set HIGHLEVEL_CLIENT_ID and HIGHLEVEL_CLIENT_SECRET environment variables")
        print("   Example: export HIGHLEVEL_CLIENT_ID=your_client_id")
        print("   Example: export HIGHLEVEL_CLIENT_SECRET=your_client_secret")
        return
    
    manager = HighLevelTokenManager(client_id, client_secret)
    
    if args.setup:
        manager.manual_authorization_flow()
    elif args.refresh:
        try:
            tokens = manager.refresh_access_token()
            print("✅ Token refreshed successfully!")
            print(f"New Access Token: {tokens['access_token'][:20]}...")
        except Exception as e:
            print(f"❌ Error refreshing token: {e}")
    elif args.get_token:
        try:
            token = manager.get_valid_token()
            print(f"✅ Valid Access Token: {token}")
        except Exception as e:
            print(f"❌ Error getting token: {e}")
    else:
        print("HighLevel Token Manager")
        print("Usage:")
        print("  python highlevel_token_manager.py --setup    # Initial authorization")
        print("  python highlevel_token_manager.py --refresh  # Refresh token")
        print("  python highlevel_token_manager.py --get-token # Get current token")

if __name__ == "__main__":
    main()
