from .personnel import personnel_bp
from .additive import additive_bp
from .packaging import packaging_bp
from .weight import weight_bp
from .humidity import humidity_bp
from .cleaning import cleaning_bp
from .faults_penalties import penailties_bp


# Registrar todas las rutas


def register_routes(app):
    app.register_blueprint(personnel_bp)
    app.register_blueprint(additive_bp)
    app.register_blueprint(packaging_bp)
    app.register_blueprint(weight_bp)
    app.register_blueprint(humidity_bp)
    app.register_blueprint(cleaning_bp)
    app.register_blueprint(penailties_bp)