from models.InvalidToken import getInvalidToken
from models.User import User
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from blueprints.blueprintAuth import blueprint_auth
app = Flask(__name__)
#DB Settings
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///socialMedia.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
#DB tables
User = User(db)
InvalidToken = getInvalidToken(db)

#Setup og config for use in app
app.config["user"] = User
app.config["db"] = db
app.config["invalidToken"] = InvalidToken
app.config["JWT_SECRET_KEY"] = "test123123Testabcrfggajkshhk"
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]
#Register Token Managemeent
jwt = JWTManager(app)

#Register BluePrints
app.register_blueprint(blueprint_auth)


#BlackListing Token 
@jwt.token_in_blacklist_loader
def check_if_blacklisted_token(decrypted):
    jti = decrypted["jti"]
    return InvalidToken.is_invalid(jti)

if __name__ == "__main__":
    app.run(debug=True)
