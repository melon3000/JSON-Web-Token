
import os
from datetime import datetime, timedelta, timezone

import jwt
from flask import Flask, jsonify, request

app = Flask(__name__)

SECRET_KEY = os.environ.get("JWT_SECRET")
if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET keskkonnamuutuja puudub!")

ALGORITHM = "HS256"

# Näidiskasutajad
USERS = {
    "student": {"password": "student123", "role": "student"},
    "admin": {"password": "admin123", "role": "admin"}
}


# 1. Sisselogimine ja JWT väljastamine
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}

    username = data.get("username")
    password = data.get("password")

    user = USERS.get(username)

    if not user or user["password"] != password:
        return jsonify({"error": "Vale kasutajanimi või parool"}), 401

    now = datetime.now(timezone.utc)

    payload = {
        "sub": username,
        "role": user["role"],
        "iat": now,
        "exp": now + timedelta(minutes=5)
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return jsonify({"token": token}), 200


# Funktsioon tokeni kontrollimiseks
def get_token_data():
    auth_header = request.headers.get("Authorization", "")
    parts = auth_header.split()

    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None, (jsonify({"error": "Token puudub"}), 401)

    token = parts[1]

    try:
        data = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"],
            options={"require": ["sub", "role", "exp"]}
        )
        return data, None

    except jwt.ExpiredSignatureError:
        return None, (jsonify({"error": "Token on aegunud"}), 401)

    except jwt.InvalidTokenError:
        return None, (jsonify({"error": "Vigane token"}), 401)


# 2. Profiili vaatamine
@app.route("/profiil", methods=["GET"])
def profiil():
    data, error = get_token_data()

    if error:
        return error

    return jsonify({
        "sub": data["sub"],
        "role": data["role"],
        "exp": data["exp"]
    }), 200


# 3. Admini ligipääs
@app.route("/admin", methods=["GET"])
def admin():
    data, error = get_token_data()

    if error:
        return error

    if data["role"] != "admin":
        return jsonify({"error": "Ligipääs keelatud"}), 403

    return jsonify({
        "message": "Admini ligipääs lubatud",
        "user": data["sub"]
    }), 200


if __name__ == "__main__":
    app.run(debug=False)
