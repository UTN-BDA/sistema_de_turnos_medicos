# controllers/notificaciones_controller.py
from flask import jsonify, request
from app.models.notificaciones import Notificacion, TipoNotificacion, EstadoNotificacion
from app.models.turnos import Turno
from app.models.pacientes import Paciente
from app.database import db

def listar_notificaciones():
    notificaciones = Notificacion.query.all()
    return jsonify([{
        "id": n.id,
        "tipo": n.tipo.value,
        "mensaje": n.mensaje,
        "fecha_envio": n.fecha_envio,
        "estado": n.estado.value,
        "origen": n.origen,
        "paciente_id": n.paciente_id,
        "turno_id": n.turno_id
    } for n in notificaciones])

def obtener_notificacion(id):
    n = Notificacion.query.get_or_404(id)
    return jsonify({
        "id": n.id,
        "tipo": n.tipo.value,
        "mensaje": n.mensaje,
        "fecha_envio": n.fecha_envio,
        "estado": n.estado.value,
        "origen": n.origen,
        "paciente_id": n.paciente_id,
        "turno_id": n.turno_id
    })

def crear_notificacion():
    data = request.json
    notificacion = Notificacion(
        tipo=TipoNotificacion(data["tipo"]),
        mensaje=data["mensaje"],
        paciente_id=data.get("paciente_id"),
        turno_id=data.get("turno_id"),
        origen=data.get("origen")
    )
    db.session.add(notificacion)
    db.session.commit()
    return jsonify({"mensaje": "Notificación creada correctamente"}), 201

def actualizar_estado(id):
    data = request.get_json()
    nuevo_estado = data.get('estado')

    notificacion = Notificacion.query.get(id)
    if not notificacion:
        return jsonify({"error": "Notificación no encontrada"}), 404

    if nuevo_estado not in [estado.value for estado in EstadoNotificacion]:
        return jsonify({"error": "Estado inválido"}), 400

    notificacion.estado = EstadoNotificacion(nuevo_estado)
    db.session.commit()

    return jsonify({"mensaje": f"Estado actualizado a {nuevo_estado}"}), 200

def eliminar_notificacion(id):
    notificacion = Notificacion.query.get_or_404(id)
    db.session.delete(notificacion)
    db.session.commit()
    return jsonify({"mensaje": "Notificación eliminada"})

def listar_por_paciente(paciente_id):
    notificaciones = Notificacion.query.filter_by(paciente_id=paciente_id).all()
    return jsonify([{
        "id": n.id,
        "tipo": n.tipo.value,
        "mensaje": n.mensaje,
        "fecha_envio": n.fecha_envio,
        "estado": n.estado.value
    } for n in notificaciones])

def listar_no_leidas_por_paciente(paciente_id):
    notificaciones = Notificacion.query.filter_by(paciente_id=paciente_id, estado=EstadoNotificacion.NO_LEIDA).all()
    return jsonify([{
        "id": n.id,
        "tipo": n.tipo.value,
        "mensaje": n.mensaje,
        "fecha_envio": n.fecha_envio
    } for n in notificaciones])

def listar_por_tipo(tipo):
    try:
        tipo_enum = TipoNotificacion(tipo)
    except ValueError:
        return jsonify({"error": "Tipo de notificación inválido"}), 400

    notificaciones = Notificacion.query.filter_by(tipo=tipo_enum).all()
    resultado = []
    for noti in notificaciones:
        resultado.append({
            "id": noti.id,
            "tipo": noti.tipo.value,
            "mensaje": noti.mensaje,
            "fecha_envio": noti.fecha_envio.isoformat(),
            "estado": noti.estado.value,
            "origen": noti.origen,
            "paciente_id": noti.paciente_id,
            "turno_id": noti.turno_id
        })
    return jsonify(resultado), 200

def listar_por_estado(estado):
    try:
        estado_enum = EstadoNotificacion(estado)
    except ValueError:
        return jsonify({"error": "Estado de notificación inválido"}), 400

    notificaciones = Notificacion.query.filter_by(estado=estado_enum).all()
    resultado = []
    for noti in notificaciones:
        resultado.append({
            "id": noti.id,
            "tipo": noti.tipo.value,
            "mensaje": noti.mensaje,
            "fecha_envio": noti.fecha_envio.isoformat(),
            "estado": noti.estado.value,
            "origen": noti.origen,
            "paciente_id": noti.paciente_id,
            "turno_id": noti.turno_id
        })
    return jsonify(resultado), 200
