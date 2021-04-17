from api import db

class RatingResponseModel(db.Model):
    __tablename__ = "rating_response"

    id = db.Column(db.Integer, primary_key=True)
    session = db.Column(db.String(100))
    question = db.Column(db.String(255))
    answer = db.Column(db.String(255))
    helped = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime)

    def __init__(self, session, question, answer, helped, timestamp):
        self.session = session
        self.question = question
        self.answer = answer
        self.helped = helped
        self.timestamp = timestamp
