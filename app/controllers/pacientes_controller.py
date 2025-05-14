from flask import request, jsonify
from app.models.pacientes import Paciente
from app.database import db

# Listar todos los pacientes
def listar_pacientes():
    pacientes = Paciente.query.all()
    return jsonify([{
        "id": p.id,
        "nombre": p.nombre,
        "email": p.email,
        "nro_historia_clinica": p.nro_historia_clinica
    } for p in pacientes]), 200

# Obtener un paciente por ID
def obtener_paciente(id):
    paciente = Paciente.query.get(id)
    if paciente is None:
        return jsonify({"mensaje": "Paciente no encontrado"}), 404

    return jsonify({
        "id": paciente.id,
        "nombre": paciente.nombre,
        "email": paciente.email,
        "nro_historia_clinica": paciente.nro_historia_clinica
    }), 200

# Crear un nuevo paciente
def crear_paciente():
    data = request.get_json()
    nuevo_paciente = Paciente(
        nombre=data.get("nombre"),
        email=data.get("email"),
        tipo="paciente",  # necesario por el discriminador
        nro_historia_clinica=data.get("nro_historia_clinica")
    )
    db.session.add(nuevo_paciente)
    db.session.commit()
    return jsonify({"mensaje": "Paciente creado", "id": nuevo_paciente.id}), 201

# Actualizar un paciente
def actualizar_paciente(id):
    paciente = Paciente.query.get(id)
    if paciente is None:
        return jsonify({"mensaje": "Paciente no encontrado"}), 404

    data = request.get_json()
    paciente.nombre = data.get("nombre", paciente.nombre)
    paciente.email = data.get("email", paciente.email)
    paciente.nro_historia_clinica = data.get("nro_historia_clinica", paciente.nro_historia_clinica)

    db.session.commit()
    return jsonify({"mensaje": "Paciente actualizado"}), 200

# Eliminar un paciente
def eliminar_paciente(id):
    paciente = Paciente.query.get(id)
    if paciente is None:
        return jsonify({"mensaje": "Paciente no encontrado"}), 404

    db.session.delete(paciente)
    db.session.commit()
    return jsonify({"mensaje": "Paciente eliminado"}), 200
