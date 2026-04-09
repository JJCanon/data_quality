#Libraries
import pandas as pd


# Functions to verify the uniqueness
def evaluate_uniqueness(serie: pd.Series, field: str, table: str) -> dict:
    serie_clean = serie.dropna()
    total_records = len(serie_clean)

    unique_records = 0
    percentage = 0

    if total_records > 0:
        duplicated_mask = serie_clean.duplicated(keep=False)
        unique_records = (~duplicated_mask).sum()
        percentage = round((unique_records / total_records) * 100, 2)

    return {
        "campo": field,
        "tabla": table,
        "dimension": "Unicidad",
        "registros_totales": total_records,
        "registros_unicos": unique_records,
        "porcentaje": percentage
    }