import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models.usuarios import Usuario, TipoUsuario
from faker import Faker
from dotenv import load_dotenv

from app import create_app
from app.database import db

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Crea una instancia de Faker
fake = Faker('es_ES')

def get_existing_emails(session):
    """
    Obtiene todos los correos electrónicos existentes en la base de datos.
    """
    # Consulta todos los emails de la tabla Usuario
    existing_emails = session.query(Usuario.email).all()
    # Convierte la lista de tuplas a un conjunto para búsquedas rápidas
    return {email[0] for email in existing_emails}

def generar_usuario(existing_emails):
    """
    Genera un usuario con un correo electrónico único, verificando contra
    los correos existentes en la base de datos y los generados en la sesión actual.
    """
    tipo = fake.random_element(elements=[TipoUsuario.PACIENTE, TipoUsuario.MEDICO, TipoUsuario.ADMIN])
    email = fake.email()
    # Bucle para generar un email único
    while email in existing_emails:
        email = fake.email()
    existing_emails.add(email) # Añade el nuevo email al conjunto de emails existentes
    return Usuario(
        nombre=fake.name(),
        email=email,
        tipo=tipo,
    )

def cargar_usuarios_bulk(cantidad):
    """
    Carga un lote de usuarios en la base de datos.
    """
    # Obtener los emails ya existentes en la base de datos
    existing_emails = get_existing_emails(db.session)
    
    usuarios = []
    for _ in range(cantidad):
        usuario = generar_usuario(existing_emails)
        usuarios.append(usuario)

    db.session.bulk_save_objects(usuarios)
    db.session.commit()
    print(f"Se han cargado {cantidad} usuarios usando bulk_save_objects().")

def cargar_datos():
    """Función para cargar los datos iniciales."""
    flask_app_instance = create_app()
    with flask_app_instance.app_context():
        cargar_usuarios_bulk(1000000)

# Llama a la función para cargar los datos
cargar_datos()
