import csv
import time
from src.utils.adb_controller import run_adb
from src.utils.logger import log
from src.utils.validator import is_valid_number
from src.config.settings import SMS_MESSAGE, CONTACTS_FILE

# Time delay between messages (seconds)
DELAY = 1

def send_sms(number: str, message: str):
    """
    Sends a message to a single number using ADB.
    """
    try:
        # Open default SMS app with the number
        run_adb(f"am start -a android.intent.action.SENDTO -d sms:{number}")
        time.sleep(1)  # wait for app to open

        # Type the message
        run_adb(f"input text '{message}'")
        time.sleep(1)

        # Press send
        run_adb("input keyevent 22")  # focus send arrow
        run_adb("input keyevent 66")  # press enter
        time.sleep(DELAY)

        # Log success
        log("success", number)

    except Exception as e:
        # Log failure
        log("failed", number, str(e))


def main():
    """
    Main function: read CSV and send SMS to each valid number
    """
    try:
        with open(CONTACTS_FILE, newline="") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if not row:
                    continue
                number = row[0].strip()

                if not is_valid_number(number):
                    log("failed", number, "Invalid number format")
                    continue

                print(f"Sending SMS to {number}...")
                send_sms(number, SMS_MESSAGE)

        print("All messages processed!")

    except FileNotFoundError:
        print(f"Error: {CONTACTS_FILE} not found!")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")


if __name__ == "__main__":
    main()
