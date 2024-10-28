import pytest
import pandas as pd
from pathlib import Path
from src.processors.csv_processor import CSVProcessor


@pytest.fixture
def sample_data():
    """Create a sample DataFrame for testing."""
    return pd.DataFrame({
        'web-scraper-order': ['1', '2', '3'],
        'web-scraper-start-url': ['url1', 'url2', 'url3'],
        'product-name': [
            'Café capsules L\'OR Espresso                      Or Absolu n°9 - x10 - 52g',
            'Capsules Café Royal                      Espresso - x36 - 190g',
            'Capsules café Plantation                      Cappuccino - 2x8 - 166g'
        ],
        'product-price-unit': [
            '2                     €                    ,89',
            '9                     €                    ,39',
            '2                     €                    ,99'
        ],
        'product-price-kilogram': [
            '55,58 € / kg',
            '49,42 € / kg',
            '18,01 € / kg'
        ],
        'product-origin': ['', '', '']
    })


def test_csv_processor_initialization(tmp_path):
    """Test the initialization of the CSVProcessor."""
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"
    processor = CSVProcessor(str(input_file), str(output_file))
    assert processor.input_file == input_file
    assert processor.output_file == output_file


def test_clean_dataframe(sample_data):
    """Test the cleaning of the DataFrame."""
    processor = CSVProcessor("dummy.csv")
    cleaned_df = processor.clean_dataframe(sample_data)

    # Verify that unnecessary columns have been removed
    assert 'web-scraper-order' not in cleaned_df.columns
    assert 'web-scraper-start-url' not in cleaned_df.columns

    # Verify that the product prices have been cleaned
    assert cleaned_df['product-price-unit'].iloc[0] == 2.89
    assert cleaned_df['product-price-kilogram'].iloc[0] == 55.58

    # Verify that the product names have been cleaned
    assert "  " not in cleaned_df['product-name'].iloc[0]


def test_remove_invalid_rows(sample_data):
    """Test the removal of invalid rows."""
    processor = CSVProcessor("dummy.csv")

    # Add an invalid row
    sample_data.loc[len(sample_data)] = ['4', 'url4', 'Invalid Product', None, None, '']

    cleaned_df = processor.clean_dataframe(sample_data)
    filtered_df = processor.remove_invalid_row(cleaned_df)

    # Verify that the invalid row has been removed
    assert len(filtered_df) < len(sample_data)

    # Verify that have not both prices missing
    assert not filtered_df[filtered_df['product-price-unit'].isna() &
                           filtered_df['product-price-kilogram'].isna()].any().any()


def test_process_full_csv(tmp_path, sample_data):
    """Test the full processing of a CSV file."""
    # Create a sample CSV file
    input_file = tmp_path / "input.csv"
    output_file = tmp_path / "output.csv"
    sample_data.to_csv(input_file, index=False)

    # Treat the CSV file
    processor = CSVProcessor(str(input_file), str(output_file))
    result_df = processor.process_csv()

    # Verify that the output file exists and contains valid data
    assert len(result_df) > 0
    assert 'web-scraper-order' not in result_df.columns
    assert result_df['product-price-unit'].notna().all()
    assert result_df['product-price-kilogram'].notna().all()
    assert output_file.exists()