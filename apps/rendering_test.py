import os
from flask import Blueprint, render_template

rendering_bp = Blueprint("rendering_bp", __name__)


@rendering_bp.route("/signup")
def signup():
    return render_template("signUp.html")


@rendering_bp.route("/signin")
def signin():
    return render_template("signIn.html")


@rendering_bp.route("/concerns")
def concerns():
    return render_template("concernList.html")


@rendering_bp.route("/addconcern")
def addconcern():
    return render_template("addConcern.html")


@rendering_bp.route("/editconcern")
def editconcern():
    return render_template("editConcern.html")


@rendering_bp.route("/concerndetail")
def concerndetail():
    return render_template("concernDetail.html")


@rendering_bp.route("/mypage")
def mypage():
    return render_template("myPage.html")
