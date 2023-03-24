from flask import redirect, request, url_for, render_template
from flask.views import MethodView
from datetime import date as get_date
import wo_model

class User(MethodView):

    def get(self):
        # Get all the entries from the database with username
        username = request.args['username']
        model = wo_model.get_model()
        user_info = model.select_user(username=username)
        # If there are some entries...
        if len(user_info) > 0:
            # Determine if we can edit the user properties
            edit = 'disabled'
            if 'edit' in request.args:
                edit = ''
            # Fill out the userinfo dictionary and the workouts list from the database
            user_info = user_info[0]
            entries = model.select_workout(username=username)
            workouts = []
            for entry in entries:
                workouts.append({'date':entry['date'], 'exercises':str([exercise['ex_name'] for exercise in entry['exercises']])})
            # Sort the workouts on their date
            workouts.sort(reverse=True, key=(lambda workout: workout['date']))
            # Render the user web page
            return render_template('user.html', user_info=user_info, workouts=workouts, today_date=str(get_date.today()), edit=edit)
        # If there are no entries...
        else:
            # Invalid username, return to the home page
            return redirect(url_for('index'))

    def post(self):
        # If working with the user section...
        if request.form['section'] == 'user':
            # Get some basic variables
            username = request.args['username']
            model = wo_model.get_model()
            # Enabling edits to user info
            if request.form['submit'] == 'Edit User':
                return redirect('{}?username={}&edit=True'.format(url_for('user'), username))
            # Updating user info
            elif request.form['submit'] == 'Update User':
                success = model.update_user(old_username=username, new_username=request.form['username'], new_created_date=request.form['created_date'])
                if success:
                    return redirect('{}?username={}'.format(url_for('user'), request.form['username']))
                else:
                    return redirect('{}?username={}'.format(url_for('user'), username))
            # Deleting user
            elif request.form['submit'] == 'Delete User':
                model.delete_user(username=username)
                return redirect(url_for('index'))
            # Logging out
            elif request.form['submit'] == 'Logout':
                return redirect(url_for('index'))
        # If working with the workout section...
        elif request.form['section'] == 'workout':
            # Get some basic variables
            username = request.args['username']
            model = wo_model.get_model()
            date = request.form['date']
            # If the date is not empty...
            if date != '':
                # Creating a new workout
                if request.form['submit'] == 'Create Workout':
                    model.insert_workout(username=username, date=date, exercises=[])
                    return redirect('{}?username={}'.format(url_for('user'), username))
                # Editing an old workout
                elif request.form['submit'] == 'Edit Workout':
                    return redirect('{}?username={}&date={}'.format(url_for('workout'), username, date))
                # Cloning an old workout
                elif request.form['submit'] == 'Clone Workout':
                    old_workout = model.select_workout(username=username, date=date)[0]
                    model.insert_workout(username=username, date=str(get_date.today()), exercises=old_workout['exercises'])
                    return redirect('{}?username={}'.format(url_for('user'), username))
            # If the date is emtpy...
            else:
                # Just return to the user page
                return redirect('{}?username={}'.format(url_for('user'), username))
