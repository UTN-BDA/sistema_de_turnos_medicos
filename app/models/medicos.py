# Modelo Medico como subclase de Usuario
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.usuarios import Usuario, TipoUsuario

class Medico(Usuario):
    __tablename__ = "medicos"
    id = Column(Integer, ForeignKey("usuarios.id"), primary_key=True)
    matricula = Column(String)
    __mapper_args__ = {
        'polymorphic_identity': TipoUsuario.MEDICO,
    }

    especialidad = Column(String(100))
    turnos = relationship("Turno", back_populates="medico")
