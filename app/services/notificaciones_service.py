# services/notificaciones_service.py
from flask import jsonify
from models import db, Notificacion, TipoNotificacion

def crear_notificacion(data):
    try:
        tipo = TipoNotificacion(data["tipo"])
    except ValueError:
        return {"error": "Tipo de notificación inválido"}, 400

    notificacion = Notificacion(
        tipo=tipo,
        mensaje=data["mensaje"],
        paciente_id=data.get("paciente_id"),
        turno_id=data.get("turno_id"),
        origen=data.get("origen")
    )
    db.session.add(notificacion)
    db.session.commit()

    return {
        "mensaje": "Notificación creada correctamente",
        "paciente_id": notificacion.paciente_id,
        "mensaje_emit": notificacion.mensaje
    }, 201

