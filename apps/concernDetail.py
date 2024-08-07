import os
from flask import Blueprint, jsonify, render_template, request, redirect
from dotenv import load_dotenv
from bson import ObjectId
from pymongo import MongoClient
from datetime import datetime

load_dotenv()
MONGO_DB_URI = os.environ.get("MONGO_DB_URI")
MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME")

concern_detail_bp = Blueprint("concern_detail_bp", __name__)

client = MongoClient(MONGO_DB_URI)
db = client[MONGO_DB_NAME]

now = datetime.now()


def strToBool(s):
    return s == "true"


# ## updateConcern 렌더링
# @concern_bp.route('/concern/update', methods=['GET']) ## 파라미터 넣는법 찾아볼것
# def updateConcernForm():

# ## Concern 업데이트
# @concern_bp.route('/concern/update', methods=['POST']) ## 파라미터 넣는법 찾아볼것
# def updateConcern():

# ## Concern 삭제 (API)
# @concern_bp.route('/concern/delete', methods=['DELETE']) ## 파라미터 넣는법 찾아볼것
# def deleteConcern():
