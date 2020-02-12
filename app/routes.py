import time
import os
import uuid
from flask import render_template, flash, redirect, url_for, request, send_file
from config import UPLOAD_DIR, basedir
from app import app, db
from app.forms import BookUploadForm
from app.textrank import process
from app.extracting_text import extracting_text
from app.models import Book, Summary

@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
def index():
    
    uploadForm = BookUploadForm()

    books = Book.query.all()

    if uploadForm.validate_on_submit():
        i_title = uploadForm.title.data
        i_file = uploadForm.file.data

        ext = i_file.filename.split('.')[-1]
        filename = f'{uuid.uuid4()}.{ext}'

        path_file = UPLOAD_DIR + filename

        i_file.save(path_file)

        newBook = Book(title=i_title, path_file='uploads/'+filename)
        db.session.add(newBook)
        db.session.commit()

        print("Uploaded a new book!")
        return redirect(url_for('index'))

    return render_template('index.html', form=uploadForm, books=books)

@app.route('/summarize', methods=['POST'])
def summarize():
    start_time = time.time()

    id_book = request.form['book']

    summ_book = Summary.query.filter_by(book_id=id_book).first()
    the_book = Book.query.filter_by(id=id_book).first()

    if summ_book is None:
        the_book = Book.query.filter_by(id=id_book).first()

        i_file = open(os.path.join(basedir, the_book.path_file), 'rb')
        s1 = extracting_text(i_file)
        result = process(s1)

        newSumm = Summary(text=result, book_id=id_book)
        db.session.add(newSumm)
        db.session.commit()
    else:
        result = summ_book.text
    
    flash(the_book.path_file)
    flash(result)
    finish_time = time.time() - start_time
    print("--- Processing Time: %s seconds ---" % ("{0:.3f}".format(finish_time)))
    return redirect(url_for('index'))
    # return os.path.join(basedir, request.form['book'])

@app.route('/uploads/<file>')
def return_files_tut(file):
	try:
		return send_file(UPLOAD_DIR+file, attachment_filename=file)
	except Exception as e:
		return str(e)

@app.route('/help')
def help():
    return render_template('help.html', title="Help")

@app.route('/about')
def about():
    return render_template('about.html', title="About")
