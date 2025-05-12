from flask import Blueprint

# Importar blueprints individuales
from .pacientes_routes import pacientes_bp
from .medicos_routes import medicos_bp
from app.routes.administrativos_routes import administrativos_bp
from .turnos_routes import turnos_bp
from .notificaciones_routes import notificaciones_bp

# Crear un blueprint principal
bp = Blueprint("routes", __name__)

# Registrar cada blueprint modular
bp.register_blueprint(pacientes_bp)
bp.register_blueprint(medicos_bp)
bp.register_blueprint(administrativos_bp)
bp.register_blueprint(turnos_bp)
bp.register_blueprint(notificaciones_bp)

