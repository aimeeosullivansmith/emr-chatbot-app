from flask import Blueprint, jsonify

main = Blueprint('main', __name__)

@main.route("/")
def index():
    return "Hello World!"

@main.route("/api/hello", methods=["GET"])
def hello():
    return jsonify({"tester": "Hello from Flask!"})