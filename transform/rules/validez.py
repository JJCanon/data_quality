# Libraries
from __future__ import annotations
import re
import pandas as pd

# Internal imports

# Functions
## to validate alphabetic fields
def evaluate_alphabetic_validity(serie: pd.Series, field:str, table:str)-> dict:
    clean_serie = _drop_nulls(serie)
    total_records = len(clean_serie)
    valid_records = 0
    percentage = 0
    if total_records > 0:
        valid_mask = clean_serie.astype("string").str.match(_ALPHA_REGEX, na=False)
        valid_records=valid_mask.sum()
        percentage = round((valid_records/total_records)*100,2)
    
    return{
            "campo": field,
            "tabla": table,
            "dimension": "Validez",
            "registros_totales": total_records,
            "registros_validos": valid_records,
            "porcentaje": percentage
        }

## to validate alphanumeric fields
def evaluate_alphanumeric_validity(serie: pd.Series, field:str, table:str)-> dict:
    clean_serie = _drop_nulls(serie)
    total_records = len(clean_serie)
    valid_records = 0
    percentage = 0
    if total_records > 0:
        valid_mask = clean_serie.astype("string").str.match(_ALNUM_REGEX, na=False)
        valid_records = valid_mask.sum()
        percentage = round((valid_records/total_records)*100,2)

    return{
            "campo": field,
            "tabla": table,
            "dimension": "Validez",
            "registros_totales": total_records,
            "registros_validos": valid_records,
            "porcentaje": percentage
        } 

## to evaluate numeric fields
def evaluate_numeric_validity(serie: pd.Series, field:str, table: str)->dict:
    clean_serie = _drop_nulls(serie)
    total_records = len(clean_serie)
    valid_records = 0
    percentage = 0

    if total_records > 0:
        numeric_records = pd.to_numeric(clean_serie, errors='coerce')
        valid_mask = numeric_records.notna()
        valid_records = valid_mask.sum()
        percentage = round((valid_records/total_records)*100,2)

    return{
            "campo": field,
            "tabla": table,
            "dimension": "Validez",
            "registros_totales": total_records,
            "registros_validos": valid_records,
            "porcentaje": percentage
        } 

## to validate positives numeric fields
def evaluate_positive_numeric_validity(serie:pd.Series,field:str,table:str)-> dict:
    clean_serie = _drop_nulls(serie)
    total_records = len(clean_serie)
    valid_records = 0
    percentage = 0

    if total_records > 0:
        numeric_records = pd.to_numeric(clean_serie, errors='coerce')
        valid_records = (numeric_records.notna()) & (numeric_records >= 0)
        valid_positive_records = valid_records.sum()
        percentage = round((valid_positive_records/total_records)*100,2)
    
    return{
            "campo": field,
            "tabla": table,
            "dimension": "Validez",
            "registros_totales": total_records,
            "registros_validos": valid_positive_records,
            "porcentaje": percentage
        }     

## to validate datetime AAAA-MM-DD HH:MM:SS
def evaluate_datetime_validity(serie:pd.Series, field:str, table:str):
    clean_serie = _drop_nulls(serie)
    total_records = len(clean_serie)
    valid_records = 0
    percentage = 0

    if total_records > 0:
        date_records = pd.to_datetime(clean_serie,format='%Y-%m-%d %H:%M:%S', errors='coerce')
        valid_mask = date_records.notna()
        valid_records = valid_mask.sum()
        percentage = round((valid_records/total_records)*100,2)

    return{
            "campo": field,
            "tabla": table,
            "dimension": "Validez",
            "registros_totales": total_records,
            "registros_validos": valid_records,
            "porcentaje": percentage
        }   

## to validate contact fields (numbers and emails)
def evaluate_contact_validity(serie: pd.Series, field: str, table: str) -> dict:
    clean_serie = _drop_nulls(serie)
    total_records = len(clean_serie)
    valid_records = 0
    percentage = 0
    if total_records > 0:
        str_serie = clean_serie.astype("string")
        valid_mask = (
            str_serie.str.match(_ALNUM_REGEX, na=False) |
            str_serie.str.match(_EMAIL_REGEX, na=False)
        )
        valid_records = valid_mask.sum()
        percentage = round((valid_records / total_records) * 100, 2)

    return {
        "campo": field,
        "tabla": table,
        "dimension": "Validez",
        "registros_totales": total_records,
        "registros_validos": valid_records,
        "porcentaje": percentage
    }

# Tools

## Patterns
_ALPHA_REGEX = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ\s]+$")
_ALNUM_REGEX = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9\s\-\._/#]+$")
_EMAIL_REGEX = re.compile(r"^[\w\.\+\-]+@([\w\-]+\.)+[a-zA-Z]{2,}$")

##  this function help to not evaluate null values dropping it
def _drop_nulls(series:pd.Series) -> pd.Series:
    # nulls
    null_mask = series.isna()

    # if serie is string type
    if pd.api.types.is_string_dtype(series) or series.dtype == "object":
        blank_mask = series.astype("string").str.strip().eq("")
        null_mask = null_mask | blank_mask
    
    # return serie without nulls
    return series[~null_mask].reset_index(drop=True)


