# Libraries
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv


# Load .env file
load_dotenv()

# Function to connect to database
def get_sqlserver_engine():
    print("connection")

    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_driver = os.getenv("DB_DRIVER")

    # debuggin
    # print(db_host,db_port,db_name,db_user,db_password,db_driver)

    # SQLAlchemy connection string for SQL Server
    connection_string = (
        f"mssql+pyodbc://{db_user}:{db_password}"
        f"@{db_host}:{db_port}/{db_name}"
        f"?driver={db_driver.replace(' ', '+')}"
        "&Encrypt=yes"
        "&TrustServerCertificate=yes"
    )

    # Create engine
    engine = create_engine(connection_string)

    return engine

def get_sqlserver_engine_results():
    print("connection")

    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME_2")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_driver = os.getenv("DB_DRIVER")

    # debuggin
    # print(db_host,db_port,db_name,db_user,db_password,db_driver)

    # SQLAlchemy connection string for SQL Server
    connection_string = (
        f"mssql+pyodbc://{db_user}:{db_password}"
        f"@{db_host}:{db_port}/{db_name}"
        f"?driver={db_driver.replace(' ', '+')}"
        "&Encrypt=yes"
        "&TrustServerCertificate=yes"
    )

    # Create engine
    engine = create_engine(connection_string)

    return engine