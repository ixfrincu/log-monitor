import unittest
from io import StringIO
import tempfile
from logMonitor import parse_log_file

class TestLogParsing(unittest.TestCase):

    def test_warning_and_error_detection(self):
        log_data = """12:00:00, scheduled task 1, START, 101
                      12:06:00, scheduled task 1, END, 101
                      12:10:00, scheduled task 2, START, 102
                      12:25:00, scheduled task 2, END, 102"""

        # Write the sample log data to a temporary file
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
            f.write(log_data)
            f.seek(0)
            # Call the parser with the temp file path
            results = parse_log_file(f.name)

        # Extract the log levels for the processed jobs and check that the correct alerts were generated
        log_levels = [r['log_level'] for r in results]
        self.assertEqual(log_levels, ['WARNING', 'ERROR'])

    def test_ignores_malformed_row(self):
        bad_log = "12:00:00, scheduled task 3, START\n"  # Missing PID
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
            f.write(bad_log)
            f.seek(0)
            results = parse_log_file(f.name)

        # Assert that no results are returned for invalid input
        self.assertEqual(results, [])

if __name__ == "__main__":
    unittest.main()
