from flask import request, jsonify
from app.models.medicos import Medico
from app.extensions import db

# Listar todos los médicos
def listar_medicos():
    medicos = Medico.query.all()
    return jsonify([{
        'id': m.id,
        'nombre': m.nombre,
        'email': m.email,
        'matricula': m.matricula,
        'especialidad': m.especialidad
    } for m in medicos])

# Obtener un médico por ID
def obtener_medico(id):
    medico = Medico.query.get_or_404(id)
    return jsonify({
        'id': medico.id,
        'nombre': medico.nombre,
        'email': medico.email,
        'matricula': medico.matricula,
        'especialidad': medico.especialidad
    })

# Crear un nuevo médico
def crear_medico():
    data = request.json
    nuevo_medico = Medico(
        nombre=data.get('nombre'),
        email=data.get('email'),
        tipo='medico',  # se puede usar TipoUsuario.MEDICO si se importa
        matricula=data.get('matricula'),
        especialidad=data.get('especialidad')
    )
    db.session.add(nuevo_medico)
    db.session.commit()
    return jsonify({'mensaje': 'Médico creado', 'id': nuevo_medico.id}), 201

# Actualizar un médico
def actualizar_medico(id):
    medico = Medico.query.get_or_404(id)
    data = request.json
    medico.nombre = data.get('nombre', medico.nombre)
    medico.email = data.get('email', medico.email)
    medico.matricula = data.get('matricula', medico.matricula)
    medico.especialidad = data.get('especialidad', medico.especialidad)
    db.session.commit()
    return jsonify({'mensaje': 'Médico actualizado'})

# Eliminar un médico
def eliminar_medico(id):
    medico = Medico.query.get_or_404(id)
    db.session.delete(medico)
    db.session.commit()
    return jsonify({'mensaje': 'Médico eliminado'})
