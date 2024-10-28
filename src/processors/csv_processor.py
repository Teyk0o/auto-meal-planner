import re

import pandas as pd
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from src.utils.price_utils import clean_price

class CSVProcessor:
    """
    Process CSV files containing product data.
    Handles cleaning, deduplication, and validation of product data.
    """

    def __init__(self, input_file: str, output_file: Optional[str] = None):
        """
        Initialize the CSV processor.

        Args:
            input_file (str): Path to the input CSV file.
            output_file (str, optional): Path to the output CSV file.
        """
        self.input_file = Path(input_file)
        self.output_file = Path(output_file) if output_file else Path(input_file).parent / f"processed_{Path(input_file).name}"
        self.setup_logging()

    def setup_logging(self) -> None:
        """Configure logging for the processor."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
        )
        self.logger = logging.getLogger(__name__)

    def read_csv(self) -> pd.DataFrame:
        """
        Read the CSV file and return initial validation.

        Returns:
            pd.DataFrame: Raw dataframe from CSV.

        Raises:
            FileNotFoundError: If input file doesn't exist.
            pd.errors.EmptyDataError: If input file is empty.
        """
        if not self.input_file.exists():
            raise FileNotFoundError(f"Input file not found: {self.input_file}")

        df = pd.read_csv(
            self.input_file,
            sep=',',
            quotechar='"',
            doublequote=True,
            escapechar=None,
            encoding='utf-8'
        )

        if df.empty:
            raise pd.errors.EmptyDataError(f"Input file is empty: {self.input_file}")

        return df

    def clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean the dataframe by removing unnecessary columns and formatting data.

        Args:
            df (pd.DataFrame): Raw dataframe from CSV.

        Returns:
            pd.DataFrame: Cleaned dataframe.
        """
        # Remove specified columns
        columns_to_drop = ['web-scraper-order', 'web-scraper-start-url']
        df = df.drop(columns=columns_to_drop)

        # Debug: afficher quelques prix avant le nettoyage
        self.logger.info("Sample of original prices:")
        self.logger.info(df['product-price-unit'].head())

        # Clean product names
        df['product-name'] = df['product-name'].apply(self.clean_product_name)

        # Clean price columns
        df['product-price-unit'] = df['product-price-unit'].apply(clean_price)
        df['product-price-kilogram'] = df['product-price-kilogram'].apply(clean_price)

        # Debug: afficher les mêmes prix après le nettoyage
        self.logger.info("Sample of cleaned prices:")
        self.logger.info(df['product-price-unit'].head())

        # Strip whitespace from product name
        df['product-name'] = df['product-name'].str.strip()

        return df

    def clean_product_name(self, name: str) -> str:
        """
        Clean product name by removing extra spaces.

        Args:
            name (str): Product name to clean.

        Returns:
            str: Cleaned product name.
        """
        if not isinstance(name, str):
            return ""

        # Replace linebreaks with a single space
        name = name.replace('\n', ' ')

        # Remove extra spaces
        name = re.sub(r'\s+', ' ', name)

        # Remove leading/trailing spaces
        return name.strip()

    def remove_invalid_row(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove rows with missing prices and duplicates.

        Args:
            df (pd.DataFrame): Cleaned dataframe.

        Returns:
            pd.DataFrame: Cleaned dataframe with invalid rows removed.
        """
        # Remove rows with both prices missing
        df_filtered = df.dropna(subset=['product-price-unit', 'product-price-kilogram'], how='all')

        # Remove duplicates based on product name
        initial_rows = len(df_filtered)
        df_filtered = df_filtered.drop_duplicates(subset=['product-name'])
        duplicates_removed = initial_rows - len(df_filtered)

        if duplicates_removed > 0:
            self.logger.info(f"Removed {duplicates_removed} duplicate entries.")

        return df_filtered

    def get_statistics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate statistics about the processed data.

        Args:
            df (pd.DataFrame): Cleaned dataframe.

        Returns:
            Dict[str, Any]: Dictionary with statistics.
        """
        return {
            'total_products': len(df),
            'missing_unit_price': df['product-price-unit'].isna().sum(),
            'missing_kilogram_price': df['product-price-kilogram'].isna().sum(),
        }

    def process_csv(self) -> pd.DataFrame:
        """
        Process the CSV file according to specified requirements.

        Returns:
            pd.DataFrame: Processed dataframe.

        Raises:
            Various exceptions from read_csv()
        """
        try:
            # Read the CSV file
            self.logger.info(f"Reading CSV file: {self.input_file}")
            df = self.read_csv()

            # Clean data
            df = self.clean_dataframe(df)

            # Remove invalid rows
            df = self.remove_invalid_row(df)

            # Get statistics
            stats = self.get_statistics(df)
            self.logger.info(f"Processed {stats['total_products']} products with {stats['missing_unit_price']} missing unit prices and {stats['missing_kilogram_price']} missing kilogram prices.")

            # Save processed data
            df.to_csv(self.output_file, index=False)
            self.logger.info(f"Processed file saved to: {self.output_file}")

            return df

        except Exception as e:
            self.logger.error(f"Error processing CSV: {str(e)}")
            raise