import time
import os
import uuid
import PyPDF2
from flask import render_template, flash, redirect, url_for, request, send_file
from werkzeug.utils import secure_filename
from config import UPLOAD_DIR, IMAGE_DIR, basedir
from app import app, db
from app.forms import BookUploadForm
from app.textrank import process
from app.models import Book, Summary


@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)

@app.route('/summarize', methods=['POST'])
def summarize():
    start_time = time.time()

    id_book = request.form['book']

    summ_book = Summary.query.filter_by(book_id=id_book).first()
    the_book = Book.query.filter_by(id=id_book).first()

    if summ_book is None:
        the_book = Book.query.filter_by(id=id_book).first()

        i_file = open(os.path.join(basedir, the_book.path_file), 'rb')

        # create a pdf reader
        pdfReader = PyPDF2.PdfFileReader(i_file)

        # get total pdf page number
        totalPageNumber = pdfReader.numPages
        fulltext = ''

        for p in range(0, totalPageNumber):
            pageObj = pdfReader.getPage(p)
            fulltext += pageObj.extractText()
        
        #print(fulltext)

        s1 = fulltext.replace('\n', '').replace('  ',' ')

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

@app.route('/images/covers/<file>')
def return_cover(file):
	try:
		return send_file(IMAGE_DIR+"covers/"+file, attachment_filename=file)
	except Exception as e:
		return str(e)

@app.route('/uploads/<book>/<file>')
def return_book(book, file):
	try:
		return send_file(UPLOAD_DIR+book+"/"+file, attachment_filename=file)
	except Exception as e:
		return str(e)

@app.route('/help')
def help():
    return render_template('help.html', title="Help")

@app.route('/about')
def about():
    return render_template('about.html', title="About")
