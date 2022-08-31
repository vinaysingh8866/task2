def User(db):

    class User(db.Model):
        uid = db.Column(db.Integer,
                        primary_key=True)
        uname = db.Column(db.String(24))
        email = db.Column(db.String(64))
        upassword = db.Column(db.String(64))

        # Constructor
        def __init__(self, uname, email, upassword):
            self.uname = uname
            self.email = email
            self.upassword = upassword

    return User


def getUsers(User):
    users = User.query.all()
    return [{"id": i.uid, "username": i.uname, "email": i.email, "upassword": i.upassword} for i in users]


def getUser(User, uid):
    users = User.query.all()
    user = list(filter(lambda x: x.uid == uid, users))[0]
    return {"id": user.id, "username": user.uname, "email": user.email, "upassword": user.upassword}


def addUser(db,User, uname, email, upassword):
    try:
        user = User(uname, email, upassword)
        db.session.add(user)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False


def removeUser(User, db, uid):
    try:
        user = User.query.get(uid)
        db.session.delete(user)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False
