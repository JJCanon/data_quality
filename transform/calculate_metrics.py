# Libraries

from __future__ import annotations

from datetime import datetime
from typing import Dict, List, TypedDict

import pandas as pd

# internal imports
from config.load_config import load_yaml
from transform.rules.completitud import evaluate_completeness
from transform.rules.validez import (
    evaluate_alphabetic_validity,
    evaluate_alphanumeric_validity,
    evaluate_numeric_validity,
    evaluate_positive_numeric_validity,
    evaluate_datetime_validity,
    evaluate_contact_validity
)
from transform.rules.unicidad import evaluate_uniqueness
from transform.rules.consistencia import consistency_relation, calculate_consistency


# Main functions

## to calculate metrics of each field
def calculate_metrics(tables: Dict[str, pd.DataFrame]) -> List[dict]:

    # getting field specifications
    specs = get_fields_specs()
    

    results: List[dict] = []

    for spec in specs:
        table = spec["tabla"]
        field = spec["campo"]
        tipo_validez = spec["tipo_validez"]
        dimensions = spec["dimensiones"]

        # print('\n', 'tabla: ', table,'campo: ',field,'\n')

        df = tables.get(table)
        if (df is None) or (field not in df):
            for dimension in dimensions:
                results.append({
                    "campo": field,
                    "tabla":table,
                    "dimension": dimension,
                    "porcentaje": None,
                    "status": "MISSING_FIELD"
                })
            continue
    

        for dimension in dimensions:
            dim_norm = dimension.strip().lower()

            #-------------- COMPLETITUD ---------------#
            if dim_norm == "completitud":

                evaluation = evaluate_completeness(df[field], field=field, table=table)
                results.append(_normalize_result(evaluation,field, table, dim_norm, "OK"))


            #-------------- VALIDEZ ---------------#
            elif dim_norm == "validez":
                
                evaluator = VALIDEZ_EVALUATORS.get(tipo_validez)
                
                if evaluator is None:
                    results.append({
                        "campo": field,
                        "tabla": table,
                        "dimension": dim_norm,
                        "porcentaje": None,
                        "status": f"UNKNOWN_TIPO_VALIDEZ:{tipo_validez}",
                    })
                    continue
                
                evaluation = evaluator(df[field], field=field, table=table)
                results.append(_normalize_result(evaluation, field, table, dim_norm, "OK"))

            #-------------- UNICICAD ---------------#
            elif dim_norm == "unicidad":
                
                evaluation = evaluate_uniqueness(df[field],field=field,table=table)
                results.append(_normalize_result(evaluation,field,table,dim_norm,"OK"))

            #-------------- PRECISION ---------------#
            elif dim_norm == "precision":
                continue

            #-------------- CONSISTENCIA ---------------#
            elif dim_norm == "consistencia":
                consistency = consistency_relation(field=field,table=table)
                # print(field,table,"\n")
                # print(f"Buscando tabla: '{consistency['table']}' en keys: {list(tables.keys())}")
                consistency_df = tables.get(consistency['table'])
                evaluation = calculate_consistency(df[field],consistency_df[consistency['field']],field=field,table=table)
                results.append(_normalize_result(evaluation,field,table,dim_norm,"OK"))

            #-------------- OPORTUNIDAD ---------------#
            elif dim_norm == "oportunidad":
                continue


    return results


# Tools

## to extract from parameters the necesary information
class ValiditySpec(TypedDict):
    tabla: str
    campo: str
    tipo_validez: str
    dimensiones: List[str]

## read parameters and return the specifications
def get_fields_specs() -> List[ValiditySpec]:
    
    
    config = load_yaml()
    
    transform_tables = (config.get("transform") or {}).get("tables") or {}

    specs: List[ValiditySpec] = []

    for table, table_config in transform_tables.items():
        fields = (table_config or {}).get("fields") or {}

        for field, field_config in fields.items():
            dims = (field_config or {}).get("dimensiones") or []
            
            tipo_validez = (field_config or {}).get("tipo_validez") if "validez" in dims else None
            
            
            consistencia = (field_config or {}).get("consistencia") if "consistencia" in dims else None

            specs.append({
                    "campo": str(field),
                    "tabla": str(table),
                    "dimensiones": [str(d) for d in dims],
                    "tipo_validez": str(tipo_validez),
                    "consistencia": str(consistencia)
                })
    

    # print(specs)
    return specs

## dictionary to evaluate type of validity
VALIDEZ_EVALUATORS = {
    "Alfabético": evaluate_alphabetic_validity,
    "Alfanumérico": evaluate_alphanumeric_validity,
    "Numérico": evaluate_numeric_validity,
    "Numérico positivo": evaluate_positive_numeric_validity,
    "Fecha (DateTime)": evaluate_datetime_validity,
    "Contacto": evaluate_contact_validity,
}

def _normalize_result(raw: dict, campo: str, tabla: str, dimension: str, status: str) -> dict:

    porcentaje = raw.get("porcentaje")
    return {
        "campo": campo,
        "tabla": tabla,
        "dimension": dimension,
        "porcentaje": float(porcentaje),
        "status": status,
    }
