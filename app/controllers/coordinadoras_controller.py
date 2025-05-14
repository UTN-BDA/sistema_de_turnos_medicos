from flask import request, jsonify
from flask_socketio import emit
from app.sockets import notificar_paciente
from services.turnos_service import crear_turno, modificar_turno
from services.notificaciones_service import crear_notificacion

def crear_turno_con_notificacion():
    data = request.get_json()

    # Crear el turno
    turno_result, status = crear_turno(data)
    if status != 201:
        return jsonify(turno_result), status

    turno_id = turno_result["id"]

    # Crear la notificación
    noti_data = {
        "tipo": "PROGRAMACION",
        "mensaje": f"Se creó un nuevo turno para el {data['fecha_hora']}.",
        "paciente_id": data["paciente_id"],
        "turno_id": turno_id,
        "origen": "sistema"
    }

    noti_result, noti_status = crear_notificacion(noti_data)
    if noti_status != 201:
        return jsonify(noti_result), noti_status

    # Emitir notificación al paciente por WebSocket
    notificar_paciente(noti_result["paciente_id"], {
    "mensaje": noti_result["mensaje_emit"]
    })

    return jsonify({"mensaje": "Turno y notificación creados correctamente"}), 201

def modificar_turno_con_notificacion(data):
    try:
        turno_modificado = modificar_turno(
            turno_id=data["turno_id"],
            nueva_fecha_str=data.get("nueva_fecha_str"),
            nuevo_estado=data.get("nuevo_estado")
        )
    except ValueError as e:
        return {"error": str(e)}, 400

    # Determinar tipo de notificación según el nuevo estado
    estado = turno_modificado.estado.value  # "programado", "reprogramado", etc.
    tipo_map = {
        "programado": "otorgamiento",
        "reprogramado": "reprogramacion",
        "cancelado": "cancelacion",
        "atendido": "consulta_realizada",
        "perdido": "perdida_del_turno"
    }
    tipo_notificacion = tipo_map.get(estado, "otorgamiento")

    noti_data = {
        "tipo": tipo_notificacion,
        "mensaje": data.get("mensaje", f"El estado de su turno ha cambiado a {estado}"),
        "paciente_id": turno_modificado.paciente_id,
        "turno_id": turno_modificado.id,
        "origen": data.get("origen", "sistema")
    }

    noti_result, noti_status = crear_notificacion(noti_data)
    if noti_status != 201:
        return noti_result, noti_status

    # Emitir notificación al paciente
    emit("nueva_notificacion", {
        "mensaje": noti_result["mensaje_emit"]
    }, to=f"paciente_{noti_result['paciente_id']}")

    return jsonify({"mensaje": "Turno modificado y notificación enviada"}), 200
