from api import db

class TrainingModel(db.Model):
    __tablename__ = "training"

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255))
    answer = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime)

    def __init__(self, question, answer, timestamp):
        self.question = question
        self.answer = answer
        self.timestamp = timestamp
