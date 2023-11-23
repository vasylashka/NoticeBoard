from flask import Flask, send_from_directory
from flask_mongoengine import MongoEngine
from flask_swagger_ui import get_swaggerui_blueprint
from ORM.user import User

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'NoticeBoard',
    'host': 'mongo'
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


db = MongoEngine(app)


@app.route('/api/v1/hello-world-3')
def hello():
    return 'Hello, World 3', 200


if __name__ == '__main__':
    app.run(debug=True)
