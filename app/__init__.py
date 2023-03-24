from flask_cors import CORS

from app.route import route
from app.app import Flask

def create_app():
    app = Flask(__name__)
    # 设置允许跨域
    CORS(app, supports_credentials=True)
    route(app)
    return app