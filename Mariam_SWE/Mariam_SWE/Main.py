from data_ingestor import DataIngestor
from interpreter import Interpreter
from database import create_table
from message_processor import MessageProcessor
import json


def main():
    create_table()

    # Load configuration
    config_path = "E:\\Mariam_SWE\\Mariam_SWE\\config.json"
    with open(config_path, "r") as config_file:
        config = json.load(config_file)

    # Get the equation from config
    equation = config.get("equation", "ATTR + 50 * (ATTR / 10)")

    messages_file = "E:\\Mariam_SWE\\Mariam_SWE\\messege.txt"

    interpreter = Interpreter()

    processor = MessageProcessor(equation=equation, interpreter=interpreter)
    ingestor = DataIngestor(messages_file, processor)

    ingestor.start_ingestion()


if __name__ == "__main__":
    main()
