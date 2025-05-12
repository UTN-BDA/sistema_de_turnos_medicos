from flask import Blueprint
from app.controllers import turnos_controller

turnos_bp = Blueprint('turnos_bp', __name__, url_prefix='/turnos')

turnos_bp.route('/', methods=['GET'])(turnos_controller.listar_turnos)
turnos_bp.route('/<int:id>', methods=['GET'])(turnos_controller.obtener_turno)
turnos_bp.route('/', methods=['POST'])(turnos_controller.crear_turno)
turnos_bp.route('/<int:id>', methods=['PUT'])(turnos_controller.actualizar_turno)
turnos_bp.route('/<int:id>', methods=['DELETE'])(turnos_controller.eliminar_turno)
turnos_bp.route('/filtrar/fecha', methods=['GET'])(turnos_controller.listar_turnos_por_fecha)
turnos_bp.route('/paciente/<int:paciente_id>', methods=['GET'])(turnos_controller.listar_turnos_por_paciente)
turnos_bp.route('/medico/<int:medico_id>', methods=['GET'])(turnos_controller.listar_turnos_por_medico)
