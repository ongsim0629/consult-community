import os
from flask import Blueprint, jsonify, render_template, request, redirect
from dotenv import load_dotenv
from bson import ObjectId
from pymongo import MongoClient
from datetime import datetime
from constants.python.page_urls import PAGE_URLS
from .utils import formatDateTimeToStr


load_dotenv()
MONGO_DB_URI = os.environ.get("MONGO_DB_URI")
MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME")

concern_detail_bp = Blueprint("concern_detail_bp", __name__)

client = MongoClient(MONGO_DB_URI)
db = client[MONGO_DB_NAME]


def createNow():
    return datetime.now()


def strToBool(s):
    return s == "true"


## concernDetail 화면 렌더링
@concern_detail_bp.route(PAGE_URLS["CONCERN_DETAIL"], methods=["GET"])
def getConcernDetail():
    ## 쿼리스트링에서 고민 id 받기
    concernId = request.args.get("concern_id")
    concern = db.concerns.find_one({"_id": ObjectId(concernId)})
    concern["_id"] = str(
        concern["_id"]
    )  # ObjectId는 Json 안에 담을 수 없다. String으로 바꿔줄 것

    nickname_concern_creator = concern["created_by"]

    solutions = list(db.concerns.find({"concern_id": concernId}))

    # revealed가 "false"이면 alias를 "익명스님"으로 설정 -> 지금 db에 불린 false랑 string flase 혼재 중 -> 수정
    alias = "익명스님" if concern.get("revealed") is False else None

    ## 수정시 조회수 +1 안 하기 위한 쿼리 파라미터
    flag = request.args.get("flag", "false")

    if not strToBool(flag):
        db.concerns.update_one(
            {"_id": ObjectId(concernId)}, {"$inc": {"view_count": 1}}
        )

    return render_template(
        "concernDetail.html",
        concern=concern,
        solutions=solutions,
        alias=alias,
        nickname_concern_creator=nickname_concern_creator,
    )

## solution 조회 (API)
@concern_detail_bp.route("/concern/solution", methods=["GET"])
def getSolution():
    concernId = request.args.get("concernId")

    solutions = list(
        db.solutions.find({"concern_id": concernId}).sort({"created_at": -1})
    )

    for i in solutions:
        i["_id"] = str(i["_id"])
        i["created_at"] = formatDateTimeToStr(i["created_at"])

    concern = db.concerns.find_one({"_id": ObjectId(concernId)})
    concernNickname = concern["created_by"]

    return jsonify(
        {
            "result": "success",
            "solutions": solutions,
            "concernNickname": concernNickname,
            "msg": "getSolution 성공!",
        }
    )


## solution 생성 (API)
@concern_detail_bp.route("/concern/solution", methods=["POST"])
def addSolution():
    formData = request.form

    now = createNow()
    solutionData = {
        "content": formData["content"],
        "revealed": strToBool(formData["revealed"]),
        "concern_id": formData["concern_id"],
        "concerned_by": formData["concerned_by"],
        "created_at": now,
        "created_by": formData["user_nickname"],
        "updated_at": now,
    }
    db.solutions.insert_one(solutionData)
    return jsonify({"result": "success", "msg": "addSolution 성공!"})


## solution 삭제 (API)
@concern_detail_bp.route("/concern/solution/<solution_id>", methods=["DELETE"])
def deleteSolution(solution_id):
    db.solutions.delete_one({"_id": ObjectId(solution_id)})
    return jsonify({"result": "success", "msg": "deleteSolution 완료!"})
