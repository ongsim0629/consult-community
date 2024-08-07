import os
from flask import Blueprint, jsonify, render_template, request, redirect
from dotenv import load_dotenv
from bson import ObjectId
from pymongo import MongoClient
from datetime import datetime

load_dotenv()
MONGO_DB_URI = os.environ.get("MONGO_DB_URI")
MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME")

concern_bp = Blueprint("concern_bp", __name__)

client = MongoClient(MONGO_DB_URI)
db = client[MONGO_DB_NAME]

now = datetime.now()


def strToBool(s):
    return s == "true"


## concernList 화면 렌더링
@concern_bp.route("/concern/concernList", methods=["GET"])
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
@concern_bp.route("/concern/concernList/test", methods=["GET"])
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


## addConcern 화면 렌더링
@concern_bp.route("/concern/add", methods=["GET"])
def addConcernForm():

    return render_template("addConcern.html")


## addConcern에서 고민 추가
@concern_bp.route("/concern/add", methods=["POST"])
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
    return redirect("/concern/concernList")
    # return jsonify({'result': 'success', 'msg':'addConcern 성공!'})
    ## TODO : 위에꺼 없애고 만들어진 고민으로 리다이렉트
    ## : JWT에서 닉네임 받기
    ## : revealed 저장하는 방식 생각해보기
    ## : 날짜 저장하는 방식 생각해보기


## concernDetail 화면 렌더링
@concern_bp.route("/concern/detail", methods=["GET"])
def getConcernDetail():
    ## 쿼리스트링에서 고민 id 받기
    concernId = request.args.get("concern_id")
    concern = db.concerns.find_one({"_id": ObjectId(concernId)})
    concern["_id"] = str(
        concern["_id"]
    )  # ObjectId는 Json 안에 담을 수 없다. String으로 바꿔줄 것
    solutions = list(db.concerns.find({"concern_id": concernId}))

    return render_template("concernDetail.html", concern=concern, solutions=solutions)

    # return jsonify({'result':'success', 'concern':concern, 'solutions':solutions, 'msg':'getConcernDetail 성공!'})


## solution 생성 (API)
@concern_bp.route("/concern/solution", methods=["POST"])
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
@concern_bp.route("/concern/solution/<concern_id>", methods=["DELETE"])
def deleteSolution(concern_id):
    db.todos.delete_one({"_id": ObjectId(concern_id)})
    return jsonify({"result": "success", "msg": "deleteSolution 완료!"})
