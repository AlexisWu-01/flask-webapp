from flask import Flask

def init_app():
    """
    Set app variable to be Flask application.
    """
    app = Flask(__name__)  #instance_relative_config=False)
    # app.config.from_object('config.Config')
    

    with app.app_context():
        # Import Routes and other core parts
        import src.routes as routes

        from src.data_exploration_tool import init_dashboard
        app = init_dashboard(app)

        return app