import flask, os
from flask.views import MethodView
from index import Index
from user import User
"""
from workout import Workout
from exercise import Exercise
"""

app = flask.Flask(__name__)

app.add_url_rule('/',
                 view_func=Index.as_view('index'),
                 methods=['GET', 'POST'])

app.add_url_rule('/user',
                 view_func=User.as_view('user'),
                 methods=['GET', 'POST'])

"""
app.add_url_rule('/workout',
                 view_func=Workout.as_view('workout'),
                 methods=['GET', 'POST'])

app.add_url_rule('/exercise',
                 view_func=Exercise.as_view('exercise'),
                 methods=['GET', 'POST'])
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT',5000)))