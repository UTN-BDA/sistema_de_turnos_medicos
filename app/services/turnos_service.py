# services/turnos_service.py
from flask import jsonify
from datetime import datetime
from models import db, Usuario, Turno, EstadoTurno

def crear_turno(data):
    try:
        fecha_hora = datetime.fromisoformat(data["fecha_hora"])
    except Exception:
        return {"error": "Formato de fecha inválido"}, 400

    paciente = Usuario.query.get(data.get("paciente_id"))
    medico = Usuario.query.get(data.get("medico_id"))

    if not paciente or paciente.tipo.name != "PACIENTE":
        return {"error": "Paciente inválido"}, 400
    if not medico or medico.tipo.name != "MEDICO":
        return {"error": "Médico inválido"}, 400

    turno = Turno(
        fecha_hora=fecha_hora,
        estado=EstadoTurno.PROGRAMADO,
        paciente_id=paciente.id,
        medico_id=medico.id,
        reprogramaciones=0
    )
    db.session.add(turno)
    db.session.commit()

    return {"message": "Turno creado", "id": turno.id}, 201


def modificar_turno(turno_id, nueva_fecha_str=None, nuevo_estado=None):
    turno = Turno.query.get(turno_id)
    if not turno:
        raise ValueError("Turno no encontrado")

    if nueva_fecha_str:
        try:
            nueva_fecha = datetime.fromisoformat(nueva_fecha_str)
        except Exception:
            raise ValueError("Formato de nueva fecha inválido")

        turno.fecha_hora = nueva_fecha
        turno.estado = EstadoTurno.REPROGRAMADO
        turno.reprogramaciones += 1

    elif nuevo_estado:
        try:
            estado_enum = EstadoTurno(nuevo_estado)
        except ValueError:
            raise ValueError("Estado inválido")
        turno.estado = estado_enum

    else:
        raise ValueError("Se requiere nueva fecha o nuevo estado")

    db.session.add(turno)  # ← opcional, si se modifican campos automáticamente
    db.session.commit()    # línea para aplicar cambios

    return turno
