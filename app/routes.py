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
from app.extract_keywords import extract_keywords
from app.models import Book, Chapter, Summary

@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)

@app.route('/result', methods=['POST'])
def result():
    start_time = time.time()
    print('Get Processing...')

    ch_id = request.form['book']

    summ_book = Summary.query.filter_by(chapter_id=ch_id).first()
    the_chapter = Chapter.query.filter_by(id=ch_id).first()
    the_book = Book.query.filter_by(id=the_chapter.book_id).first()

    ### UNTUK PERCOBAAN ###
    p = "Di dunia bisnis, multimedia digunakan sebagai media profil perusahaan, profil produk, bahkan sebagai media kios informasi dan pelatihan dalam sistem e-learning."
    result = extract_keywords(p)
    ### 
    
    # if summ_book is None:
    #     print('Extracting Text from PDF...')
    #     i_file = open(os.path.join(UPLOAD_DIR, the_book.code + "/" + the_chapter.code + ".pdf"), 'rb')

    #     # create a pdf reader
    #     pdfReader = PyPDF2.PdfFileReader(i_file)

    #     # get total pdf page number
    #     totalPageNumber = pdfReader.numPages
    #     fulltext = ''

    #     for p in range(0, totalPageNumber):
    #         pageObj = pdfReader.getPage(p)
    #         fulltext += pageObj.extractText()
        
    #     #print(fulltext)

    #     s1 = fulltext.replace('\n', '').replace('  ',' ')

    #     print('Summarizing...')
    #     result = process(s1)

    #     newSumm = Summary(text=result, chapter_id=ch_id)
    #     db.session.add(newSumm)
    #     db.session.commit()
    # else:
    #     result = summ_book.text
    
    finish_time = time.time() - start_time
    
    print('Done.')
    print("--- Processing Time: %s seconds ---" % ("{0:.3f}".format(finish_time)))
    
    chapter_ori_path = the_book.code + "/" + the_chapter.code + "_ori.pdf"
    

    return render_template('result.html', ch_path=chapter_ori_path, summary=result)


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
