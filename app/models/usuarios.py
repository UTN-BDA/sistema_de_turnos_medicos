# Modelo base: Usuario con herencia simple
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.ext.declarative import declared_attr
from enum import Enum as PyEnum
from app.database import db

class TipoUsuario(PyEnum):
    PACIENTE = "paciente"
    MEDICO = "medico"
    ADMIN = "administrativo"

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    tipo = Column(Enum(TipoUsuario), nullable=False)  # Discriminador

    __mapper_args__ = {
        'polymorphic_identity': 'usuario',
        'polymorphic_on': tipo
    }
