from flask import Blueprint

# Importar blueprints individuales
from .pacientes_routes import pacientes_bp
from .medicos_routes import medicos_bp
from app.routes.administrativos_routes import administrativos_bp
from .turnos_routes import turnos_bp
from .notificaciones_routes import notificaciones_bp
from .coordinadoras_routes import coordinadoras_bp
from .web_routes import web_bp

# Crear un blueprint principal
bp = Blueprint("routes", __name__)

# Registrar cada blueprint modular
bp.register_blueprint(pacientes_bp)
bp.register_blueprint(medicos_bp)
bp.register_blueprint(administrativos_bp)
bp.register_blueprint(turnos_bp)
bp.register_blueprint(notificaciones_bp)
bp.register_blueprint(coordinadoras_bp)
bp.register_blueprint(web_bp)

@bp.route("/")
def index():
    return "<h1>Bienvenido a la App de Turnos Médicos</h1><p>El backend está funcionando correctamente.</p>"

