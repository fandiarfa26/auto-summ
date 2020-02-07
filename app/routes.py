import time
import os
import uuid
from flask import render_template, flash, redirect, url_for, request
from config import UPLOAD_DIR
from app import app, db
from app.forms import BookUploadForm
from app.textrank import process
from app.extracting_text import extracting_text
from app.models import Book

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

    # if form.validate_on_submit():
    #     start_time = time.time()
    #     i_file = form.file.data
    #     s1 = extracting_text(i_file)
    #     result = process(s1)
    #     flash(result)
    #     finish_time = time.time() - start_time
    #     print("--- Processing Time: %s seconds ---" % ("{0:.3f}".format(finish_time)))
    #     return redirect(url_for('index'))
    return render_template('index.html', form=uploadForm, books=books)


@app.route('/help')
def help():
    return render_template('help.html', title="Help")

@app.route('/about')
def about():
    return render_template('about.html', title="About")
