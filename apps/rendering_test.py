import os
from flask import Blueprint, render_template
from constants.python.page_urls import PAGE_URLS

rendering_bp = Blueprint("rendering_bp", __name__)


@rendering_bp.route(PAGE_URLS["SIGN_UP"])
def signup():
    return render_template("signUp.html")


@rendering_bp.route(PAGE_URLS["SIGN_IN"])
def signin():
    return render_template("signIn.html")


@rendering_bp.route(PAGE_URLS["CONCERN_LIST"])
def concerns():
    return render_template("concernList.html")


@rendering_bp.route(PAGE_URLS["CONCERN_ADD"])
def addconcern():
    return render_template("addConcern.html")


@rendering_bp.route(PAGE_URLS["CONCERN_EDIT"])
def editconcern():
    return render_template("editConcern.html")


@rendering_bp.route(PAGE_URLS["CONCERN_DETAIL"])
def concerndetail():
    return render_template("concernDetail.html")


@rendering_bp.route(PAGE_URLS["MYPAGE"])
def mypage():
    return render_template("myPage.html")
