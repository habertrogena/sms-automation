import csv
import time
import requests
from src.utils.adb_controller import run_adb
from src.utils.logger import log
from src.utils.validator import is_valid_number
from src.config.settings import (
    SMS_MESSAGE,
    CONTACTS_FILE,
    SMS_GATEWAY_IP,
    SMS_GATEWAY_PORT,
    SMS_GATEWAY_USER,
    SMS_GATEWAY_PASS
)

# Delay between messages (seconds) for ADB/emulator
DELAY = 1

def send_sms(number: str, message: str):
    """
    Sends SMS via emulator/ADB.
    """
    try:
        run_adb(f"am start -a android.intent.action.SENDTO -d sms:{number}")
        time.sleep(1)

        run_adb(f"input text '{message}'")
        time.sleep(1)

        run_adb("input keyevent 22")  # focus send
        run_adb("input keyevent 66")  # press send
        time.sleep(DELAY)

        log("success", number)

    except Exception as e:
        log("failed", number, str(e))


def send_sms_gateway(number: str, message: str, sim_slot: int = 0, retries: int = 3):
    """
    Sends SMS via SMS Gateway for Android with retry logic.
    """
    url = f"http://{SMS_GATEWAY_IP}:{SMS_GATEWAY_PORT}/message"
    payload = {
        "textMessage": {"text": message},
        "phoneNumbers": [number],
        "simSlot": sim_slot
    }

    for attempt in range(1, retries + 1):
        try:
            response = requests.post(
                url,
                json=payload,
                auth=(SMS_GATEWAY_USER, SMS_GATEWAY_PASS),
                timeout=10
            )
            response.raise_for_status()
            log("success", number)
            return
        except requests.RequestException as e:
            print(f"Attempt {attempt} failed for {number}: {e}")
            if attempt == retries:
                log("failed", number, str(e))
            else:
                time.sleep(2)  # wait 2 seconds before retry


def main(use_gateway=False, sim_slot=0):
    """
    Reads CSV and sends messages.
    use_gateway: True -> SMS Gateway; False -> emulator/ADB
    sim_slot: 0 or 1 for dual-SIM phones
    """
    try:
        with open(CONTACTS_FILE, newline="") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if not row:
                    continue
                number = row[0].strip()

                if not is_valid_number(number):
                    log("failed", number, "Invalid phone number")
                    continue

                print(f"Sending SMS to {number}...")
                if use_gateway:
                    send_sms_gateway(number, SMS_MESSAGE, sim_slot)
                else:
                    send_sms(number, SMS_MESSAGE)

        print("All messages processed!")

    except FileNotFoundError:
        print(f"Error: {CONTACTS_FILE} not found!")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")


if __name__ == "__main__":
    # Example usage:
    # Emulator/ADB:
    # main(use_gateway=False)
    # Real phone (SIM1):
    main(use_gateway=True, sim_slot=0)
