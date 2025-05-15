from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.usuarios import Usuario, TipoUsuario

class Medico(Usuario):
    __tablename__ = "medicos"
    id = Column(Integer, ForeignKey("usuarios.id"), primary_key=True)
    matricula = Column(String)
    especialidad = Column(String(100))
    __mapper_args__ = {
        'polymorphic_identity': TipoUsuario.MEDICO,
    }

    # Aquí indicamos explícitamente la foreign_key 
    turnos = relationship(
        "Turno",
        back_populates="medico",
        foreign_keys="[Turno.medico_id]"  
    )
