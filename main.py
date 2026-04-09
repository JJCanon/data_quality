#Libraries
import pandas as pd
import matplotlib.pyplot as plt
from typing import List

# Local imports
from extract.extract_all import extract_all_tables
from transform.calculate_metrics import calculate_metrics
from load.load_results import load_results
from transform.calculate_score import transform_data



def main():
    # EXTRACT
    print("################### EXTRACT ########################")
    tables = extract_all_tables()

    print("\nExtracted tables:")
    for name in tables.keys():
        print(f"table: {name}")
    print()


    # TRANSFORM
    print("################### Transform ########################")
    metrics = calculate_metrics(tables)

    print()


    # LOAD
    print("################### LOAD ########################")
    engine = load_results(metrics)
    print()


    # TRANSFORM
    print("################### Transform ########################")
    transform_data(engine)

    print()
    


# Main function
if __name__ == "__main__":
    main()
