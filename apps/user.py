import os
from flask import Blueprint, jsonify, request
from dotenv import load_dotenv
from bson import ObjectId
from pymongo import MongoClient
from .auth import (
    UserObject,
    create_access_token,
    decode_access_token,
    get_token_from_header,
)

load_dotenv()
MONGO_DB_URI = os.environ.get("MONGO_DB_URI")
MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME")
COLLECTION_NAME = "users"

user_bp = Blueprint("user_bp", __name__)

client = MongoClient(MONGO_DB_URI)
db = client[MONGO_DB_NAME]


# 회원가입
@user_bp.route("/api/user/sign-up", methods=["POST"])
def signup():
    data = request.get_json()
    user_id = data.get("user_id")
    user_pw = data.get("password")
    nickname = data.get("nickname")

    # 1. client 요청 유효성 체크
    if not user_id:
        return jsonify({"message": "user_id를 입력해주세요"}), 400

    elif not user_pw:
        return jsonify({"message": "pw를 입력해주세요"}), 400

    elif not nickname:
        return jsonify({"messsage": "nickname을 입력해주세요"}), 400

    # 2. 중복 유저 체크
    user_by_id = db[COLLECTION_NAME].find_one({"user_id": user_id})
    if user_by_id:
        return jsonify({"message": "중복된 아이디 입니다."}), 409

    user_by_nickname = db[COLLECTION_NAME].find_one({"nickname": nickname})
    if user_by_nickname:
        return jsonify({"message": "중복된 닉네임 입니다."}), 409

    # 3. 비로소 생성 완료
    user = db[COLLECTION_NAME].insert_one(
        {"user_id": user_id, "password": user_pw, "nickname": nickname}
    )

    return jsonify({"message": "생성 완료되었습니다."}), 201


# 로그인
@user_bp.route("/api/user/sign-in", methods=["POST"])
def signin():
    data = request.get_json()
    user_id = data.get("user_id")
    user_pw = data.get("password")

    if not user_id:
        return jsonify({"message": "user_id를 입력해주세요"}), 400

    elif not user_pw:
        return jsonify({"message": "pw를 입력해주세요"}), 400

    user = db[COLLECTION_NAME].find_one({"user_id": user_id, "password": user_pw})

    if user:
        user_obj = UserObject(user["user_id"], user["nickname"])
        access_token = create_access_token(user_obj)
        return jsonify({"access_token": access_token}), 200

    else:
        return jsonify({"message": "존재하지 않는 유저입니다."}), 404


@user_bp.route("/api/user/info", methods=["GET"])
def get_user_info():

    ## ===== TODO: (시작) 분리 고민 필요 =====
    token = get_token_from_header()

    if not token:
        return ({"message": "Token is missing"}), 403

    user_dict, error = decode_access_token(token)

    if error:
        return ({"message": error}), 403

    ## ===== TODO: (끝) 분리 고민 필요 =====

    user_id = user_dict["user_id"]
    nickname = user_dict["nickname"]

    return jsonify({"user_id": user_id, "nickname": nickname}), 200


@user_bp.route("/api/user/pw", methods=["POST"])
def update_password():
    token = get_token_from_header()

    if not token:
        return jsonify({"message": "Token is missing"}), 403

    data = request.get_json()
    old_pw = data.get("old_pw")
    new_pw = data.get("new_pw")

    user_dict, error = decode_access_token(token)
    if error:
        return jsonify({"message": error}), 403

    filter = {"user_id": user_dict["user_id"]}
    user = db[COLLECTION_NAME].find_one(filter)
    if old_pw != user["password"]:
        return jsonify({"message": "이전 비번을 다시 확인해주세요"}), 400

    try:
        new_user = {"$set": {"password": new_pw}}
        db[COLLECTION_NAME].update_one(filter, new_user)

        return jsonify({"message": "비번 변경을 완료했어요"}), 200

    except:
        return jsonify({"message": "잠시 후 다시 시도해주세요"}), 500
