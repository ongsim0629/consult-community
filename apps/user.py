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
COLLECTION_NAME = 'users'

user_bp = Blueprint('user_bp', __name__)

client = MongoClient(MONGO_DB_URI)
db = client[MONGO_DB_NAME]

class UserObject:
    def __init__(self, user_id, nickname):
        self.user_id = user_id
        self.nickname = nickname
        
    def to_dict(self):
        """Convert UserObject to a dictionary."""
        return {
            'user_id': self.user_id,
            'nickname': self.nickname
        }

def create_access_token(user_obj):
    """Create JWT access token"""
    expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)

    token = jwt.encode({
        **user_obj.to_dict(),
        'exp': expiration
    }, SECRET_KEY, algorithm='HS256')
    return token


def decode_access_token(token):
    """Decode JWT access token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_dict = UserObject(payload['user_id'], payload['nickname']).to_dict()
        return user_dict, None
    except jwt.ExpiredSignatureError:
        return None, 'Token has expired'
    except jwt.InvalidTokenError:
        return None, 'Invalid token'


def get_token_from_header():
    """Extracts the token from the Authorization header"""
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
        return token
    return None

# 회원가입
@user_bp.route('/api/user/sign-up', methods=["POST"])
def todo():  
    data=request.get_json()
    user_id = data.get('user_id')
    user_pw=data.get('password')
    nickname=data.get('nickname')
    
    # 1. client 요청 유효성 체크
    if not user_id:
        return jsonify({
            "message": "user_id를 입력해주세요"
        }), 400

    elif not user_pw:
        return jsonify({
            "message": "pw를 입력해주세요"
        }), 400
    
    elif not nickname:
        return jsonify({
            "messsage": "nickname을 입력해주세요"
        }), 400
    
    # 2. 중복 유저 체크
    user_by_id = db[COLLECTION_NAME].find_one({"user_id": user_id})
    if user_by_id:
        return jsonify({
            "message": "중복된 아이디 입니다."
        }), 409
        
    user_by_nickname = db[COLLECTION_NAME].find_one({"nickname": nickname})
    if user_by_nickname:
        return jsonify({
            "message": "중복된 닉네임 입니다."
        }), 409

    # 3. 비로소 생성 완료
    user = db[COLLECTION_NAME].insert_one({
        "user_id": user_id,
        "password": user_pw,
        "nickname": nickname
    })
    
    return jsonify({
        "message": "생성 완료되었습니다."
    }), 201


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
        
    user = db[COLLECTION_NAME].find_one({"user_id": user_id, "password": user_pw})

    if user:
        user_obj = UserObject(user['user_id'], user['nickname'])
        access_token = create_access_token(user_obj)
        return jsonify({
            "access_token": access_token
        }), 200
        
    else:
        return jsonify({
            "message": "존재하지 않는 유저입니다."
        }), 404


@user_bp.route('/api/user/info', methods=["GET"])
def get_user_info():
    token = get_token_from_header()
    
    if not token:
        return({ "message": "Token is missing" }), 403
    
    user_dict, error = decode_access_token(token)
        
    if error:
        return({ "message": error }), 403
    
    user_id = user_dict['user_id']
    nickname = user_dict['nickname']
    
    return jsonify({
        'user_id': user_id,
        'nickname': nickname
    }), 200
    

# @user_bp.route('/api/user/set-pw', methods=["POST"])

