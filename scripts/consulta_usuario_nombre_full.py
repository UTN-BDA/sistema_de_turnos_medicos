import sys
import os
import time

# Añade el directorio raíz del proyecto al sys.path
# Esto asume que el script está en 'scripts/' y la raíz del proyecto está un nivel arriba.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.database import db
from app.models.usuarios import Usuario

def consultar_usuarios_por_nombre_o_apellido(cadena_a_buscar, buscar_exacto=False):
    """
    Consulta usuarios por su nombre o apellido (o parte de ellos) y mide el tiempo de respuesta.
    Puede buscar coincidencias exactas o parciales.

    Args:
        cadena_a_buscar (str): La cadena (nombre o apellido) a buscar.
        buscar_exacto (bool): Si es True, busca una coincidencia exacta.
                              Si es False, busca coincidencias parciales (LIKE).
    Returns:
        list: Una lista de objetos Usuario que coinciden con la búsqueda.
    """
    flask_app_instance = create_app()
    with flask_app_instance.app_context():
        print(f"Buscando usuarios con '{cadena_a_buscar}' (Exacto: {buscar_exacto})")
        
        start_time = time.time() # Inicia el temporizador

        query = db.session.query(Usuario)

        if buscar_exacto:
            # Búsqueda exacta: si hay dos con el mismo nombre, traerá el primero con .first()
            # Si quieres todos los que se llamen igual, usarías .all() aquí.
            # Para esta función, si buscar_exacto es True, devolveremos todos los exactos.
            users = query.filter_by(nombre=cadena_a_buscar).all()
        else:
            # Búsqueda parcial (ej. para apellidos como 'Perez')
            # Usamos ilike para que la búsqueda no distinga entre mayúsculas y minúsculas
            users = query.filter(Usuario.nombre.like(f'%{cadena_a_buscar}%')).all()
        
        end_time = time.time() # Detiene el temporizador
        
        tiempo_transcurrido = (end_time - start_time) * 1000 # Tiempo en milisegundos

        if users:
            print(f"Se encontraron {len(users)} usuarios:")
            for user in users:
                print(f"  - ID={user.id}, Nombre={user.nombre}, Email={user.email}")
        else:
            print(f"No se encontraron usuarios con '{cadena_a_buscar}'.")
        
        print(f"Tiempo de consulta: {tiempo_transcurrido:.2f} ms")
        return users

if __name__ == "__main__":
    # --- PRUEBAS DE BÚSQUEDA EXACTA ---
    print("\n--- Pruebas de Búsqueda Exacta ---")
    # Si tienes dos usuarios con el mismo nombre, esta búsqueda traerá AMBOS.
    # Si solo quieres el primero, cambiarías .all() por .first() en la función.
    consultar_usuarios_por_nombre_o_apellido("Raquel Alba", buscar_exacto=True)


    # --- PRUEBAS DE BÚSQUEDA PARCIAL (por apellido o parte del nombre) ---
    #print("\n--- Pruebas de Búsqueda Parcial ---")
    #consultar_usuarios_por_nombre_o_apellido("Llano Cerezo", buscar_exacto=False)

