# Log Monitor

A log monitoring application based on Python, that reads a CSV log file, calculates job durations, and logs warnings or errors if job durations exceed defined thresholds.

---

## How does it work?

- Parses CSV-formatted log files with timestamped job events.
- Matches jobs by unique PID to calculate execution duration.
- Logs a:
- **WARNING** if a job takes more than 5 minutes.
- **ERROR** if a job takes more than 10 minutes.
- Outputs alerts to `alerts.log`.

---

## How to run?

0. The app requires Python 3.x
1. Place your log entries in a file named `logs.log` within the test/data directory.
2. Run the script:
    python logMonitor.py

---

## Example output

[WARNING] Job 'scheduled task 1' (PID 71766) ran for 0:05:47 (Start: 11:45:04, End: 11:50:51)
[ERROR] Job 'background job 2' (PID 81258) ran for 0:14:46 (Start: 11:36:58, End: 11:51:44)

---

## Running Tests

Go in root directory then run:
    python -m unittest test.testLogMonitor
