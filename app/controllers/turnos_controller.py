from flask import request, jsonify
from app.models.turnos import Turno
from app.models.usuarios import Usuario
from app.extensions import db
from datetime import datetime

def listar_turnos():
    turnos = Turno.query.all()
    return jsonify([{
        "id": t.id,
        "fecha_hora": t.fecha_hora.isoformat(),
        "estado": t.estado,
        "paciente_id": t.paciente_id,
        "medico_id": t.medico_id
    } for t in turnos])

def obtener_turno(id):
    turno = Turno.query.get_or_404(id)
    return jsonify({
        "id": turno.id,
        "fecha_hora": turno.fecha_hora.isoformat(),
        "estado": turno.estado,
        "paciente_id": turno.paciente_id,
        "medico_id": turno.medico_id
    })

def crear_turno():
    data = request.get_json()
    try:
        fecha_hora = datetime.fromisoformat(data["fecha_hora"])
    except Exception:
        return jsonify({"error": "Formato de fecha inválido"}), 400

    paciente = Usuario.query.get(data.get("paciente_id"))
    medico = Usuario.query.get(data.get("medico_id"))

    if not paciente or paciente.tipo.name != "PACIENTE":
        return jsonify({"error": "Paciente inválido"}), 400
    if not medico or medico.tipo.name != "MEDICO":
        return jsonify({"error": "Médico inválido"}), 400

    turno = Turno(
        fecha_hora=fecha_hora,
        estado=data.get("estado", "programado"),
        paciente_id=paciente.id,
        medico_id=medico.id
    )
    db.session.add(turno)
    db.session.commit()
    return jsonify({"message": "Turno creado", "id": turno.id}), 201

def actualizar_turno(id):
    turno = Turno.query.get_or_404(id)
    data = request.get_json()
    if "fecha_hora" in data:
        try:
            turno.fecha_hora = datetime.fromisoformat(data["fecha_hora"])
        except Exception:
            return jsonify({"error": "Formato de fecha inválido"}), 400
    if "estado" in data:
        turno.estado = data["estado"]
    db.session.commit()
    return jsonify({"message": "Turno actualizado"})

def eliminar_turno(id):
    turno = Turno.query.get_or_404(id)
    db.session.delete(turno)
    db.session.commit()
    return jsonify({"message": "Turno eliminado"})

def listar_turnos_por_fecha():
    fecha = request.args.get("fecha")
    try:
        fecha_dt = datetime.fromisoformat(fecha)
    except Exception:
        return jsonify({"error": "Formato de fecha inválido"}), 400
    turnos = Turno.query.filter(
        db.func.date(Turno.fecha_hora) == fecha_dt.date()
    ).all()
    return jsonify([{
        "id": t.id,
        "fecha_hora": t.fecha_hora.isoformat(),
        "estado": t.estado,
        "paciente_id": t.paciente_id,
        "medico_id": t.medico_id
    } for t in turnos])

def listar_turnos_por_paciente(paciente_id):
    paciente = Usuario.query.get_or_404(paciente_id)
    if paciente.tipo.name != "PACIENTE":
        return jsonify({"error": "No es un paciente válido"}), 400
    turnos = Turno.query.filter(Turno.paciente_id == paciente.id).all()
    return jsonify([{
        "id": t.id,
        "fecha_hora": t.fecha_hora.isoformat(),
        "estado": t.estado,
        "paciente_id": t.paciente_id,
        "medico_id": t.medico_id
    } for t in turnos])

def listar_turnos_por_medico(medico_id):
    medico = Usuario.query.get_or_404(medico_id)
    if medico.tipo.name != "MEDICO":
        return jsonify({"error": "No es un médico válido"}), 400
    turnos = Turno.query.filter(Turno.medico_id == medico.id).all()
    return jsonify([{
        "id": t.id,
        "fecha_hora": t.fecha_hora.isoformat(),
        "estado": t.estado,
        "paciente_id": t.paciente_id,
        "medico_id": t.medico_id
    } for t in turnos])