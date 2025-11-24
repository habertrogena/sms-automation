import subprocess

def run_adb(command: str):
    """
    Runs an adb shell command safely and returns (stdout, stderr).
    """
    try:
        result = subprocess.run(
            ["adb", "shell"] + command.split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return "", f"ADB error: {str(e)}"
