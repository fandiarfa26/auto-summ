from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import SentenceForm
from app.textrank import process

@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
def index():
    
    form = SentenceForm()
    if form.validate_on_submit():
        s1 = form.sentence1.data
        result = process(s1)
        print(result)
        flash('OK')
        return redirect(url_for('index'))
    return render_template('index.html', form=form)

@app.route('/help')
def help():
    return render_template('help.html', title="Help")

@app.route('/about')
def about():
    return render_template('about.html', title="About")
