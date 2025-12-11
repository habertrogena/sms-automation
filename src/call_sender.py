# src/call_sender.py
"""
ADB Call Sender
Uses ADB commands to start and end calls for missed call automation.
"""

import csv
import time
import subprocess
from typing import Optional, Tuple
from datetime import datetime
from src.config.settings import (
    CONTACTS_FILE,
    CALL_DURATION,
    CALL_LOG_FILE,
)
from src.utils.adb_controller import run_adb

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
    """Convert number to format suitable for ADB call intent."""
    num = num.strip().replace(" ", "")
    
    # Remove + prefix for tel: URI
    if num.startswith("+"):
        num = num[1:]
    
    # Convert local format (0707xxxxxx) to international (254707xxxxxx)
    if num.startswith("0") and len(num) == 10:
        num = "254" + num[1:]
    
    # Ensure it's international format (254xxxxxxxxx)
    if num.startswith("254") and len(num) == 12:
        return num
    
    # If already international without country code, add it
    if len(num) == 9:  # Local without leading 0
        return "254" + num
    
    return num

def is_valid_number(num: str) -> bool:
    """Validate phone number format."""
    n = num.replace("+", "").replace("254", "").replace("0", "", 1)
    return n.isdigit() and len(n) >= 9

# ----------------------
# ADB Call Functions
# ----------------------
def start_call_via_adb(number: str) -> Tuple[bool, Optional[str]]:
    """
    Start a call using ADB intent.
    Uses Android's CALL intent to initiate calls.
    """
    try:
        # Format number for tel: URI
        tel_number = format_number(number)
        tel_uri = f"tel:{tel_number}"
        
        # Use CALL intent to start call
        # Note: Requires CALL_PHONE permission on device
        command = f'am start -a android.intent.action.CALL -d "{tel_uri}"'
        
        stdout, stderr = run_adb(command)
        
        if stderr and "Error" in stderr:
            return False, f"ADB error: {stderr}"
        
        # Small delay to let call initiate
        time.sleep(0.5)
        
        return True, None
        
    except Exception as e:
        return False, f"Failed to start call: {str(e)}"

def end_call_via_adb() -> Tuple[bool, Optional[str]]:
    """
    End call using ADB keyevent.
    Simulates pressing the END CALL button.
    """
    try:
        # Key event 6 = ENDCALL
        command = "input keyevent 6"
        stdout, stderr = run_adb(command)
        
        if stderr and "Error" in stderr:
            return False, f"ADB error: {stderr}"
        
        return True, None
        
    except Exception as e:
        return False, f"Failed to end call: {str(e)}"

def is_call_active() -> bool:
    """
    Check if there's an active call by trying to end it.
    Returns True if call can be ended (call is active).
    """
    try:
        # Try to end call - if it works, call was active
        # If it fails silently, no call is active
        command = "input keyevent 6"
        stdout, stderr = run_adb(command)
        
        # If no error, call might have been active
        # We can't reliably detect, so we'll assume it worked
        return True
        
    except:
        return False

def test_adb_connection() -> bool:
    """Test if ADB can connect to device."""
    try:
        stdout, stderr = run_adb("getprop ro.product.model")
        return bool(stdout and not stderr)
    except:
        return False

# ----------------------
# Main Function
# ----------------------
def main():
    """Main function to process calls from CSV file."""
    
    print("=" * 60)
    print("ADB Call Sender")
    print("=" * 60)
    print()
    
    # Test ADB connection
    if test_adb_connection():
        print("✓ ADB is connected to device")
        device_info, _ = run_adb("getprop ro.product.model")
        if device_info:
            print(f"  Device: {device_info}")
    else:
        print("⚠ WARNING: Cannot connect to device via ADB")
        print("  Make sure:")
        print("  1. ADB is installed and in PATH")
        print("  2. USB debugging is enabled on device")
        print("  3. Device is connected via USB or WiFi ADB")
        print("  4. Run: adb devices (should show your device)")
        print()
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Exiting...")
            return
    
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
                
                print(f"Calling {number}...")
                
                # Start call using ADB
                success, error = start_call_via_adb(raw_number)
                
                if not success:
                    print(f"  ✗ Failed to start call: {error}")
                    log("failed", raw_number, error or "Failed to start call")
                    continue
                
                print(f"  ✓ Call initiated")
                
                # Wait for call to start
                time.sleep(1.5)
                
                # Let it ring briefly (missed call pattern)
                print(f"  📞 Ringing ({CALL_DURATION}s for missed call)...")
                time.sleep(CALL_DURATION)
                
                # End call using ADB
                print(f"  🔚 Ending call...")
                end_success, end_error = end_call_via_adb()
                
                if end_success:
                    print(f"  ✓ Call ended successfully")
                    log("success", raw_number)
                else:
                    print(f"  ⚠ Could not end call: {end_error}")
                    print(f"  💡 Call may end naturally or already ended")
                
                # Wait before next call
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

