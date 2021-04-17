from api import db

class RatingFinalModel(db.Model):
    __tablename__ = "rating_final"

    id = db.Column(db.Integer, primary_key=True)
    session = db.Column(db.String(100))
    rating = db.Column(db.SmallInteger)
    timestamp = db.Column(db.DateTime)

    def __init__(self, session, rating, timestamp):
        self.session = session
        self.rating = rating
        self.timestamp = timestamp
