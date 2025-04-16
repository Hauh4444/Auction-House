import os
from datetime import datetime

LOG_FILE = os.path.join(os.path.dirname(__file__), 'login_activity.txt')

def parse_log_file():
    """
    Parses the login_activity.txt file and extracts relevant data.
    
    Returns:
        list: A list of dictionaries containing login activity data.
    """
    log_data = []
    
    # Open and read the log file
    with open(LOG_FILE, 'r') as f:
        for line in f:
            timestamp_str, message = line.split(" - ", 1)
            timestamp = datetime.fromisoformat(timestamp_str)
            
            # Extract status and username from the message
            if "logged in successfully" in message:
                status = "success"
                username = message.split("'")[1]
            elif "Failed login attempt" in message:
                status = "fail"
                username = message.split("'")[1]
            else:
                continue
            
            log_data.append({"timestamp": timestamp, "username": username, "status": status})

    return log_data

def count_logins_by_user(log_data):
    """
    Count the number of successful logins per user.
    
    Args:
        log_data (list): List of parsed log entries.
        
    Returns:
        dict: Dictionary with usernames as keys and login counts as values.
    """
    login_counts = {}
    for entry in log_data:
        if entry['status'] == 'success':
            username = entry['username']
            login_counts[username] = login_counts.get(username, 0) + 1
    return login_counts

def count_failed_logins_by_user(log_data):
    """
    Count the number of failed login attempts per user.
    
    Args:
        log_data (list): List of parsed log entries.
        
    Returns:
        dict: Dictionary with usernames as keys and failed login counts as values.
    """
    failed_counts = {}
    for entry in log_data:
        if entry['status'] == 'fail':
            username = entry['username']
            failed_counts[username] = failed_counts.get(username, 0) + 1
    return failed_counts

def count_logins_by_time(log_data):
    """
    Count the number of logins by hour of the day.
    
    Args:
        log_data (list): List of parsed log entries.
        
    Returns:
        dict: Dictionary with hour of the day as keys and login counts as values.
    """
    logins_by_hour = {}
    for entry in log_data:
        hour = entry['timestamp'].hour
        logins_by_hour[hour] = logins_by_hour.get(hour, 0) + 1
    return logins_by_hour
