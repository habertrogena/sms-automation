#!/usr/bin/env python3
"""
Helper script to add real phone numbers to contacts.csv
"""

import csv
import sys
from src.config.settings import CONTACTS_FILE

def add_contact(number: str):
    """Add a phone number to contacts.csv"""
    number = number.strip()
    
    # Read existing contacts
    contacts = []
    try:
        with open(CONTACTS_FILE, 'r', newline='') as f:
            reader = csv.reader(f)
            contacts = [row[0].strip() for row in reader if row and row[0].strip()]
    except FileNotFoundError:
        pass
    
    # Check if already exists
    if number in contacts:
        print(f"⚠ Number {number} already exists in contacts")
        return False
    
    # Add new contact
    contacts.append(number)
    
    # Write back
    with open(CONTACTS_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        for contact in contacts:
            writer.writerow([contact])
    
    print(f"✓ Added {number} to contacts.csv")
    return True

def show_contacts():
    """Show all contacts"""
    try:
        with open(CONTACTS_FILE, 'r', newline='') as f:
            reader = csv.reader(f)
            contacts = [row[0].strip() for row in reader if row and row[0].strip()]
        
        print(f"\nCurrent contacts ({len(contacts)}):")
        for i, contact in enumerate(contacts, 1):
            print(f"  {i}. {contact}")
        print()
    except FileNotFoundError:
        print("No contacts file found")

def main():
    if len(sys.argv) > 1:
        # Add contact from command line
        number = sys.argv[1]
        add_contact(number)
        show_contacts()
    else:
        # Interactive mode
        print("=" * 60)
        print("Add Contacts to CSV")
        print("=" * 60)
        print()
        show_contacts()
        
        print("Enter phone numbers to add (one per line, or 'done' to finish):")
        numbers = []
        while True:
            number = input("Number (or 'done'): ").strip()
            if number.lower() == 'done':
                break
            if number:
                numbers.append(number)
        
        if numbers:
            print()
            for number in numbers:
                add_contact(number)
            print()
            show_contacts()
            print("\n✓ Contacts updated!")
            print("Run: python3 -m src.call_sender_automation")

if __name__ == "__main__":
    main()




