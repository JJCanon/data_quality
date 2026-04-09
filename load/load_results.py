# Libraries
from sqlalchemy import text
# Internal imports
from load.preload import preload_data

# Functions
## This function load the results in the database
def load_results(metrics: list[dict])-> None:

    # Preload results
    print("Preloading data")
    preloaded_results = preload_data(metrics)

    # Load results
    print("Loading data")
    insert_results(preloaded_results)

    print("Results loaded")
    return preloaded_results["engine"]



# Auxiliary functions
## This function load data into the database
def insert_results(preloaded_results:dict) -> None:
    
    engine = preloaded_results["engine"]
    ejecution_id = preloaded_results["id_ejecucion"]
    rows = preloaded_results["rows"]

    if not rows:
        print("[insert_results] No hay filas para insertar.")
        return
    
    insert_sql = text(
        """
        INSERT INTO dbo.resultado (id_ejecucion, id_campo, id_dimension, score)
        VALUES (:id_ejecucion,:id_campo,:id_dimension, :score)
        """
    )

    with engine.begin() as connection:
        for row in rows:
            connection.execute(insert_sql,{
                "id_ejecucion": ejecution_id,
                "id_campo": row["id_campo"],
                "id_dimension": row["id_dimension"],
                "score": row["score"]
            })

    print(f"  [insert_results] {len(rows)} filas insertadas en dbo.Resultado "
          f"(id_ejecucion={ejecution_id}).")


