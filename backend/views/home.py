from flask import Blueprint, render_template

default_bp = Blueprint("default", __name__)


@default_bp.route("/")
def home():
    return render_template("home.html")
