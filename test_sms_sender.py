#!/usr/bin/env python3
"""
SMS Sender Test Script
Tests SMS sending in both ADB and Gateway modes.
"""

import sys
from src.sms_sender import send_sms, send_sms_gateway
from src.config.settings import SMS_MESSAGE, SMS_GATEWAY_IP, SMS_GATEWAY_PORT

def test_adb_mode():
    """Test SMS sending via ADB."""
    print("=" * 60)
    print("Testing ADB Mode (Emulator)")
    print("=" * 60)
    print()
    
    test_number = "0712345678"
    print(f"Test number: {test_number}")
    print(f"Message: {SMS_MESSAGE}")
    print()
    
    response = input("Send test SMS via ADB? (y/n): ")
    if response.lower() != 'y':
        print("Skipped.")
        return
    
    print("\nSending SMS...")
    try:
        send_sms(test_number, SMS_MESSAGE)
        print("✓ SMS sent via ADB")
        print("  Check emulator to verify message was sent")
    except Exception as e:
        print(f"✗ Error: {e}")

def test_gateway_mode():
    """Test SMS sending via SMS Gateway API."""
    print("=" * 60)
    print("Testing Gateway Mode (Real Device)")
    print("=" * 60)
    print()
    
    print(f"SMS Gateway: {SMS_GATEWAY_IP}:{SMS_GATEWAY_PORT}")
    print()
    
    # Test connection first
    import requests
    from src.config.settings import SMS_GATEWAY_USER, SMS_GATEWAY_PASS
    
    try:
        url = f"http://{SMS_GATEWAY_IP}:{SMS_GATEWAY_PORT}/"
        response = requests.get(url, auth=(SMS_GATEWAY_USER, SMS_GATEWAY_PASS), timeout=5)
        print(f"✓ SMS Gateway is reachable (Status: {response.status_code})")
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to SMS Gateway")
        print("\nMake sure:")
        print("  1. SMS Gateway app is installed on device")
        print("  2. SMS Gateway server is running")
        print("  3. Device IP is correct in settings.py")
        print("  4. Device and computer are on same network")
        return
    except Exception as e:
        print(f"⚠ Connection test: {e}")
    
    print()
    test_number = "0712345678"
    print(f"Test number: {test_number}")
    print(f"Message: {SMS_MESSAGE}")
    print()
    
    response = input("Send test SMS via Gateway? (y/n): ")
    if response.lower() != 'y':
        print("Skipped.")
        return
    
    print("\nSending SMS...")
    try:
        send_sms_gateway(test_number, SMS_MESSAGE, sim_slot=0)
        print("✓ SMS sent via Gateway")
        print("  Check device to verify message was sent")
    except Exception as e:
        print(f"✗ Error: {e}")

def main():
    """Main test menu."""
    print("\n" + "=" * 60)
    print("SMS Sender Test Menu")
    print("=" * 60)
    print()
    print("Choose test mode:")
    print("  1. ADB Mode (Emulator - currently connected)")
    print("  2. Gateway Mode (Real Device - requires SMS Gateway app)")
    print("  3. Test both")
    print("  4. Exit")
    print()
    
    choice = input("Enter choice (1-4): ").strip()
    
    if choice == "1":
        test_adb_mode()
    elif choice == "2":
        test_gateway_mode()
    elif choice == "3":
        test_adb_mode()
        print("\n" + "-" * 60 + "\n")
        test_gateway_mode()
    elif choice == "4":
        print("Exiting...")
        sys.exit(0)
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()

