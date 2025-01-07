from http.client import HTTPException
import pymysql # type: ignore
from sqlalchemy import create_engine, text # type: ignore
from sqlalchemy.engine import Row # type: ignore

import os

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "aubay",
    "cursorclass": pymysql.cursors.DictCursor,
}


def test_connexion(host, user, password, database):
    """
    Teste la connexion à une base de données MySQL.
    
    :param host: Adresse du serveur (e.g., 'localhost' ou IP)
    :param user: Nom de l'utilisateur MySQL
    :param password: Mot de passe de l'utilisateur
    :param database: Nom de la base de données
    :return: True si la connexion réussit, False sinon
    """
    try:
        # Établir la connexion
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        
        # Vérifier si la connexion est ouverte
        if connection.open:
            print("Connexion réussie à la base de données!")
            connection.close()  # Fermer la connexion
            return True
        else:
            print("Échec de la connexion.")
            return False
    except pymysql.MySQLError as e:
        print(f"Erreur lors de la connexion à la base de données : {e}")
        return False
def validate_and_clean_query(query: str) -> str:
    # Supprimer tout point-virgule mal placé
    cleaned_query = query.replace(';', '').strip()
    # Ajout du point-virgule uniquement à la fin
    if not cleaned_query.endswith(';'):
        cleaned_query += ';'
    return cleaned_query
def getData(host:str,user:str,db:str,password:str,query:str):
    query = validate_and_clean_query(query)
    database_url = f"mysql+pymysql://{user}:{password}@{host}/{db}"
    engine = create_engine(database_url)
    with engine.connect() as connection:
      with connection.begin():
        result=connection.execute(text(query)).fetchall()
        #print("DEBUG: Raw result:", result)
        return [row._asdict() if isinstance(row, Row) else dict(row) for row in result]
      


      
def get_db_connection():
    try:
        connection = pymysql.connect(**DB_CONFIG)
        return connection
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")
    

