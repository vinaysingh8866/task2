from flask import Blueprint, request, jsonify,current_app

from models.User import addUser, getUsers
import re
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, \
    jwt_refresh_token_required, create_refresh_token, get_raw_jwt
blueprint_auth = Blueprint('blueprint_auth', __name__)
app = current_app


@blueprint_auth.route("/api/register", methods=["POST"])
def register():
    with app.app_context():
        db = current_app.config['db']
        User = current_app.config['user']
        
        try:

            email = request.json["email"]
            email = email.lower()
            upassword = request.json["upassword"]
            uname = request.json["uname"]
            if not (email and upassword and uname):
                return jsonify({"error": "Invalid Requet"})
            users = getUsers(User)
            usersByEmail = list(filter(lambda x: (x["email"] == email), users))
            if len(usersByEmail) == 1:
                return jsonify({"error": "Already Registered"})

            if not re.match(r"[\w._]{5,}@\w{3,}\.\w{2,4}", email):
                return jsonify({"error": "Invalid email"})
            addUser(db, User, uname, email, upassword)
            return jsonify({"success": True})
        except Exception as e:
            print(e)
            return jsonify({"error": "Invalid Request"})


@blueprint_auth.route("/api/login", methods=["POST"])
def login():
    with app.app_context():
        User = current_app.config['user']
        try:
            upassword = request.json["upassword"]
            email = request.json["email"]
            if email and upassword:
                user = list(filter(
                    lambda x: x["email"] == email and upassword == x["upassword"], getUsers(User)))
                if len(user) == 1:
                    refresh_token = create_refresh_token(identity=user[0]["id"])
                    token = create_access_token(identity=user[0]["id"])
                    returnJson = jsonify(
                        {"token": token, "refreshToken": refresh_token})
                    return returnJson
                else:
                    return jsonify({"error": "Invalid Password"})
            else:
                return jsonify({"error": "Invalid Request"})
        except Exception as e:
            return jsonify({"error": "Invalid Request"})


@blueprint_auth.route("/api/token_test", methods=["POST"])
@jwt_required
def tokenTest():
    return jsonify({"success": True})


@blueprint_auth.route("/api/new_token", methods=["POST"])
@jwt_refresh_token_required
def newToken():
    identity = get_jwt_identity()
    token = create_access_token(identity=identity)
    return jsonify({"token": token})


@blueprint_auth.route("/api/logout/", methods=["POST"])
@jwt_required
def logout():
    jti = get_raw_jwt()["jti"]
    # Make Token Invalid
    with app.app_context():
        InvalidToken = current_app.config['invalidToken']
        try:
            invalid_token = InvalidToken(jti=jti)
            invalid_token.save()
            return jsonify({"success": True})
        except Exception as e:
            print(e)
            return {"error": e.message}
