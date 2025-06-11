# routes/notificaciones_routes.py
from flask import Blueprint
from app.controllers import notificaciones_controller

notificaciones_bp = Blueprint('notificaciones_bp', __name__, url_prefix='/notificaciones')

notificaciones_bp.route('/', methods=['GET'])(notificaciones_controller.listar_notificaciones)
notificaciones_bp.route('/<int:id>', methods=['GET'])(notificaciones_controller.obtener_notificacion)
notificaciones_bp.route('/', methods=['POST'])(notificaciones_controller.crear_notificacion)
notificaciones_bp.route('/<int:id>', methods=['PUT'])(notificaciones_controller.actualizar_estado)
notificaciones_bp.route('/<int:id>', methods=['DELETE'])(notificaciones_controller.eliminar_notificacion)

# Rutas específicas por paciente
notificaciones_bp.route('/paciente/<int:paciente_id>', methods=['GET'])(notificaciones_controller.listar_por_paciente)
notificaciones_bp.route('/paciente/<int:paciente_id>/no-leidas', methods=['GET'])(notificaciones_controller.listar_no_leidas_por_paciente)

# Filtrado
notificaciones_bp.route('/tipo/<string:tipo>', methods=['GET'])(notificaciones_controller.listar_por_tipo)
notificaciones_bp.route('/estado/<string:estado>', methods=['GET'])(notificaciones_controller.listar_por_estado)
