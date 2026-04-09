# Libraries
import pandas as pd
from datetime import datetime
from sqlalchemy import text

# internal imports
from results.export_excel import export_to_excel

# Functions
# This function get and calculate the data quality in the database
def transform_data(engine):

   # Query to extract the results 
    select_query = text(
        """
        SELECT 
            tb.tabla,
            fld.campo,
            dm.dimension,
            result.score,
            ejec.fecha_ejecucion
        FROM dbo.resultado result
        JOIN dbo.campo fld
            ON fld.id = result.id_campo
        JOIN dbo.tabla tb
            ON fld.id_tabla = tb.id
        JOIN dbo.dimension dm
            ON result.id_dimension = dm.id
        JOIN dbo.ejecucion ejec
            ON result.id_ejecucion = ejec.id
        WHERE ejec.id = (
            SELECT MAX(id)
            FROM dbo.ejecucion
        )
        """
    )
    data = None

    with engine.connect() as connection:
        data = connection.execute(select_query).fetchall()

    print("############## CALCULATE QUALITY ######################")
    
    data_qualty = calculate_point(data=data)

    print("############## EXPORT EXCEL ###############")
    
    export_to_excel(data=data, data_quality=data_qualty, file_path="data_quality_report.xlsx")



# Auxiliary functions
## This function return the score of the data quality in general
def calculate_point(data:pd.DataFrame, threshold: float = 85.0)->float:

    # Transform in a dataframe the tuple list
    if not isinstance(data, pd.DataFrame):
        df = pd.DataFrame(data, columns=["tabla", "campo", "dimension", "score", "fecha_ejecucion"])
    else:
        df = data.copy()

    # if field has more than 85% score, get 1 point, else 0
    
    df["point"] = (df["score"] > threshold).astype(int)

    data_quality = round((df["point"].sum() / len(df["point"])) * 100, 2)

    return float(data_quality)
