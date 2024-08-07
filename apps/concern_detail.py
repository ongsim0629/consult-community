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

concern_detail_bp = Blueprint("concern_detail_bp", __name__)

client = MongoClient(MONGO_DB_URI)
db = client[MONGO_DB_NAME]

now = datetime.now()


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

    return render_template(
        "concernDetail.html",
        concern=concern,
        solutions=solutions,
        nickname_concern_creator=nickname_concern_creator,
    )

    # return jsonify({'result':'success', 'concern':concern, 'solutions':solutions, 'msg':'getConcernDetail 성공!'})


## solution 생성 (API)
@concern_detail_bp.route("/concern/solution", methods=["POST"])
def addSolution():
    formData = request.form
    print(formData)
    solutionData = {
        "content": formData["content"],
        "revealed": strToBool(formData["revealed"]),
        "concern_id": formData["concern_id"],
        "concerned_by": formData["concerned_by"],
        "created_at": now,
        "created_by": "고민해결자 TEST1",
        "updated_at": now,
    }
    db.solutions.insert_one(solutionData)
    return jsonify({"result": "success", "msg": "addSolution 성공!"})


## solution 삭제 (API)
@concern_detail_bp.route("/concern/solution/<concern_id>", methods=["DELETE"])
def deleteSolution(concern_id):
    db.todos.delete_one({"_id": ObjectId(concern_id)})
    return jsonify({"result": "success", "msg": "deleteSolution 완료!"})
