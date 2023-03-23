from flask import redirect, request, url_for, render_template
from flask.views import MethodView
import exercise_api
import wo_model
import json

class Workout(MethodView):

    def get(self):
        username = request.args['username']
        date = request.args['date']
        model = wo_model.get_model()
        workouts = model.select_workout(username=username, date=date)
        if len(workouts) > 0:
            workout_info = {'username':username, 'date':date}
            exercises = workouts[0]['exercises']
            ex_api = exercise_api.ExerciseAPI()
            search_options = {'kinds':ex_api.kinds, 'muscles':ex_api.muscles, 'difficulties':ex_api.difficulties}
            search_terms={'name':'', 'kind':'', 'muscle':'', 'difficulty':''}
            search_results=[]
            if 'search_terms' in request.args:
                search_terms = json.loads(request.args['search_terms'])
                search_results = ex_api.call(search_terms)
            return render_template('workout.html', workout_info=workout_info, exercises=exercises,
                                   search_options=search_options, search_terms=search_terms, search_results=search_results)
        else:
            return redirect('{}?username={}'.format(url_for('user'), username))

    def post(self):
        username = request.args['username']
        date = request.args['date']
        model = wo_model.get_model()
        if request.form['section'] == 'workout':
            print('Got to 3')
            if request.form['submit'] == 'Delete Workout':
                model.delete_workout(username=username, date=date)
                return redirect('{}?username={}'.format(url_for('user'), username))
            elif request.form['submit'] == 'Update Workout':
                new_date = request.form['date']
                model.update_workout(username=username, old_date=date, new_date=new_date)
                return redirect('{}?username={}&date={}'.format(url_for('workout'), username, new_date))
            elif request.form['submit'] == 'Return to User':
                return redirect('{}?username={}'.format(url_for('user'), username))
        elif request.form['section'] == 'exercise_search':
            return redirect('{}?username={}&date={}'.format(url_for('workout'), username, date))
        elif request.form['section'] == 'exercise_select':
            return redirect('{}?username={}&date={}'.format(url_for('workout'), username, date))
        elif request.form['section'] == 'exercise_edit':
            return redirect('{}?username={}&date={}'.format(url_for('workout'), username, date))
