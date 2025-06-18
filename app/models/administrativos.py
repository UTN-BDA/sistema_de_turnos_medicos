# Modelo Administrativo como subclase de Usuario
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.usuarios import Usuario, TipoUsuario
from app.models.turnos import Turno

class Administrativo(Usuario):
    __tablename__ = "administrativos"
    id = Column(Integer, ForeignKey("usuarios.id"), primary_key=True)
    nro_legajo = Column(String)
    __mapper_args__ = {
        'polymorphic_identity': TipoUsuario.ADMIN,
    }

    # Relaciones inversas
    turnos = relationship("Turno", back_populates="administrativo", foreign_keys=[Turno.administrativo_id])

