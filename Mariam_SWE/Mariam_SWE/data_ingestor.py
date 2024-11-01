import json
import time
from message_processor import MessageProcessor

import json

import json


class DataIngestor:
    def __init__(self, file_path, processor):
        self.file_path = file_path
        self.processor = processor

    def start_ingestion(self):
        with open(self.file_path, "r") as file:
            for line in file:
                try:
                    # Parse each line as JSON
                    message = json.loads(line.strip())
                    self.processor.process_message(message)
                except json.JSONDecodeError:
                    print(f"Error decoding JSON: {line.strip()}")
                except Exception as e:
                    print(f"Error processing line '{line.strip()}': {e}")
                time.sleep(5)
    def _parse_message(self, line):
        """Parse a JSON message line from the file."""
        try:
            return json.loads(line.strip())
        except json.JSONDecodeError:
            print(f"Invalid message format: {line}")
            return None
