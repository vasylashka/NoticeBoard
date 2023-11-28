from flask import Flask, request, jsonify, json, render_template
from flask_mongoengine import MongoEngine
from flask_swagger_ui import get_swaggerui_blueprint

import controllers.user_routes
import controllers.note_routes
from werkzeug.exceptions import HTTPException


app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'NoticeBoard',
    'host': 'mongodb://localhost:27017/NoticeBoard'
}

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "NoticeBoard API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

app.register_blueprint(controllers.user_routes.blp, url_prefix='/api/v1/user')
app.register_blueprint(controllers.note_routes.blp, url_prefix='/api/v1/note')

db = MongoEngine(app)


@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code

if __name__ == '__main__':
    app.run(debug=True)
