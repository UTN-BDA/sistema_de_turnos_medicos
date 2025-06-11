# Rutas web (rutas en Flask que renderizan los templates)
from flask import Blueprint, render_template

web_bp = Blueprint('web_bp', __name__, url_prefix='/web')

@web_bp.route('/paciente/<int:paciente_id>')
def vista_paciente(paciente_id):
    return render_template("paciente.html", paciente_id=paciente_id)

@web_bp.route('/medico/<int:medico_id>')
def vista_medico(medico_id):
    return render_template("medico.html", medico_id=medico_id)

@web_bp.route('/administrativo')
def vista_admin():
    return render_template("administrativo.html")

