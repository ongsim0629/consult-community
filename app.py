from flask import Flask
from apps.concern import concern_bp
from apps.user import user_bp

app = Flask(__name__)

app.register_blueprint(user_bp)
app.register_blueprint(concern_bp)

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)