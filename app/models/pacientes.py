# Modelo Paciente como subclase de Usuario
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.usuarios import Usuario, TipoUsuario
from app.models.turnos import Turno  # Asegurate de importar Turno

class Paciente(Usuario):
    __tablename__ = "pacientes"
    id = Column(Integer, ForeignKey("usuarios.id"), primary_key=True)
    nro_historia_clinica = Column(String)
    __mapper_args__ = {
        'polymorphic_identity': TipoUsuario.PACIENTE,
    }

    # Relaciones
    turnos = relationship("Turno", back_populates="paciente", foreign_keys=[Turno.paciente_id])
    notificaciones = relationship("Notificacion", back_populates="paciente")

