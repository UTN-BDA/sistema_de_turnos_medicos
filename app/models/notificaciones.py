# Modelo Notificacion: 
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.extensions import db

class TipoNotificacion(PyEnum):
    OTORGAMIENTO = "otorgamiento"
    CANCELACION = "cancelación"
    REPROGRAMACION = "reprogramacion"
    CONSULTA_REALIZADA = "consulta_realizada"
    PERDIDA_TURNO = "perdida_del_turno"

class EstadoNotificacion(PyEnum):
    NO_LEIDA = "no_leida"
    LEIDA = "leida"                                         # CONFIRMADA/O = "confirmada/o" podría agregarse más adelante (y/o "cancelado").

class Notificacion(db.Model):
    __tablename__ = "notificaciones"

    id = Column(Integer, primary_key=True)
    tipo = Column(Enum(TipoNotificacion), nullable=False)
    mensaje = Column(Text, nullable=False)
    fecha_envio = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    turno_id = Column(Integer, ForeignKey("turnos.id"), nullable=False)

    estado = Column(Enum(EstadoNotificacion), default=EstadoNotificacion.NO_LEIDA, nullable=False)
    origen = Column(String(50), nullable=True)  # Opcional. Ej: 'médico', 'administrativo', 'sistema'

    # Relación opcional
    turno = relationship("Turno", back_populates="notificaciones", foreign_keys=[turno_id])
