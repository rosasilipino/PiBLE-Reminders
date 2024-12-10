'''
Names: Rosa Lisa Silipino, Jose Urrutia, Alberto Escalante
Class: CS 578 Final Project
File: ble.py
Description:
This Python script monitors the RSSI (signal strength) of a specified Bluetooth Low Energy (BLE) device.
It uses the `bleak` library for BLE scanning and sends notifications via IFTTT if the device moves out of range.
Reminders are fetched from a JSON file (`reminders.json`) and sent as alerts when the device disconnects or exceeds a distance threshold.
Key functionalities:
- Monitor BLE device signal strength and log RSSI values.
- Fetch reminders from a JSON file.
- Send notifications using IFTTT webhook.
'''

from bleak import BleakScanner
import asyncio
import time
import requests
import json

# IFTTT Configuration
IFTTT_EVENT_NAME = "bluetooth_disconnect"  # IFTTT event name
IFTTT_KEY = "klPVP4wQ234wKjclDmWQqswyd1mkksG7PXy96SSXtUh"  # IFTTT webhook key
IFTTT_URL = f"https://maker.ifttt.com/trigger/{IFTTT_EVENT_NAME}/with/key/{IFTTT_KEY}"

# Function to fetch reminders from the JSON file
def get_reminders():
    """Fetch reminders from reminders.json."""
    reminder_file = "/home/admin/cs578/project/reminders.json"
    try:
        with open(reminder_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Reminder file not found. Using an empty list.")
        return []
    except json.JSONDecodeError:
        print("reminders.json is empty or malformed. Returning an empty list.")
        return []
    except Exception as e:
        print(f"Error reading reminders: {e}")
        return []


# Function to log RSSI values to a file
def log_rssi_to_file(rssi, timestamp):
    """Log RSSI values to a file for troubleshooting."""
    log_file = "rssi_log.txt"
    try:
        with open(log_file, "a") as file:  # Open in append mode
            file.write(f"{timestamp}, RSSI: {rssi} dBm\n")
    except Exception as e:
        print(f"Error writing to log file: {e}")

# Function to send a notification via IFTTT
def send_ifttt_notification(reminder):
    # Sends a notification for a single reminder using IFTTT.
    
    # Formats the reminder sent through IFTT, pulling from the json.
    payload = {"value1": f"Reminder Alert: {reminder}"}
    try:
        response = requests.post(IFTTT_URL, json=payload)
        if response.status_code == 200:
            print(f"Notification sent successfully: {reminder}")
        else:
            print(f"Failed to send notification: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Error sending notification: {e}")

# Function to monitor BLE device
async def monitor_ble_device(device_address):
    # Monitor a BLE device's RSSI values.
    print(f"Monitoring connection to {device_address}...")
    while True:
        try:
            # Discover nearby BLE devices
            devices = await BleakScanner.discover()  
            found = False  # Track if the target device is found

            # Iterate through discovered devices
            for device in devices:
                if device.address.lower() == device_address.lower():
                    rssi = device.rssi  # Get RSSI directly from BLEDevice
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    print(f"{timestamp}, RSSI: {rssi} dBsm")
                    log_rssi_to_file(rssi, timestamp)  # Log the RSSI value

                    # Check if RSSI indicates the device is far away
                    if rssi <= -75:  # Threshold for certain vacinity.
                        print(f"{timestamp}, Device is too far away! Fetching reminders and sending notifications...")
                        log_rssi_to_file("Device out of range", timestamp)

                        # Fetch reminders
                        reminders = get_reminders()  # Load reminders from reminders.json

                        if reminders:
                            # Send each reminder as a separate notification
                            for reminder in reminders:
                                send_ifttt_notification(reminder)
                                time.sleep(1)  # Slight delay between notifications to avoid rate limits
                        else:
                            # Send a generic notification if no reminders exist
                            send_ifttt_notification("No reminders set. The user may have left the front door!")

                        return  # Stop monitoring after sending the notifications

                    found = True  # Mark device as found
                    break  # Exit loop once the target device is found

            # Handle case when the target device is not found
            if not found:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                print(f"{timestamp}, Device not found. Logging as disconnected.")
                log_rssi_to_file("Device not found", timestamp)

        except Exception as e:
            print(f"Error: {e}")
        
        # Wait before scanning again
        await asyncio.sleep(3)  # Scan every 5 seconds

# Main function
def main():
    """Main function to start BLE monitoring."""
    device_address = "A0:FB:C5:31:FC:CF"  # Replace with your Bluetooth device's MAC address
    asyncio.run(monitor_ble_device(device_address))

if __name__ == "__main__":
    main()
