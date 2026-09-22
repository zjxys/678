from __future__ import annotations

import os

from flask import Flask, render_template, request, jsonify, redirect, url_for

from config import Config
from core.grader import EssayGrader

app = Flask(__name__)
app.config.from_object(Config)

grader = EssayGrader()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/grade", methods=["POST"])
def grade():
    title = request.form.get("title", "").strip()
    text = request.form.get("essay", "").strip()

    if not text:
        return render_template(
            "index.html",
            error="请输入作文内容",
            title=title,
        )

    result = grader.grade(text, title)
    return render_template("result.html", result=result)


@app.route("/api/grade", methods=["POST"])
def api_grade():
    data = request.get_json(silent=True)
    if not data or "essay" not in data:
        return jsonify({"error": "缺少 essay 字段"}), 400

    title = data.get("title", "").strip()
    text = data["essay"].strip()

    if not text:
        return jsonify({"error": "作文内容不能为空"}), 400

    result = grader.grade(text, title)
    return jsonify(result.to_dict())


@app.route("/api/criteria", methods=["GET"])
def api_criteria():
    from core.criteria import get_criteria_summary
    return jsonify(get_criteria_summary())


if __name__ == "__main__":
    app.run(
        host=app.config["HOST"],
        port=app.config["PORT"],
        debug=app.config["DEBUG"],
    )
