import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from pymongo import MongoClient
from .auth import decode_access_token
from constants.python.page_urls import PAGE_URLS
from .utils import createNow

load_dotenv()
MONGO_DB_URI = os.environ.get("MONGO_DB_URI")
MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME")

concern_add_bp = Blueprint("concern_add_bp", __name__)

client = MongoClient(MONGO_DB_URI)
db = client[MONGO_DB_NAME]


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

    token = formData["token"]

    if not token:
        flash("토큰이 없습니다. 로그인해주세요")
        return redirect(PAGE_URLS["SIGN_IN"])

    user_dict, error = decode_access_token(token)

    if error:
        flash("토큰이 만료되었습니다. 재로그인해주세요")
        return redirect(PAGE_URLS["SIGN_IN"])

    nickname = user_dict["nickname"]

    now = createNow()
    concernData = {
        "title": formData["title"],
        "content": formData["content"],
        "revealed": strToBool(formData["revealed"]),
        "view_count": 0,
        "created_at": now,
        "created_by": nickname,
        "updated_at": now,
    }
    insertData = db.concerns.insert_one(concernData)
    concernId = str(insertData.inserted_id)
    return redirect(url_for("concern_detail_bp.getConcernDetail", concern_id=concernId))
    # TODO : page URL 상수와 연결되어있지 않음
