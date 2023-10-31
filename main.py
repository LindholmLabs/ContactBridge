from flask import Flask
from WebAPI import blueprint as api_blueprint
from WebInterface import web_interface
import os

app = Flask(__name__)
app.register_blueprint(api_blueprint, url_prefix='/api')
app.register_blueprint(web_interface)
app.secret_key = os.urandom(24)

if __name__ == '__main__':
    app.run(debug=True)