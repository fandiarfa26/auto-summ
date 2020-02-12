from datetime import datetime
from app import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    pages = db.Column(db.Integer())
    path_file = db.Column(db.Text())
    summaries = db.relationship('Summary', backref='book', lazy='dynamic')

    def __repr__(self):
        return '<Book ID:{}>'.format(self.id)

class Summary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text())
    keywords = db.Column(db.String(255), default="-")
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))

    def __repr__(self):
        return '<Summary {}>'.format(self.id)