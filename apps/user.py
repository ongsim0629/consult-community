import os
from flask import Blueprint, jsonify, request
from dotenv import load_dotenv
from bson import ObjectId
from pymongo import MongoClient

import datetime
import jwt

load_dotenv()
MONGO_DB_URI = os.environ.get("MONGO_DB_URI")
MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME")
SECRET_KEY = os.environ.get("SECRET_KEY")

user_bp = Blueprint('user_bp', __name__)
client = MongoClient(MONGO_DB_URI)
db = client[MONGO_DB_NAME]

def create_access_token(identity):
    """Create JWT access token"""
    expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    token = jwt.encode({
        'identity': identity,
        'exp': expiration
    }, SECRET_KEY, algorithm='HS256')
    return token

#'localhost:3000/user/sign-up' #화면을 불러올때는
# 회원가입
@user_bp.route('/api/user/sign-up', methods=["POST"])
def todo():  
    return {}


# 로그인
@user_bp.route('/api/user/sign-in', methods=["POST"])
def signin():
    data=request.get_json()
    user_id = data.get('user_id')
    user_pw=data.get('password')

    if not user_id:
        return jsonify({
            "message": "user_id를 입력해주세요"
        }), 400

    elif not user_pw:
        return jsonify({
            "message": "pw를 입력해주세요"
        }), 400
        
    user = db.users.find_one({"user_id": user_id, "password": user_pw})

    if user:
        access_token = create_access_token(identity=user_id)
        return jsonify({
            "access_token": access_token
        }), 200
        
    else:
        return jsonify({
            "message": "존재하지 않는 유저입니다."
        }), 404

# @user_bp.route('/api/user/set-pw', methods=["POST"])

