# SMS Automation System

## Overview
This Python script automates sending SMS messages to a list of phone numbers using an Android emulator and ADB.

## Features
- Reads phone numbers from `contacts.csv`
- Sends a predefined SMS message
- Validates phone numbers
- Logs successful and failed attempts with timestamps

## Setup Instructions

1. **Clone the repository**  
   ```bash
   git clone <repo_url>
   cd sms-automation

2. **Create and activate virtual environment**
   python3 -m venv venv
   source venv/bin/activate

3. **Install dependancies**
   pip install -r requirements.txt

4. **Install ADB (depends with the OS, for linux Mint users)**
   sudo apt update
   sudo apt install android-tools-adb android-tools-fastboot

5. **Start Android Emulator**
   Use Android Studio → Tools → AVD Manager → Start device

6. **Prepare contacts**
   Add phone numbers to data/contacts.csv, one per line

7. **Run the script**
   python -m src.sms_sender

8. **Check logs**
   Logs are stored in data/sms_log.txt

## Notes
- Python 3.12 recommended

- Linux Mint tested

- Emulator must be running before script execution

