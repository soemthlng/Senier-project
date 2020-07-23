from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from elasticsearch import Elasticsearch
import json

es = Elasticsearch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)

	
class SearchForm(FlaskForm):
    SearchType = SelectField(choices=[('title', 'Title'), ('author', 'Author'), ('content', 'Content')])
    Inputdata = StringField('Input texts below', validators=[DataRequired()])
    submit = SubmitField('Search')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
	session['type'] = form.SearchType.data
        session['data'] = form.Inputdata.data        
        return redirect(url_for('result'))
    
    return render_template('index.html', form=form, data=session.get('data'), type = session.get('type'))

@app.route('/result', methods=['GET', 'POST'])
def result():
    if session['type'] == "title":
	query = "Title:" + session['data']
    elif session['type'] == "author":
	query = "Author:" + session['data']
    else:
	query = "Source:" + session['data']
   
    results = es.search(index="paper", q=query, default_operator="and")
    
    title = []
    author = []
    content = []
    for result in results['hits']['hits']:
        title.append(result['_source']['Title'])
        author.append(result['_source']['Author'])
        content.append(result['_source']['Source'])

    if len(title) == 1: 
    	return render_template('result.html', title = title[0], author = author[0], content = content[0])
    if len(title) == 2: 
    	return render_template('result.html', title = title[0], author = author[0], content = content[0], title2 = title[1], author2 = author[1], content2 = content[1])
    if len(title) == 3: 
    	return render_template('result.html', title = title[0], author = author[0], content = content[0], title2 = title[1], author2 = author[1], content2 = content[1], title3 = title[2], author3 = author[2], content3 = content[2])

if __name__ == '__main__':
	app.run()
