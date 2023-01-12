"""
A simple Flask web application for listing charities and social services in Medford.
"""
import flask, os
from flask.views import MethodView
from index import Index
from view import View
from submit import Submit

app = flask.Flask(__name__)

app.add_url_rule('/',
                 view_func=Index.as_view('index'),
                 methods=["GET"])

app.add_url_rule('/view/',
                 view_func=View.as_view('view'),
                 methods=['GET'])

app.add_url_rule('/submit/',
                 view_func=Submit.as_view('submit'),
                 methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT',5000)))