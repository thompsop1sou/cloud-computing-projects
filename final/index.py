from flask import redirect, request, url_for, render_template
from flask.views import MethodView
from datetime import date
import wo_model

class Index(MethodView):

    def get(self):
        model = wo_model.get_model()
        entries = model.select()
        usernames = []
        for entry in entries:
            if entry['username'] not in usernames:
                usernames.append(entry['username'])
        return render_template('index.html', usernames=usernames)

    def post(self):
        model = wo_model.get_model()
        username = request.form.get("username")
        entries = model.select(username=username)
        if len(entries) == 0:
            model.insert(username=username, date=str(date.today()), exercises='usercreated')
        return redirect(url_for('index'))
