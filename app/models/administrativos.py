# Modelo Administrativo como subclase de Usuario
from sqlalchemy import Column, Integer, String, ForeignKey
from app.models.usuarios import Usuario, TipoUsuario

class Administrativo(Usuario):
    __tablename__ = "administrativos"
    id = Column(Integer, ForeignKey("usuarios.id"), primary_key=True)
    nro_legajo = Column(String)
    __mapper_args__ = {
        'polymorphic_identity': TipoUsuario.ADMIN,
    }
