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

concern_add_bp = Blueprint("concern_add_bp", __name__)

client = MongoClient(MONGO_DB_URI)
db = client[MONGO_DB_NAME]

now = datetime.now()


def strToBool(s):
    return s == "true"


## addConcern 화면 렌더링
@concern_add_bp.route(PAGE_URLS["CONCERN_ADD"], methods=["GET"])
def addConcernForm():

    return render_template("addConcern.html")


## addConcern에서 고민 추가
@concern_add_bp.route(PAGE_URLS["CONCERN_ADD"], methods=["POST"])
def addConcern():
    formData = request.form
    concernData = {
        "title": formData["title"],
        "content": formData["content"],
        "revealed": strToBool(formData["revealed"]),
        "view_count": 0,
        "created_at": now,
        "created_by": "닉네임TEST1",  # 토큰에서 값 가져온다.
        "updated_at": now,
    }
    print(concernData)

    insertData = db.concerns.insert_one(concernData)
    print(concernData)

    return redirect(PAGE_URLS["HOME"])
    ## TODO : 위에꺼 없애고 만들어진 고민으로 리다이렉트
    ## : JWT에서 닉네임 받기
