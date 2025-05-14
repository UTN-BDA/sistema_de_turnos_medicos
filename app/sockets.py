from flask_socketio import emit, join_room
from app.database import socketio

# Evento: cuando el paciente se conecta al sistema
@socketio.on('unirse')
def manejar_unirse(data):
    tipo = data.get('tipo')  # 'paciente' o 'medico'
    id_usuario = data.get('id')
    if tipo and id_usuario:
        room = f"{tipo}_{id_usuario}"
        join_room(room)
        print(f"Usuario {tipo} con ID {id_usuario} se unió a la sala {room}")
        emit("joined", {"mensaje": f"Conectado a la sala {room}"})

# Enviar una notificación a un paciente específico
def notificar_paciente(paciente_id, mensaje):
    room = f"paciente_{paciente_id}"
    socketio.emit("nueva_notificacion", mensaje, room=room)


# Enviar una notificación a un médico (si se implementa en el futuro)
def notificar_medico(medico_id, mensaje):
    room = f"medico_{medico_id}"
    socketio.emit("nueva_notificacion", mensaje, room=room)
