from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import FileUploadForm
from app.textrank import process
from app.extracting_text import extracting_text

@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
def index():
    
    form = FileUploadForm()
    if form.validate_on_submit():
        i_file = form.file.data
        s1 = extracting_text(i_file)
        result = process(s1)
        flash(result)
        return redirect(url_for('index'))
    return render_template('index.html', form=form)

@app.route('/help')
def help():
    return render_template('help.html', title="Help")

@app.route('/about')
def about():
    return render_template('about.html', title="About")
