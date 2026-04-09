# Libraries
import os
import pandas as pd
from pathlib import Path

# internal imports
from config.db_connections import get_sqlserver_engine

# function to load database query in a Dataframe
def extract_table(query_file:str)-> pd.DataFrame:

    # read SQL file
    query = Path(query_file).read_text(encoding='utf-8')

    # Get engine
    engine = get_sqlserver_engine()

    # Execute query
    df = pd.read_sql(query,engine)

    return df