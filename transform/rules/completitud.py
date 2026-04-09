#Libraries
import pandas as pd

# function to verify the completeness
def evaluate_completeness(serie: pd.Series, field:str, table:str) -> dict:
    total_records = len(serie)
    valid_records = 0
    percentage = 0

    if total_records > 0:
        valid_records = serie.notna().sum()
        percentage = round((valid_records / total_records)*100,2)
    
    
    return {
        "campo":field,
        "tabla":table,
        "dimension":"Completitud",
        "registros_totales":total_records,
        "registros_validos":valid_records,
        "porcentaje":percentage
    }