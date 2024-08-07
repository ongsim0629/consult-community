import os
from flask import Blueprint, jsonify, render_template, redirect, flash
from dotenv import load_dotenv
from bson import ObjectId
from pymongo import MongoClient
from datetime import datetime
from constants.python.page_urls import PAGE_URLS
from .auth import (
    decode_access_token,
    get_token_from_header,
)

load_dotenv()
MONGO_DB_URI = os.environ.get("MONGO_DB_URI")
MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME")

concern_list_bp = Blueprint("concern_list_bp", __name__)

client = MongoClient(MONGO_DB_URI)
db = client[MONGO_DB_NAME]


def createNow():
    return datetime.now()


def strToBool(s):
    return s == "true"


## concernList 화면 렌더링
@concern_list_bp.route(PAGE_URLS["HOME"], methods=["GET"])
def getConcernList():

    topList = list(db.concerns.find({}).sort({"view_count": -1}).limit(5))
    concernList = list(db.concerns.find({}).sort({"created_at": -1}))

    for i in topList:
        i["_id"] = str(i["_id"])
        if i.get("revealed") is False:
            i["created_by"] = "익명스님"
        i["created_at"] = i["created_at"].strftime("%Y년 %m월 %d일 %H시 %M분")

    for i in concernList:
        i["_id"] = str(i["_id"])
        i["created_at"] = i["created_at"].strftime("%Y년 %m월 %d일 %H시 %M분 %S초")
        if i.get("revealed") is False:
            i["created_by"] = "익명스님"

    ## TODO: 무한 스크롤(페이징) 고민
    return render_template("concernList.html", topList=topList, concernList=concernList)


@concern_list_bp.route("/api/concerns", methods=["GET"])
def get_concerns_by_user():

    token = get_token_from_header()

    if not token:
        flash("토큰이 없습니다. 로그인해주세요")
        return redirect(PAGE_URLS["SIGN_IN"])

    # TODO: 토큰 만료 재현
    # expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoidGVzdGVyMTIzNDUiLCJuaWNrbmFtZSI6InRlc3Rlcl9uaWNrbmFtZTEyMzQ1IiwiZXhwIjoxNzIyOTQ3MDIwfQ.8rFaJnbOpJa-6YEeEVh2LYk0kzXARg7EAD8TNLI3fAE"
    user_dict, error = decode_access_token(token)

    if error:
        flash("토큰이 만료되었습니다. 재로그인해주세요")
        return redirect(PAGE_URLS["SIGN_IN"])

    ## ===== TODO: (끝) 분리 고민 필요 =====

    nickname = user_dict["nickname"]

    print("nickname", nickname)

    data = list(db.concerns.find({"created_by": nickname}).sort({"created_at": -1}))

    for i in data:
        i["_id"] = str(i["_id"])
        i["created_at"] = i["created_at"].strftime("%Y년 %m월 %d일 %H시 %M분 %S초")

    ## TODO: 무한 스크롤(페이징) 고민
    return jsonify({"data": data}), 200


## concernList 화면 렌더링 테스트용
@concern_list_bp.route(PAGE_URLS["HOME"] + "/test", methods=["GET"])
def getConcernListTest():

    topList = list(db.concerns.find({}).sort({"view_count": -1}).limit(5))

    concernList = list(db.concerns.find({}).sort({"created_at": 1}))

    for i in topList:
        i["_id"] = str(i["_id"])

    for i in concernList:
        i["_id"] = str(i["_id"])

    return jsonify(
        {
            "result": "success",
            "topList": topList,
            "concernList": concernList,
            "msg": "getConcernList 성공!",
        }
    )
    ## TODO : 추후 삭제
