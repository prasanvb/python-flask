from db import db

# Not implemented


class RevokedTokensModel(db.Model):
    __tablename__ = "revokedtokens"

    id = db.Column(db.Integer, primary_key=True)
    token_id = db.Column(db.String(200))
