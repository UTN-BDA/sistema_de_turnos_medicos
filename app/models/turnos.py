# Modelo Turno: Representa la reserva de una consulta entre un paciente y un médico.
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.extensions import db

class EstadoTurno(PyEnum):
    PROGRAMADO = "programado"
    CANCELADO = "cancelado"
    REPROGRAMADO = "reprogramado"
    ATENDIDO = "atendido"
    PERDIDO = "perdido"

class Turno(db.Model):
    __tablename__ = "turnos"
    id = Column(Integer, primary_key=True)
    fecha_hora = Column(DateTime, nullable=False)   # Sin unique=True porque generaría una restricción individual (ningún duplicado, incluso para diferentes médicos)
    estado = Column(Enum(EstadoTurno), default=EstadoTurno.PROGRAMADO, nullable=False)
    reprogramaciones = Column(Integer, default=0, nullable=False)
    # Restricciones de clave foránea
    paciente_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    medico_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    administrativo_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    # Para que SQLAlchemy sepa qué fk usar en cada relación
    paciente = relationship("Paciente", back_populates="turnos", foreign_keys=[paciente_id])
    medico = relationship("Medico", back_populates="turnos", foreign_keys=[medico_id])
    administrativo = relationship("Administrativo", back_populates="turnos", foreign_keys=[administrativo_id])
    
    # Relación inversa
    notificaciones = relationship("Notificacion", back_populates="turno")

    __table_args__ = (
        db.UniqueConstraint('medico_id', 'fecha_hora', name='uq_medico_fecha'),
    )
