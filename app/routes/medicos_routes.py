from flask import Blueprint
from app.controllers import medicos_controller

medicos_bp = Blueprint('medicos_bp', __name__, url_prefix='/medicos')

# Definición de rutas usando asignación directa
medicos_bp.route('/', methods=['GET'])(medicos_controller.listar_medicos)
medicos_bp.route('/<int:id>', methods=['GET'])(medicos_controller.obtener_medico)
medicos_bp.route('/', methods=['POST'])(medicos_controller.crear_medico)
medicos_bp.route('/<int:id>', methods=['PUT'])(medicos_controller.actualizar_medico)
medicos_bp.route('/<int:id>', methods=['DELETE'])(medicos_controller.eliminar_medico)
