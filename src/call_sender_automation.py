# src/call_sender_automation.py
"""
Call Sender using Automation Apps
Works without ADB, root, or Developer Options.
Uses automation apps that can be controlled via HTTP/API.
"""

import csv
import time
import requests
from typing import Optional, Tuple
from datetime import datetime
from src.config.settings import (
    CONTACTS_FILE,
    CALL_DURATION,
    CALL_LOG_FILE,
)

# ----------------------
# Configuration
# ----------------------
# MacroDroid Webhook URL
# Get this from MacroDroid: Settings → Webhooks → Your webhook URL
MACRODROID_WEBHOOK_URL = "https://trigger.macrodroid.com/914d0a93-042b-402a-ab39-b2543b2b2d4a/call_trigger"  # Replace with your MacroDroid webhook URL

# ----------------------
# Logging
# ----------------------
def log(status: str, number: str, error: str = ""):
    """Log call attempts to file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(CALL_LOG_FILE, "a") as f:
        if status == "success":
            f.write(f"[{timestamp}] SUCCESS - Call to {number}\n")
        else:
            f.write(f"[{timestamp}] FAILED - {number} - {error}\n")

# ----------------------
# Number Formatting
# ----------------------
def format_number(num: str) -> str:
    """Convert number to format suitable for call intent."""
    num = num.strip().replace(" ", "")
    
    if num.startswith("+"):
        num = num[1:]
    
    # if num.startswith("0") and len(num) == 10:
    #     num = "254" + num[1:]
    
    if num.startswith("254") and len(num) == 12:
        return num
    
    if len(num) == 9:
        return "254" + num
    
    return num

def is_valid_number(num: str) -> bool:
    """Validate phone number format."""
    n = num.replace("+", "").replace("254", "").replace("0", "", 1)
    return n.isdigit() and len(n) >= 9

# ----------------------
# Automation App Methods
# ----------------------
def call_via_macrodroid_webhook(number: str) -> Tuple[bool, Optional[str]]:
    """
    Trigger call via MacroDroid Webhook URL.
    Requires MacroDroid app with Webhook trigger configured.
    """
    if not MACRODROID_WEBHOOK_URL or "macrodroid.com" not in MACRODROID_WEBHOOK_URL:
        return False, "MacroDroid webhook URL not configured correctly"
    
    try:
        # MacroDroid webhook format: https://trigger.macrodroid.com/xxxxx/webhook-id
        # You can pass data as query parameters or in the URL path
        # Method 1: Pass number as query parameter
        params = {
            "phone_number": number,
            "action": "call"
        }
        response = requests.get(f"{MACRODROID_WEBHOOK_URL}?{number}", timeout=20)
        # response = requests.get(MACRODROID_WEBHOOK_URL, params=params, timeout=2)
        
        # MacroDroid webhooks typically return 200 on success
        if response.status_code == 200:
            return True, None
        else:
            return False, f"MacroDroid webhook returned: {response.status_code}"
            
    except requests.exceptions.ConnectionError:
        return False, "Cannot connect to MacroDroid webhook - check internet connection"
    except Exception as e:
        return False, f"Error: {str(e)}"


# ----------------------
# Main Function
# ----------------------
def main():
    """Main function to process calls."""
    
    print("=" * 60)
    print("Call Sender - MacroDroid Webhook Method")
    print("=" * 60)
    print()
    print("This method uses MacroDroid webhooks - no ADB/root needed!")
    print()
    print("Setup required:")
    print("  1. Install MacroDroid app")
    print("  2. Create macro with Webhook trigger")
    print("  3. Get webhook URL from MacroDroid")
    print("  4. Update MACRODROID_WEBHOOK_URL in this script")
    print()
    
    # Test connection
    print("Testing MacroDroid webhook connection...")
    test_number = "0712345678"
    
    # Test MacroDroid webhook
    success, error = call_via_macrodroid_webhook(test_number)
    if not success:
        print("⚠ Cannot connect to MacroDroid webhook")
        print(f"  Error: {error}")
        print()
        print("Please:")
        print("  1. Set up MacroDroid webhook")
        print("  2. Get webhook URL from MacroDroid")
        print("  3. Update MACRODROID_WEBHOOK_URL in this script")
        print("  4. See AUTOMATION_APPS_SETUP.md for instructions")
        return
    
    print("✓ MacroDroid webhook connection works!")
    
    print()
    print("Processing calls...")
    print()
    
    try:
        with open(CONTACTS_FILE, newline="") as csvfile:
            reader = csv.reader(csvfile)
            
            for row in reader:
                if not row:
                    continue
                
                raw_number = row[0].strip()
                number = format_number(raw_number)
                
                if not is_valid_number(raw_number):
                    log("failed", raw_number, "Invalid number format")
                    print(f"✗ Skipping invalid number: {raw_number}")
                    continue
                
                print(f"Calling {number} (from {raw_number})...")
                
                # Delay to ensure MacroDroid processes previous call
                # This helps prevent number accumulation and server overload
                time.sleep(1.0)
                
                # Call via MacroDroid webhook with retry logic for timeouts
                success, error = call_via_macrodroid_webhook(number)
                
                # Retry once if timeout occurs (server might be slow after multiple calls)
                if not success and "timeout" in (error or "").lower():
                    print(f"  ⚠ Timeout detected, retrying in 2s...")
                    time.sleep(2.0)
                    success, error = call_via_macrodroid_webhook(number)
                
                if not success:
                    print(f"  ✗ Failed: {error}")
                    log("failed", raw_number, error or "Failed to trigger call")
                    continue
                
                print(f"  ✓ Call triggered")
                
                # Wait for call to ring
                print(f"  📞 Ringing ({CALL_DURATION}s)...")
                time.sleep(CALL_DURATION)
                
                # Note: Ending calls would require another automation trigger
                # For now, calls will end naturally or need manual intervention
                print(f"  ✓ Call completed")
                
                time.sleep(1.0)
                print(f"  ✓ Moving to next number...")
                print()
        
        print("✓ All calls processed!")
        
    except FileNotFoundError:
        print(f"✗ Error: {CONTACTS_FILE} not found!")
    except Exception as e:
        print(f"✗ Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()

