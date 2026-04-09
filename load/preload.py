# Libraries
import pandas as pd
from datetime import datetime
from sqlalchemy import text

# Internal imports
from config.db_connections import get_sqlserver_engine_results

# Functions
## this function set the data in the correct structure to be loaded
def preload_data(metrics: list[dict])-> dict:

    engine = get_sqlserver_engine_results()

    rows_to_insert = []

    with engine.begin() as connection:
        
        # create ejecution register
        ejecution_date = datetime.now()

        insert_exec = text(
            """
            INSERT INTO dbo.ejecucion (fecha_ejecucion, fuente, notas)
            OUTPUT INSERTED.id
            VALUES (:fecha,:fuente,:notas)
            """
        )

        exec_result = connection.execute(insert_exec,{
            "fecha": ejecution_date,
            "fuente": "persefone/alfa",
            "notas": "testing"
        })

        id_ejecucion = exec_result.fetchone()[0]

        # print(f"  [Ejecucion] id={id_ejecucion}  fecha={ejecution_date:%Y-%m-%d %H:%M:%S}")

        # Resolve catalog and create rows
        # Caching to not repeat queries into the same preload
        table_cache: dict[str,int] = {}
        field_cache: dict[tuple,int] = {}
        dimension_cache: dict[str,int] = {}

        for metric in metrics:
            table_name = metric["tabla"]
            field_name = metric["campo"]
            dimension_name = metric["dimension"]
            score = metric["porcentaje"]

            # table
            if table_name not in table_cache:
                table_id = get_or_create_table(connection=connection,table_name=table_name)
                table_cache[table_name] = table_id
                # print(f"  [Tabla]     '{table_name}' -> id={table_id}")
            table_id = table_cache[table_name]

            # field
            field_key = (table_id,field_name)
            if field_key not in field_cache:
                field_id = get_or_create_field(connection=connection,table_id=table_id,field_name=field_name)
                field_cache[field_key] = field_id
                # print(f"  [Campo]     '{field_name}' (tabla_id={table_id}) -> id={field_id}")
            field_id = field_cache[field_key]

            # dimension
            if dimension_name not in dimension_cache:
                dimension_id = get_or_create_dimension(connection=connection,dimension_name=dimension_name)
                dimension_cache[dimension_name] = dimension_id
                # print(f"  [Dimension] '{dimension_name}' -> id={dimension_id}")
            dimension_id = dimension_cache[dimension_name]

            rows_to_insert.append({
                "id_campo": field_id,
                "id_dimension": dimension_id,
                "score": float(score)
            })

    print(f"\n  Preload completado: {len(rows_to_insert)} filas listas para insertar.")
 
    return {
        "engine":       engine,
        "id_ejecucion": id_ejecucion,
        "rows":         rows_to_insert,
    }





## Auxiliary functions
"""
This function return table id in the database data_process in the table "table" 
if the table name is not in the database, insert a new one and return its index
"""
def get_or_create_table(connection, table_name:str) -> int:

    # search table id
    select_sql = text("SELECT id FROM dbo.tabla WHERE tabla = :table_name")
    row = connection.execute(select_sql,{"table_name":table_name}).fetchone()

    # if the table exist, return id
    if row:
        return row[0]
    
    # in case that the table doesn't exist, insert one and return id
    insert_sql = text("INSERT INTO dbo.tabla (tabla) OUTPUT INSERTED.id VALUES (:table_name)")
    result = connection.execute(insert_sql,{"table_name":table_name})
    return result.fetchone()[0]

"""
This function return the field or "campo" id from the database data_process in the table campo
if the field is not in the database, insert a new one and return its id
"""
def get_or_create_field(connection, table_id: int, field_name:str) -> int:
    
    # search field id
    select_sql = text("SELECT id FROM dbo.campo WHERE id_tabla = :id_tabla AND campo = :campo")
    row = connection.execute(select_sql,{"id_tabla":table_id,"campo":field_name}).fetchone()

    # if the id field exist, return id
    if row:
        return row[0]
    
    # in case that doesn't exist, insert one and return id
    insert_sql = text("INSERT INTO dbo.campo (id_tabla, campo) OUTPUT INSERTED.id VALUES (:id_tabla,:campo)")
    result = connection.execute(insert_sql,{"id_tabla":table_id,"campo":field_name})
    return result.fetchone()[0]

"""
This function return the dimension id from the database data_process in the table dimension
if the dimension is not in the database, insert one and return its id
"""
def get_or_create_dimension(connection,dimension_name:str)->int:

    # Search dimension id
    select_sql = text("SELECT id FROM dbo.dimension WHERE dimension = :dimension_name")
    row = connection.execute(select_sql,{"dimension_name":dimension_name}).fetchone()

    # if the id dimension exist, return id
    if row:
        return row[0]
    
    # in case that doesn't exist, insert one and return id
    insert_sql = text("INSERT INTO dbo.dimension (dimension) OUTPUT INSERTED.id VALUES (:dimension_name)")
    result = connection.execute(insert_sql,{"dimension_name":dimension_name})
    return result.fetchone()[0]