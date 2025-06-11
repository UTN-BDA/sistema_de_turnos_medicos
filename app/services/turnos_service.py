# services/turnos_service.py
from datetime import datetime
from app.models.turnos import Turno, EstadoTurno

def crear_turno(data):
    required_fields = ["fecha_hora", "paciente_id", "medico_id"]
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Campo obligatorio '{field}' faltante.")

    try:
        fecha_hora = datetime.fromisoformat(data["fecha_hora"])
    except ValueError:
        raise ValueError("Formato de fecha inválido (se espera ISO 8601)")
    
    turno = Turno(
        fecha_hora=fecha_hora,
        estado=EstadoTurno.PROGRAMADO,
        paciente_id=data["paciente_id"],
        medico_id=data["medico_id"],
        administrativo_id=data.get("administrativo_id"),
        reprogramaciones=0
    )

    return turno


def modificar_turno(turno_id, nueva_fecha_str=None, nuevo_estado=None):
    turno = Turno.query.get(turno_id)
    if not turno:
        raise ValueError("Turno no encontrado")

    # No se puede modificar un turno cancelado, atendido o perdido
    if turno.estado in [EstadoTurno.CANCELADO, EstadoTurno.ATENDIDO, EstadoTurno.PERDIDO]:
        raise ValueError(f"No se puede modificar un turno con estado '{turno.estado.value}'")

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


    return turno
