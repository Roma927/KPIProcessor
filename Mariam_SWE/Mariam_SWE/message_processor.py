import json
from datetime import datetime
from interpreter import Interpreter
from database import insert_message


class MessageProcessor:
    def __init__(self, equation, interpreter):
        self.equation = equation
        self.interpreter = interpreter

    def process_message(self, message):
        """Process a message by evaluating its value based on config rules."""
        attr_value = message.get("value", None)

        # Check if value is None
        if attr_value is None:
            print(f"Missing 'value' in message: {message}")
            return

        try:
            # Attempt to convert the value to float
            numeric_value = float(attr_value)
            # Process as an arithmetic expression
            result = self.interpreter.evaluate(self.equation, numeric_value)
            print(f"Processing message: {attr_value} => Arithmetic Result: {result}")
        except ValueError:
            # If conversion fails, treat it as a string for regex evaluation
            regex = "Regex(ATTR, '^dog')"
            result = self.interpreter.evaluate(regex, attr_value)
            print(f"Processing message: {attr_value} => Regex Result: {result}")

        # Prepare output message with timestamp
        output_msg = self._prepare_output_message(message, result)
        insert_message(**output_msg)  # Insert into database
        return output_msg

    def _prepare_output_message(self, message, result):
        """Prepare the output message format."""
        return {
            "asset_id": message["asset_id"],
            "attribute_id": f"output_{message['attribute_id']}",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "value": result,
        }
