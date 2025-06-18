# Agregar el directorio raíz al sys.path para permitir las importaciones del paquete 'app'
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app import create_app
from app.extensions import socketio

# Crear una instancia de la aplicación Flask
app = create_app()

# Ejecutar el servidor con soporte para WebSocket mediante Flask-SocketIO
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True, allow_unsafe_werkzeug=True)
