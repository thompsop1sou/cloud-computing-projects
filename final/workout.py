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
            search_options = {'types':ex_api.types, 'muscles':ex_api.muscles, 'difficulties':ex_api.difficulties}
            search_terms={'name':'', 'type':'', 'muscle':'', 'difficulty':''}
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
            if request.form['submit'] == 'Search for Exercises':
                search_terms = str({'name':request.form['ex_name'], 'type':request.form['ex_type'],
                                   'muscle':request.form['ex_muscle'], 'difficulty':request.form['ex_difficulty']})
                search_terms = search_terms.replace("'", '"')
                return redirect('{}?username={}&date={}&search_terms={}'.format(url_for('workout'), username, date, search_terms))
            else:
                return redirect('{}?username={}&date={}'.format(url_for('workout'), username, date))
        elif request.form['section'] == 'exercise_select':
            if request.form['submit'] == 'Select Exercise' or request.form['submit'] == 'Create Exercise':
                entries = model.select_workout(username=username, date=date)
                if len(entries) > 0:
                    exercises = entries[0]['exercises']
                    new_ex_name = request.form['ex_name']
                    if new_ex_name not in [exercise['ex_name'] for exercise in exercises]:
                        exercises.append({'ex_name':new_ex_name, 'resistance':0, 'repititions':0})
                        model.update_workout(username=username, old_date=date, new_date=date, new_exercises=exercises)
                return redirect('{}?username={}&date={}'.format(url_for('workout'), username, date))
            else:
                return redirect('{}?username={}&date={}'.format(url_for('workout'), username, date))
        elif request.form['section'] == 'exercise_edit':
            if request.form['submit'] == 'Update Exercise':
                entries = model.select_workout(username=username, date=date)
                if len(entries) > 0:
                    exercises = entries[0]['exercises']
                    for i in range(len(exercises)):
                        if exercises[i]['ex_name'] == request.form['ex_name']:
                            exercises[i]['resistance'] = request.form['resistance']
                            exercises[i]['repititions'] = request.form['repititions']
                            break
                    model.update_workout(username=username, old_date=date, new_date=date, new_exercises=exercises)
                return redirect('{}?username={}&date={}'.format(url_for('workout'), username, date))
            elif request.form['submit'] == 'Delete Exercise':
                entries = model.select_workout(username=username, date=date)
                if len(entries) > 0:
                    exercises = entries[0]['exercises']
                    for i in range(len(exercises)):
                        if exercises[i]['ex_name'] == request.form['ex_name']:
                            exercises.pop(i)
                            break
                    model.update_workout(username=username, old_date=date, new_date=date, new_exercises=exercises)
                return redirect('{}?username={}&date={}'.format(url_for('workout'), username, date))
            else:
                return redirect('{}?username={}&date={}'.format(url_for('workout'), username, date))
