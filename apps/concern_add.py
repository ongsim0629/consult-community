import os
from flask import Blueprint, jsonify, render_template, request, redirect, url_for
from dotenv import load_dotenv
from bson import ObjectId
from pymongo import MongoClient
from datetime import datetime
from .auth import (
    UserObject,
    create_access_token,
    decode_access_token,
    get_token_from_header,
)

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
@concern_add_bp.route("/concern/add", methods=["GET"])
def addConcernForm():

    return render_template("addConcern.html")


## addConcern에서 고민 추가
@concern_add_bp.route("/concern/add", methods=["POST"])
def addConcern():
    formData = request.form
    print(formData)


    concernData = {
        "title": formData["title"],
        "content": formData["content"],
        "revealed": strToBool(formData["revealed"]),
        "view_count": 0,
        "created_at": now,
        "created_by": formData["user_id"],
        "updated_at": now,
    }
    insertData = db.concerns.insert_one(concernData)
    concernId = str(insertData.inserted_id)
    return redirect(url_for("concern_detail_bp.getConcernDetail", concern_id=concernId))
