from flask import Flask, jsonify, render_template
from flask_migrate import Migrate
from flask_swagger_ui import get_swaggerui_blueprint
from werkzeug.exceptions import HTTPException
import static
from controllers.note_routes import blp as note_blp
from controllers.user_routes import blp as user_blp
from database import db

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///NoticeBoard.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "NoticeBoard API"
    }
)

@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code


app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
app.register_blueprint(user_blp, url_prefix='/api/v1/users')
app.register_blueprint(note_blp, url_prefix='/api/v1/notes')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
