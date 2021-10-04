# IMPORTS
from flask_jsonschema_validator import JSONSchemaValidator
from controllers.data import data_controller
from services.data import data_service
from flask_cors import CORS
from flask import Flask
import psycopg2


# INICIAR API
def PSQLApi():
    connect = None
    cursor = None
    app = None

    # APP
    app = Flask(__name__)
    app.config['CORS_HEADERS'] = 'Content-Type'
    CORS(app, resources={r"/*": {"origins": "*"}})

    # CONFIGURACION DE POSTGRES
    DB_HOST = "localhost"
    DB_NAME = "Blockbuster"
    DB_USER = "postgres"
    DB_PASS = "root"

    # CONNECTION
    try:
        connect = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST)
        cursor = connect.cursor()
    except:
        print('Error en la conexion a postgres')

    # JSON VALIDATION
    JSONSchemaValidator(app, root="models")

    # INICIAR CONTROLADORES
    data_controller(app, data_service, cursor, connect)

    # INSTANCIA
    return app
