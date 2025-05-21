import sys
import os
import time

# Añade el directorio raíz del proyecto al sys.path
# Esto asume que el script está en 'scripts/' y la raíz del proyecto está un nivel arriba.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.database import db
from app.models.usuarios import Usuario

def consultar_usuario_por_email(email_a_buscar):
    """
    Consulta un usuario por su dirección de correo electrónico y mide el tiempo de respuesta.

    Args:
        email_a_buscar (str): El correo electrónico del usuario a buscar.
    """
    flask_app_instance = create_app()
    with flask_app_instance.app_context():
        print(f"Buscando usuario con email: {email_a_buscar}")
        
        start_time = time.time() # Inicia el temporizador

        # Realiza la consulta
        # .filter_by() es una forma conveniente para condiciones de igualdad
        # .first() obtiene el primer resultado o None si no se encuentra
        user = db.session.query(Usuario).filter_by(email=email_a_buscar).first()
        
        end_time = time.time() # Detiene el temporizador
        
        tiempo_transcurrido = (end_time - start_time) * 1000 # Tiempo en milisegundos

        if user:
            print(f"Usuario encontrado: ID={user.id}, Nombre={user.nombre}, Email={user.email}")
        else:
            print(f"Usuario con email '{email_a_buscar}' no encontrado.")
        
        print(f"Tiempo de consulta: {tiempo_transcurrido:.2f} ms")

if __name__ == "__main__":
    # Puedes cambiar este email por uno que sepas que existe en tu base de datos
    # o generar uno aleatoriamente si tienes muchos datos.
    # Para pruebas, es bueno usar un email que sabes que existe y uno que no.
    
    # Ejemplo de un email que probablemente exista si cargaste 1 millón de usuarios con Faker
    # Faker genera emails como 'nombre.apellido@example.com'
    # Si sabes un email específico que cargaste, úsalo.
    # De lo contrario, puedes intentar con un patrón común de Faker o un email inventado.
    
    # Para la primera prueba, puedes usar un email que sabes que no existe
    # o uno que generes y luego busques.
    
    # Si quieres buscar un email que sabes que existe, puedes buscarlo directamente en pgAdmin
    # o si tienes el script de carga, puedes modificarlo temporalmente para imprimir algunos emails generados.
    
    # Ejemplo de email para buscar (ajusta según tus datos)
    test_email = "canellasleonor@example.net" # Reemplaza con un email real de tu BD si lo tienes
    # Si no estás seguro de qué emails existen, puedes ejecutar una consulta en pgAdmin
    # SELECT email FROM usuarios LIMIT 10; para obtener algunos ejemplos.

    consultar_usuario_por_email(test_email)
    
    # Puedes probar con otro email que no exista para ver el tiempo de respuesta para no encontrados
    # consultar_usuario_por_email("nonexistent.user@example.com")
