def getPortFolio(db):
    class PortFolio(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        uid = db.Column(db.Integer, db.ForeignKey("user.uid"))
        user = db.relationship('User', foreign_keys=uid)
        assetName = db.Column(db.String(256))
        assetBalance = db.Column(db.Integer)
    return PortFolio


def getUserAddedAssets(PortFolio,uid):
    assets = PortFolio.query.all()
    return [{"id": item.id, "uid": item.uid, "assetName": item.assetName, "assetBalance": item.assetBalance} for item in
            filter(lambda i: i.uid == uid, assets)]

def addNewAsset(PortFolio,db,User,assetName, assetBalance,uid):
    try:
        user = list(filter(lambda i: i.uid == uid, User.query.all()))[0]
        asset = PortFolio(assetBalance=assetBalance, assetName=assetName, user=user)
        db.session.add(asset)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False

def buyAsset(PortFolio,db,aid, amount):
    try:
        asset = PortFolio.query.get(aid)
        asset.assetBalance += amount
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False

def sellAsset(PortFolio,db,aid, amount):
    try:
        asset = PortFolio.query.get(aid)
        asset.assetBalance -= amount
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False

