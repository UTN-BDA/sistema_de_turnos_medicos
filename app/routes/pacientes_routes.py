from flask import Blueprint, render_template
from app.controllers import pacientes_controller

pacientes_bp = Blueprint('pacientes_bp', __name__, url_prefix='/pacientes')

# Definición de rutas
pacientes_bp.route('/', methods=['GET'])(pacientes_controller.listar_pacientes)
pacientes_bp.route('/<int:id>', methods=['GET'])(pacientes_controller.obtener_paciente)
pacientes_bp.route('/', methods=['POST'])(pacientes_controller.crear_paciente)
pacientes_bp.route('/<int:id>', methods=['PUT'])(pacientes_controller.actualizar_paciente)
pacientes_bp.route('/<int:id>', methods=['DELETE'])(pacientes_controller.eliminar_paciente)
@pacientes_bp.route('/<int:paciente_id>', methods=['GET'])
def vista_paciente(paciente_id):
    return render_template("paciente.html", paciente_id=paciente_id)

