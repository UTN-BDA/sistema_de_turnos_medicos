from flask import Blueprint
from app.controllers import administrativos_controller

administrativos_bp = Blueprint('administrativos_bp', __name__, url_prefix='/administrativos')

# Definición de rutas usando asignación directa
administrativos_bp.route('/', methods=['GET'])(administrativos_controller.listar_administrativos)
administrativos_bp.route('/<int:id>', methods=['GET'])(administrativos_controller.obtener_administrativo)
administrativos_bp.route('/', methods=['POST'])(administrativos_controller.crear_administrativo)
administrativos_bp.route('/<int:id>', methods=['PUT'])(administrativos_controller.actualizar_administrativo)
administrativos_bp.route('/<int:id>', methods=['DELETE'])(administrativos_controller.eliminar_administrativo)
