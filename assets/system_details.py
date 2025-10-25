import platform
import psutil
import socket
import logging
from collections import defaultdict

# Helper function to convert bytes to a readable format (GB)
def convert_bytes_to_gb(bytes):
    return round(bytes / (1024**3), 2)

def get_system_details():
    details = defaultdict(lambda: "???")


    # =======================================================
    # 1. Operating System Details
    # =======================================================
    try:
        details['os_name'] = platform.system()
        details['release'] = platform.release()
        details['architecture'] = platform.machine()
        details['hostname'] = platform.node()
    except Exception as e:
        logging.warning(f"Could not retrieve OS details: {e}")

    # =======================================================
    # 2. System RAM (Memory)
    # =======================================================
    try:
        vmem = psutil.virtual_memory()
        details['total_ram_gb'] = convert_bytes_to_gb(vmem.total)
        details['used_ram_gb'] = convert_bytes_to_gb(vmem.used)
        details['free_ram_gb'] = convert_bytes_to_gb(vmem.free)
    except Exception as e:
        logging.warning(f"Could not retrieve RAM details: {e}")

    # =======================================================
    # 3. System Disk Memory (Storage)
    # =======================================================
    try:
        disk = psutil.disk_usage('/')
        details['total_disk_gb'] = convert_bytes_to_gb(disk.total)
        details['used_disk_gb'] = convert_bytes_to_gb(disk.used)
        details['free_disk_gb'] = convert_bytes_to_gb(disk.free)
    except Exception as e:
        logging.warning(f"Could not retrieve disk details: {e}")

    # =======================================================
    # 4. Internet Connection Status (Basic Check)
    # =======================================================
    host = "8.8.8.8"  # Google Public DNS
    port = 53
    timeout = 3 # seconds

    try:
        socket.setdefaulttimeout(timeout)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.close()
        details['internet_connection'] = 'Online'
    except OSError:
        details['internet_connection'] = 'Offline'
    
    return details

def log_system_details():
    system_details = get_system_details()
    # 1. Operating System Details
    logging.info("--- Operating System Details ---")
    logging.info(f"OS Name: {system_details['os_name']}")
    logging.info(f"Release: {system_details['release']}")
    logging.info(f"Architecture: {system_details['architecture']}")
    logging.info(f"Hostname: {system_details['hostname']}")

    logging.info("\n" + "="*50 + "\n") # Separator

    # 2. System RAM (Memory)
    logging.info("--- System RAM (Virtual Memory) ---")
    logging.info(f"Total RAM: {system_details['total_ram_gb']} GB")
    logging.info(f"Used RAM: {system_details['used_ram_gb']} GB")
    logging.info(f"Free RAM: {system_details['free_ram_gb']} GB")

    logging.info("\n" + "="*50 + "\n") # Separator

    # 3. System Disk Memory (Storage)
    logging.info("--- System Disk Memory (Storage) ---")
    logging.info(f"Total Disk: {system_details['total_disk_gb']} GB")
    logging.info(f"Used Disk: {system_details['used_disk_gb']} GB")
    logging.info(f"Free Disk: {system_details['free_disk_gb']} GB")

    logging.info("\n" + "="*50 + "\n") # Separator

    # 4. Internet Connection Status (Basic Check)
    if system_details['internet_connection'] == 'Online':
        logging.info("Internet Connection Status: **Online** (Successfully connected to an external host)")
    else:
        logging.warn("Internet Connection Status: **Offline** (Connection attempt failed)")

if __name__ == "__main__":
    # Add basic logging configuration to ensure the output is visible
    # and has a consistent format. The level is set to INFO to display
    # all the logging.info statements.
    # Configure basic logging
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    log_system_details()