from flask import Flask, render_template, jsonify, request
from apps.concern import concern_bp

app = Flask(__name__)

## blueprint 등록
app.register_blueprint(concern_bp)

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)