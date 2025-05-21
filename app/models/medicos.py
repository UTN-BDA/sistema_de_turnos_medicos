from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.usuarios import Usuario, TipoUsuario
from app.models.turnos import Turno  

class Medico(Usuario):
    __tablename__ = 'medicos'
    id = Column(Integer, ForeignKey('usuarios.id'), primary_key=True)
    matricula = Column(String(50), unique=True, nullable=False)
    especialidad = Column(String(100))
    __mapper_args__ = {
        'polymorphic_identity': TipoUsuario.MEDICO,
    }

    # Relaciones
    # Especificar explícitamente la clave foránea para la relación 'turnos'
    turnos = relationship("Turno", back_populates="medico", foreign_keys=[Turno.medico_id])
    notificaciones = relationship("Notificacion", back_populates="medico")