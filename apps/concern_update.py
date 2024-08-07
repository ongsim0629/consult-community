import os
from flask import Blueprint, jsonify, render_template, request, redirect
from dotenv import load_dotenv
from bson import ObjectId
from pymongo import MongoClient
from datetime import datetime
from constants.python.page_urls import PAGE_URLS

load_dotenv()
MONGO_DB_URI = os.environ.get("MONGO_DB_URI")
MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME")

concern_update_bp = Blueprint("concern_update_bp", __name__)

client = MongoClient(MONGO_DB_URI)
db = client[MONGO_DB_NAME]

now = datetime.now()


def strToBool(s):
    return s == "true"


## updateConcern 렌더링
@concern_update_bp.route(PAGE_URLS["CONCERN_EDIT"], methods=["GET"])
def updateConcernForm():
    # 먼저 고민 아이디 받아와서
    concernId = request.args.get("concern_id")
    concern = db.concerns.find_one({"_id": ObjectId(concernId)})
    
    return render_template("editConcern.html", concern=concern)


## Concern 업데이트
@concern_update_bp.route(PAGE_URLS["CONCERN_EDIT"], methods=["POST"])
def updateConcern():
    data = request.get_json()
    new_title = data.get('new_title')
    new_content = data.get('new_content')
    concernId = data.get('concern_id')
    revealed = data.get('revealed')
    
    if not all([new_title, new_content, concernId, revealed]):
        return jsonify({"message": "모든 필드를 입력해주세요."}), 400
    
    db.concerns.update_one({"_id": ObjectId(concernId)}, {'$set': {"title": new_title, "content": new_content, "revealed": strToBool(revealed)}})
    
    return jsonify({"message": "업데이트되었습니다."}), 200



## Concern 삭제 (API)
@concern_update_bp.route("/concern/delete", methods=["DELETE"])
def deleteConcern():
    data = request.get_json()
    concernId = data.get('concern_id')
    
    if concernId:
        db.concerns.delete_one({"_id": ObjectId(concernId)})
        return jsonify({"message": "삭제되었습니다."}), 200
    else:
        return jsonify({"message": "삭제에 실패했습니다."}), 400
