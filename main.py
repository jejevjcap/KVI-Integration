import os
from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from flask_migrate import Migrate  # Import Flask-Migrate
from dotenv import load_dotenv
from models.user import db
from controller import authentication
from flask_jwt_extended import JWTManager

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Setup database URI using environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional, for reducing overhead
# JWT Setup
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "your_secret_key_here")
jwt = JWTManager(app)
# Initialize db instance
db.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Swagger UI setup
SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': 'KVI API'}
)

app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# Route to register a new user
@app.route("/register", methods=["POST"])
def register():
    return authentication.signup()
# Route to authenticate a user (login)
@app.route("/auth", methods=["POST"])
def auth():
    return authentication.login()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
