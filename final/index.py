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
            # If creating new user...
            if request.form['submit'] == 'Create User':
                # Get all the entries in the database with username
                model = wo_model.get_model()
                entries = model.select_user(username=username)
                # If no entries exist, username is unique (valid), so create the new user
                if len(entries) == 0:
                    model.insert_user(username=username, date=str(date.today()))
                # Return to home page
                return redirect(url_for('index'))
            # If logging in in to existing user...
            elif request.form['submit'] == 'Login':
                # Go to the user page
                return redirect(url_for('user') + '?username=' + username)
        # If the username is empty...
        else:
            # Just return to the home page
            return redirect(url_for('index'))
