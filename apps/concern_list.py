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

concern_list_bp = Blueprint("concern_list_bp", __name__)

client = MongoClient(MONGO_DB_URI)
db = client[MONGO_DB_NAME]

now = datetime.now()


def strToBool(s):
    return s == "true"


## concernList 화면 렌더링
@concern_list_bp.route(PAGE_URLS["HOME"], methods=["GET"])
def getConcernList():

    topList = list(db.concerns.find({}).sort("view_count", -1).limit(5))

    concernList = list(db.concerns.find({}).sort("created_at", -1))

    for i in topList:
        i["_id"] = str(i["_id"])

    for i in concernList:
        i["_id"] = str(i["_id"])

    return render_template("concernList.html", topList=topList, concernList=concernList)
    ## 무한 스크롤(페이징) 고민


## concernList 화면 렌더링 테스트용
@concern_list_bp.route(PAGE_URLS["HOME"] + "/test", methods=["GET"])
def getConcernListTest():

    topList = list(db.concerns.find({}).sort("view_count", -1).limit(5))

    concernList = list(db.concerns.find({}).sort("created_at", 1))

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
