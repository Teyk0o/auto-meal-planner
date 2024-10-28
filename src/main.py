from src.processors.csv_processor import CSVProcessor
from pathlib import Path
import logging
import os

def main():
    """Main entry point for the application."""
    try:
        # Get the project root directory
        PROJECT_ROOT = get_project_root()

        # Build the absolute path to files
        input_path = PROJECT_ROOT / "data" / "raw" / "input.csv"
        output_path = PROJECT_ROOT / "data" / "processed" / "output.csv"

        # Check if the output directory exists, if not create it
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Initialize the CSV processor
        processor = CSVProcessor(
            input_file=str(input_path),
            output_file=str(output_path)
        )

        # Process the CSV
        df = processor.process_csv()

        print(f"Successfully processed {len(df)} products.")

    except Exception as e:
        logging.error(f"Error in main: {str(e)}")
        raise

def get_project_root() -> Path:
    """Returns project root folder."""
    return Path(__file__).parent.parent

if __name__ == "__main__":
    main()