from datetime import datetime

LOG_FILE = "data/sms_log.txt"

def log(status: str, number: str, error: str = ""):
    """
    Write a timestamped log entry to sms_log.txt.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a") as f:
        if status == "success":
            f.write(f"[{timestamp}] SUCCESS - Message sent to {number}\n")
        else:
            f.write(f"[{timestamp}] FAILED - {number} - {error}\n")
