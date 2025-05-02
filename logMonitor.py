import csv
from datetime import datetime, timedelta

# File paths
LOG_FILE = 'logs.log'
ALERT_LOG_FILE = 'alerts.log'

# Alert thresholds
WARNING_THRESHOLD = timedelta(minutes=5)
ERROR_THRESHOLD = timedelta(minutes=10)
VALID_STATUSES = {'START', 'END'}

def parse_log_file(file_path):
    jobs = {}  # Track ongoing jobs by PID
    results = []  # Completed job entries

    # Keep track of the row number as well for better error reporting
    with open(file_path, 'r') as file:
        reader = csv.reader(file)

        for row_num, row in enumerate(reader, start=1):
            try:
                if len(row) != 4:
                    raise ValueError("Expected 4 fields")
                
                # Clean whitespace and unpack into vars
                timestamp_str, job_desc, status, pid = [item.strip() for item in row]

                # Validate status
                if status not in VALID_STATUSES:
                    print(f"[WARNING] Row {row_num}: Invalid status '{status}', skipping.")
                    continue

                # Parse time
                timestamp = datetime.strptime(timestamp_str, '%H:%M:%S')

                # Initialize job tracking if new
                if pid not in jobs:
                    jobs[pid] = {'description': job_desc}

                jobs[pid][status] = timestamp

                # If job has both START and END, process it
                if 'START' in jobs[pid] and 'END' in jobs[pid]:
                    start = jobs[pid]['START']
                    end = jobs[pid]['END']

                    # Handle rollover if end < start
                    if end < start:
                        end += timedelta(days=1)

                    duration = end - start

                    # Determine alert level
                    if duration > ERROR_THRESHOLD:
                        log_level = 'ERROR'
                    elif duration > WARNING_THRESHOLD:
                        log_level = 'WARNING'
                    else:
                        log_level = None

                    results.append({
                        'pid': pid,
                        'description': job_desc,
                        'start': start,
                        'end': end,
                        'duration': duration,
                        'log_level': log_level
                    })

                    # Cleanup
                    del jobs[pid]

            except Exception as e:
                print(f"[WARNING] Row {row_num}: Skipping malformed row {row} - {e}")

    return results

def write_alerts_to_file(results, output_file):
    with open(output_file, 'w') as f:
        for entry in results:
            if entry['log_level']:
                log_line = (
                    f"[{entry['log_level']}] Job '{entry['description']}' (PID {entry['pid']}) "
                    f"ran for {entry['duration']} (Start: {entry['start'].time()}, End: {entry['end'].time()})\n"
                )
                f.write(log_line)

if __name__ == "__main__":
    report = parse_log_file(LOG_FILE)
    write_alerts_to_file(report, ALERT_LOG_FILE)
    print(f"Alerts written to {ALERT_LOG_FILE}")
