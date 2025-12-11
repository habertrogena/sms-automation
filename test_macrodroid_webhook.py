#!/usr/bin/env python3
"""
Test MacroDroid Webhook Connection
Helps verify your webhook URL is working.
"""

import requests
from src.call_sender_automation import MACRODROID_WEBHOOK_URL, call_via_macrodroid_webhook

def test_webhook():
    """Test the MacroDroid webhook connection."""
    print("=" * 60)
    print("MacroDroid Webhook Test")
    print("=" * 60)
    print()
    
    if not MACRODROID_WEBHOOK_URL or "macrodroid.com" not in MACRODROID_WEBHOOK_URL:
        print("⚠ Webhook URL not configured!")
        print()
        print("Please:")
        print("  1. Open MacroDroid app")
        print("  2. Create a macro with Webhook trigger")
        print("  3. Copy the webhook URL")
        print("  4. Update MACRODROID_WEBHOOK_URL in src/call_sender_automation.py")
        print()
        print("Current URL:", MACRODROID_WEBHOOK_URL or "Not set")
        return
    
    print(f"Webhook URL: {MACRODROID_WEBHOOK_URL}")
    print()
    
    # Test with a sample number
    test_number = "0712345678"
    print(f"Testing with number: {test_number}")
    print()
    
    print("Sending webhook request...")
    success, error = call_via_macrodroid_webhook(test_number)
    
    if success:
        print("✓ Webhook request sent successfully!")
        print()
        print("Check your device:")
        print("  - MacroDroid should have triggered the macro")
        print("  - Call should be initiated (if macro is configured correctly)")
    else:
        print(f"✗ Webhook request failed: {error}")
        print()
        print("Troubleshooting:")
        print("  1. Verify webhook URL is correct")
        print("  2. Check internet connection")
        print("  3. Ensure macro is active in MacroDroid")
        print("  4. Check MacroDroid logs for errors")

if __name__ == "__main__":
    test_webhook()

