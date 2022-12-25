import sqlite3
from base64 import urlsafe_b64decode, urlsafe_b64encode
from typing import Optional

from flask import send_file  # type: ignore
from flask import Flask, abort, jsonify, request

app = Flask(__name__)
DATABASE = "1.db"


@app.get("/<path:hash>")
def get(hash: str):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    rowid = int(urlsafe_b64decode(hash))
    res: Optional[tuple[str]] = cur.execute(
        "SELECT url FROM urls WHERE rowid = ?", [rowid]
    ).fetchone()
    if not res:
        abort(404)
    url = res[0]
    return f'<script>location.replace("{url}")</script>'


@app.post("/")
def post():
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    if not request.json or "url" not in request.json:
        return jsonify({"success": False})
    url: str = request.json["url"]
    if len(url) > 256:
        return jsonify({"success": False})
    con.execute("INSERT INTO urls (url) VALUES (?)", [url])
    con.commit()
    rowid: int = cur.execute("SELECT last_insert_rowid()").fetchone()[0]
    hash = urlsafe_b64encode(str(rowid).encode("ascii")).decode("ascii")
    return jsonify({"success": True, "hash": hash})


@app.get("/")
def fe():
    return send_file("fe.html")
