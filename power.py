import psutil
import datetime
import threading
import csv
import time
from colorama import Fore, Style

power_data = []
csv_file_path = 'power_log.csv'
txt_file_path = 'power_log.txt'

def monitor_power():
    global power_data
    while True:
        power = psutil.sensors_battery()
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        power_data.append((timestamp, power.power_plugged))
        # Save log to .csv and .txt files every 60 seconds
        save_log(power_data)
        # Print log message
        print_log(timestamp, power.power_plugged)
        # Sleep for 60 seconds before checking again
        time.sleep(60)

def save_log(data):
    with open(csv_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Time', 'Plugged'])
        for entry in data:
            plugged_status = 'Yes' if entry[1] else 'No'
            csv_writer.writerow([entry[0], plugged_status])
    
    with open(txt_file_path, 'w') as txt_file:
        for entry in data:
            plugged_status = 'Plugged In' if entry[1] else 'Unplugged'
            txt_file.write(f"{entry[0]} - {plugged_status}\n")

def print_log(timestamp, plugged_in):
    if plugged_in:
        print(f"[{Fore.GREEN}+{Style.RESET_ALL}] {timestamp} {Fore.GREEN}Plugged In{Style.RESET_ALL}")
    else:
        print(f"[{Fore.RED}-{Style.RESET_ALL}] {timestamp} {Fore.RED}Plugged Out{Style.RESET_ALL}")


if __name__ == '__main__':
    from colorama import init
    init(autoreset=True)  # Initialize Colorama to reset colors automatically
    # Start monitoring power status in a separate thread
    power_thread = threading.Thread(target=monitor_power)
    power_thread.start()
