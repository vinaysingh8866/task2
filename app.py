from crypt import methods
from email import message
from models.InvalidToken import getInvalidToken
from models.PortFolio import addNewAsset, buyAsset, getPortFolio, getUserAddedAssets, sellAsset
from models.User import User
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from blueprints.blueprintAuth import blueprint_auth
from flask_socketio import SocketIO, send
import requests as rr
import cryptocompare

app = Flask(__name__)
socket = SocketIO(app)
# DB Settings
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///socialMedia.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
cryptocompare.cryptocompare._set_api_key_parameter(
    "5315e17c1be3ba7b6ef9776560b873b6207b0d1f9852af48b3e25aafe33fea06")

db = SQLAlchemy(app)
# DB tables
User = User(db)
PortFolio = getPortFolio(db)
InvalidToken = getInvalidToken(db)

# Setup og config for use in app
app.config["user"] = User
app.config["db"] = db
app.config["invalidToken"] = InvalidToken
app.config["JWT_SECRET_KEY"] = "test123123Testabcrfggajkshhk"
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]
# Register Token Managemeent
jwt = JWTManager(app)

# Register BluePrints
app.register_blueprint(blueprint_auth)


@app.route("/api/add_stock", methods=["POST"])
@jwt_required
def addStock():
    try:
        assetName = request.json["name"]
        assetBalance = request.json["balance"]
        if not (assetBalance and assetName):
            return jsonify({"error": "Invalid request"})
        uid = get_jwt_identity()
        addNewAsset(PortFolio, db, User, assetName, assetBalance, uid)
        return jsonify({"success": "true"})
    except Exception as e:
        print(e)
        return jsonify({"error": "Invalid Request"})


@app.route("/api/get_stock")
@jwt_required
def getStock():
    try:
        uid = get_jwt_identity()
        assets = getUserAddedAssets(PortFolio, uid)
        return jsonify(assets)
    except Exception as e:
        print(e)
        return jsonify({"error": "Invalid Request"})


@app.route("/api/buy_stock", methods=["POST"])
@jwt_required
def buyStock():
    try:
        uid = get_jwt_identity()
        aid = request.json["aid"]
        amount = request.json["amount"]
        buyAsset(PortFolio, db, uid, aid, amount)
        return jsonify({"success": "true"})
    except Exception as e:
        print(e)
        return jsonify({"error": "Invalid Request"})


@app.route("/api/sell_stock", methods=["POST"])
@jwt_required
def sellStock():
    try:
        uid = get_jwt_identity()
        aid = request.json["aid"]
        amount = request.json["amount"]
        sellAsset(PortFolio, db, uid, aid, amount)
        return jsonify({"success": "true"})
    except Exception as e:
        print(e)
        return jsonify({"error": "Invalid Request"})

# BlackListing Token


@jwt.token_in_blacklist_loader
def check_if_blacklisted_token(decrypted):
    jti = decrypted["jti"]
    return InvalidToken.is_invalid(jti)


@socket.on('connect')
def handleConnect():
    print("user Connected")


@socket.on('message')
def handleSocket(msg):
    price = cryptocompare.get_price(msg)
    send(price, brodcast=True)


if __name__ == "__main__":
    app.run(debug=True)
