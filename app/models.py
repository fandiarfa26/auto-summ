from datetime import datetime
from app import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100))
    title = db.Column(db.String(100))
    chapters = db.relationship('Chapter')

    def __repr__(self):
        return '<Book ID:{}>'.format(self.id)

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100))
    title = db.Column(db.String(100))
    pages = db.Column(db.Integer())
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    summaries = db.relationship('Summary')

    def __repr__(self):
        return '<Chapter ID:{}>'.format(self.id)

class Summary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text())
    keywords = db.Column(db.String(255), default="-")
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'))

    def __repr__(self):
        return '<Summary {}>'.format(self.id)