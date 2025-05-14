# Modelo Turno: Representa la reserva de una consulta entre un paciente y un médico.
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.database import db

class EstadoTurno(PyEnum):
    PROGRAMADO = "programado"
    CANCELADO = "cancelado"
    REPROGRAMADO = "reprogramado"
    ATENDIDO = "atendido"
    PERDIDO = "perdido"

class Turno(db.Model):
    __tablename__ = "turnos"
    id = Column(Integer, primary_key=True)
    fecha_hora = Column(DateTime, nullable=False)
    estado = Column(Enum(EstadoTurno), default=EstadoTurno.PROGRAMADO)
    reprogramaciones = Column(Integer, default=0)
    
    paciente_id = Column(Integer, ForeignKey("usuarios.id"))
    medico_id = Column(Integer, ForeignKey("usuarios.id"))

    paciente = relationship("Paciente", back_populates="turnos", foreign_keys=[paciente_id])
    medico = relationship("Medico", back_populates="turnos", foreign_keys=[medico_id])
    notificaciones = relationship("Notificacion", back_populates="turno")
