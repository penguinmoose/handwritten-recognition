from app import app
import datetime
from re import A
from math import fabs
from flask import render_template
@app.route('/')
@app.route('/index')
def index():
    text = str(datetime.datetime.now())
    return '''
    <html>
        <head>
            <title>Hello World</title>
        </head>
        <body>
            <a href ="/about"> About </a>
            <a href ="/test"> Test Page <a>
            <a href ="/test2"> Test2 Page <a>
            <div>You ran this flask thingy on: ''' + text + '''</div>
        </body>
    </html>
    '''
@app.route('/about')
def about():
    return "this is an about page"

@app.route('/test2')
def test2():
    user = {'username':'jc'}
    data = [
        {
            'person': {'username': 'Moose', 'likes': 'MOOSE MOOSE'},
            'content': 'Special stuff 123',
            'location': 'Moose',
        },
        {
            'person': {'username': 'jc', 'likes': 'programming'},
            'content': 'JC stuff 456',
            'location': 'United States',
        },
        {
            'person': {'username': 'penguin', 'likes': 'cucumbers'},
            'content': 'Penguin stuff 789',
            'location': 'Unknown',
        }
    ]
    return render_template('test2.html', user=user, data=data)

@app.route('/test')
def test():
    user = {'username':'jc'}
    data = "data 123 beeeeep"
    return render_template('test.html',user=user, data=data)