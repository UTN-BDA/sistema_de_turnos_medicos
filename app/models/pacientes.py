# Modelo Paciente como subclase de Usuario
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.usuarios import Usuario, TipoUsuario
from app.models.turnos import Turno  

class Paciente(Usuario):
    __tablename__ = "pacientes"
    id = Column(Integer, ForeignKey("usuarios.id"), primary_key=True)
    nro_historia_clinica = Column(String)
    __mapper_args__ = {
        'polymorphic_identity': TipoUsuario.PACIENTE,
    }

    # Relaciones
    # Se especifica explícitamente la clave foránea para la relación 'turnos'
    # Esto le dice a SQLAlchemy que use 'Turno.paciente_id' para vincular Paciente con Turno.
    turnos = relationship("Turno", back_populates="paciente", foreign_keys=[Turno.paciente_id])
    notificaciones = relationship("Notificacion", back_populates="paciente")

