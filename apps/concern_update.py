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
    return 1


## Concern 업데이트
@concern_update_bp.route(PAGE_URLS["CONCERN_EDIT"], methods=["POST"])
def updateConcern():
    return 1


## Concern 삭제 (API)
@concern_update_bp.route("/concern/delete", methods=["DELETE"])
def deleteConcern():
    return 1
