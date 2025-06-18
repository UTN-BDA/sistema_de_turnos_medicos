from flask import Blueprint
from app.controllers import coordinadoras_controller

coordinadoras_bp = Blueprint('coordinadoras_bp', __name__, url_prefix='/coordinadoras')

coordinadoras_bp.route('/crear-con-notificacion', methods=['POST'])(coordinadoras_controller.crear_turno_con_notificacion)
coordinadoras_bp.route('/modificar-con-notificacion', methods=['PUT'])(coordinadoras_controller.modificar_turno_con_notificacion)
