# Libraries
from __future__ import annotations
import re
import pandas as pd


# Internal imports



# Functions
## This function calculate the consistency between a foreign key and its reference
def calculate_consistency(serie: pd.Series, serie_key:pd.Series, field:str, table:str)->dict:
    clean_serie = _drop_nulls(serie)
    total_records = len(clean_serie)
    valid_records = 0
    percentage = 0
    
    if total_records > 0:
        valid_records = clean_serie.isin(serie_key).sum()
        percentage = round((valid_records/total_records)*100,2)


    return {
            "campo": field,
            "tabla": table,
            "dimension": "Consistencia",
            "registros_totales": total_records,
            "registros_validos": valid_records,
            "porcentaje": percentage
    }





# Tools

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


def consistency_relation(field:str,table:str)->dict:
    field_selected = ""
    table_selected = ""
    if field == 'cod_tipo_doc' and table == 'mpersona':
        field_selected = "cod_tipo_doc"
        table_selected = "ttipo_doc"
    if field == "cod_pais_nac" and table == 'mpersona':
        field_selected = "cod_pais"
        table_selected = "tpais"
    if field == "cod_dpto_nac" and table == "mpersona":
        field_selected = "cod_dpto"
        table_selected = "tdpto"
    if field == "cod_municipio_nac" and table == "mpersona":
        field_selected = "cod_municipio"
        table_selected = "tmunicipio"
    if field == "cod_est_civil" and table == "mpersona":
        field_selected = "cod_est_civil"
        table_selected = "test_civil"
    if field == "cod_pais" and (table == "tdpto" or table == "tmunicipio" or table == "mpersona_dir"):
        field_selected = "cod_pais"
        table_selected = "tpais"
    if field == "cod_dpto" and (table == "tmunicipio" or table == "mpersona_dir"):
        field_selected = "cod_dpto"
        table_selected = "tdpto"
    if field == "id_persona" and (table == "mpersona_telef" or table == "mpersona_sarlaft" or table == "mpersona_dir"):
        field_selected = "id_persona"
        table_selected = "mpersona"
    if field == "cod_tipo_telef" and table == "mpersona_telef":
        field_selected = "cod_tipo_telef"
        table_selected = "ttipo_telef"
    if field == "cod_municipio" and table == "mpersona_dir":
        field_selected = "cod_municipio"
        table_selected = "tmunicipio"

    return {
        "field": field_selected,
        "table": table_selected
    }