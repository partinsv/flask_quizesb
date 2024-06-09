from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    questions = db.relationship('Question', backref='topic', lazy=True)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(500), nullable=False)
    choice1 = db.Column(db.String(200), nullable=False)
    choice2 = db.Column(db.String(200), nullable=False)
    choice3 = db.Column(db.String(200), nullable=False)
    choice4 = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.String(200), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)
