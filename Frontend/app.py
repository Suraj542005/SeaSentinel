import os
from flask import Flask, request, jsonify
from functools import wraps
from dotenv import load_dotenv
from jwt_utils import verify_clerk_token
import requests

load_dotenv()

app = Flask(__name__)

CLERK_API_KEY = os.getenv("CLERK_API_KEY")


def require_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid Authorization header"}), 401

        token = auth_header.split(" ")[1]
        try:
            user = verify_clerk_token(token)
        except Exception as e:
            return jsonify({"error": str(e)}), 401

        request.user = user
        return f(*args, **kwargs)
    return wrapper


@app.route("/")
def home():
    return {"message": "Hello from Flask + Clerk!"}


@app.route("/protected")
@require_auth
def protected():
    return jsonify({
        "message": "Access granted ✅",
        "user": request.user
    })


@app.route("/profile")
@require_auth
def profile():
    """Fetch full Clerk user profile using Admin API"""
    user_id = request.user["sub"]  # Clerk user ID
    headers = {"Authorization": f"Bearer {CLERK_API_KEY}"}
    res = requests.get(f"https://api.clerk.dev/v1/users/{user_id}", headers=headers)

    if res.status_code != 200:
        return {"error": "Failed to fetch user profile"}, res.status_code

    return res.json()


if __name__ == "__main__":
    app.run(debug=True, port=5000)

