# from app import init_app
import src

app = src.init_app()

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# db = SQLAlchemy(app)

if __name__ == "__main__":
	app.run(debug = False, port=33507)
