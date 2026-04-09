# Libraries
from pathlib import Path
from config.load_config import load_yaml

# Internal imports
from extract.extract_table import extract_table


# function to extract each table from database
def extract_all_tables():

    config = load_yaml()
    base_path = Path("extract/queries")

    tables = {
        name: base_path / filename for name, filename in config['TABLES'].items()
    }

    data = {}

    for table_name, query_file in tables.items():

        print(f'Extracting {table_name}...')

        try:
            df = extract_table(query_file)
            data[table_name] = df
            print(f'{table_name}: {len(df)} rows')

        except Exception as e:
            print(f'Error extracting {table_name}: {e}')

    print("Extraction phase completed ✅")

    return data
