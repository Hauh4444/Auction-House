import json
from collections import defaultdict
from datetime import datetime

# Paths to input and output files
LOG_FILE = "login_activity.txt"
OUTPUT_FILE = "login_analytics.txt"

def load_log_data():
    log_data = []
    try:
        with open(LOG_FILE, "r") as f:
            for line in f:
                log_entry = parse_log_line(line.strip())
                if log_entry:
                    log_data.append(log_entry)
    except FileNotFoundError:
        print(f"{LOG_FILE} not found.")
    return log_data

def parse_log_line(line):
    if "logged in successfully" in line:
        timestamp_str = line.split(" - ")[0]
        username = line.split("User '")[1].split("'")[0]
        status = "success"
    elif "Failed login attempt for" in line:
        timestamp_str = line.split(" - ")[0]
        username = line.split("for '")[1].split("'")[0]
        status = "fail"
    else:
        return None

    try:
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S,%f")
    except ValueError:
        print(f"Skipping line: Invalid timestamp format {timestamp_str}")
        return None

    return {
        "timestamp": timestamp.isoformat(),
        "username": username,
        "status": status,
    }

def analyze_login_data(log_data):
    results = {
        "total_logins": 0,
        "total_successful_logins": 0,
        "total_failed_logins": 0,
        "login_by_user": defaultdict(int),
        "login_frequency_by_hour": defaultdict(int),
    }

    for entry in log_data:
        results["total_logins"] += 1
        if entry["status"] == "success":
            results["total_successful_logins"] += 1
        else:
            results["total_failed_logins"] += 1

        results["login_by_user"][entry["username"]] += 1
        hour = datetime.fromisoformat(entry["timestamp"]).hour
        results["login_frequency_by_hour"][hour] += 1

    return results

def write_analysis_results(analysis_results):
    with open(OUTPUT_FILE, "w") as f:
        f.write(f"Total Logins: {analysis_results['total_logins']}\n")
        f.write(f"Total Successful Logins: {analysis_results['total_successful_logins']}\n")
        f.write(f"Total Failed Logins: {analysis_results['total_failed_logins']}\n\n")

        f.write("Login Attempts by User:\n")
        for user, count in analysis_results["login_by_user"].items():
            f.write(f"{user}: {count} attempts\n")

        f.write("\nLogin Frequency by Hour:\n")
        for hour, count in sorted(analysis_results["login_frequency_by_hour"].items()):
            f.write(f"Hour {hour}: {count} login attempts\n")

    print(f"Analysis results written to {OUTPUT_FILE}")

def print_text_graph(title, data, unit):
    if not data:
        print(f"{title}: No data to display.\n")
        return

    print(f"\n{title}")
    print("-" * len(title))

    max_val = max(data.values())
    scale = 50
    for key, val in sorted(data.items()):
        bar = "#" * int((val / max_val) * scale) if max_val > 0 else ""
        print(f"{str(key):<15}: {bar} ({val} {unit})")
    print()

if __name__ == "__main__":
    log_data = load_log_data()

    if log_data:
        analysis_results = analyze_login_data(log_data)
        write_analysis_results(analysis_results)

        print_text_graph("Login Frequency by Hour", analysis_results["login_frequency_by_hour"], "attempts")
        print_text_graph("Login Attempts by User", analysis_results["login_by_user"], "attempts")
        print_text_graph("Login Success/Failure Ratio", {
            "Successful Logins": analysis_results["total_successful_logins"],
            "Failed Logins": analysis_results["total_failed_logins"]
        }, "logins")
    else:
        print("No data found to analyze.")
