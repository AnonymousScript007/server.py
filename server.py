from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def db():
    return sqlite3.connect("database.db")

@app.route("/save", methods=["POST"])
def save():
    data = request.json
    user = data["user"]
    x = data["x"]
    y = data["y"]

    conn = db()
    c = conn.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS players (id TEXT, x INT, y INT)")
    c.execute("DELETE FROM players WHERE id=?", (user,))
    c.execute("INSERT INTO players VALUES (?,?,?)", (user, x, y))

    conn.commit()
    conn.close()

    return jsonify({"status": "ok"})

@app.route("/load/<user>")
def load(user):
    conn = db()
    c = conn.cursor()

    c.execute("SELECT x,y FROM players WHERE id=?", (user,))
    row = c.fetchone()

    conn.close()

    if row:
        return jsonify({"x": row[0], "y": row[1]})
    return jsonify({"x":100, "y":100})

import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
