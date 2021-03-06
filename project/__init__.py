from flask import Flask,Blueprint
from flask_sqlalchemy import SQLAlchemy
from project.routes.login_view import login_bp
from . import models, routes, services
# db = SQLAlchemy()
#app = Flask(__name__)
#app.config.from_object('project.config.Config')
#models.init_app(app)
#routes.init_app(app)


def create_app():
    from . import models, routes, services
    app = Flask(__name__)
    app.config.from_object('project.config.Config')
    # db.init_app(app)
    models.init_app(app)
    routes.init_app(app)
    # services.init_app(app)
    # with app.app_context():

        # app.register_blueprint(login_bp)

        # Create tables for our models
        # db.create_all()
    return app

if __name__ == '__main__':
    # app.run(host, port, debug, options)
    # host要监听的主机名。 默认为127.0.0.1（localhost）
    # debug 默认为false。 如果设置为true，则提供调试信息   options 要转发到底层的Werkzeug服务器
    app = create_app()
    app.run(debug=True)
