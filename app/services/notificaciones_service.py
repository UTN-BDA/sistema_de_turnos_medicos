# services/notificaciones_service.py
from app.models.notificaciones import  Notificacion, TipoNotificacion

def crear_notificacion(data):
    required_fields = ["tipo", "mensaje"]
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Campo obligatorio '{field}' faltante.")

    try:
        tipo = TipoNotificacion(data["tipo"])
    except ValueError:
        raise ValueError(f"Tipo de notificación inválido: '{data['tipo']}'")

    notificacion = Notificacion(
        tipo=tipo,
        mensaje=data["mensaje"],
        turno_id=data.get("turno_id"),
        origen=data.get("origen")
    )

    return notificacion
