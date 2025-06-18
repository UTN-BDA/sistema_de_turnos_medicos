from flask import request, jsonify
from app.models.administrativos import Administrativo
from app.extensions import db

def listar_administrativos():
    administrativos = Administrativo.query.all()
    resultado = [{
        "id": admin.id,
        "nombre": admin.nombre,
        "email": admin.email,
        "nro_legajo": admin.nro_legajo
    } for admin in administrativos]
    return jsonify(resultado), 200

def obtener_administrativo(id):
    admin = Administrativo.query.get_or_404(id)
    resultado = {
        "id": admin.id,
        "nombre": admin.nombre,
        "email": admin.email,
        "nro_legajo": admin.nro_legajo
    }
    return jsonify(resultado), 200

def crear_administrativo():
    data = request.get_json()
    nuevo_admin = Administrativo(
        nombre=data.get("nombre"),
        email=data.get("email"),
        nro_legajo=data.get("nro_legajo"),
        tipo="administrativo"
    )
    db.session.add(nuevo_admin)
    db.session.commit()
    return jsonify({"mensaje": "Administrativo creado exitosamente."}), 201

def actualizar_administrativo(id):
    admin = Administrativo.query.get_or_404(id)
    data = request.get_json()
    admin.nombre = data.get("nombre", admin.nombre)
    admin.email = data.get("email", admin.email)
    admin.nro_legajo = data.get("nro_legajo", admin.nro_legajo)
    db.session.commit()
    return jsonify({"mensaje": "Administrativo actualizado exitosamente."}), 200

def eliminar_administrativo(id):
    admin = Administrativo.query.get_or_404(id)
    db.session.delete(admin)
    db.session.commit()
    return jsonify({"mensaje": "Administrativo eliminado exitosamente."}), 200
