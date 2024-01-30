from flask import redirect, request, url_for, render_template
from flask.views import MethodView
from datetime import date
import wo_model

class Index(MethodView):

    def get(self):
        # Get all users from the database
        model = wo_model.get_model()
        users = model.select_user()
        # Sort on the username
        users.sort(key=(lambda user: user['username']))
        # Render the webpage
        return render_template('index.html', users=users)

    def post(self):
        # Get the username from the form
        username = request.form['username']
        # If the username is not emtpy...
        if username != '':
            # Creating a new user
            if request.form['submit'] == 'Create User':
                model = wo_model.get_model()
                model.insert_user(username=username, date=str(date.today()))
                return redirect(url_for('index'))
            # Logging in to an existing user
            elif request.form['submit'] == 'Login':
                return redirect(url_for('user') + '?username=' + username)
        # If the username is empty...
        else:
            # Just return to the home page
            return redirect(url_for('index'))
