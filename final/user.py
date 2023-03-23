from flask import redirect, request, url_for, render_template
from flask.views import MethodView
from datetime import date
import wo_model

class User(MethodView):

    def get(self):
        username = request.args.get("username")
        model = wo_model.get_model()
        entries = model.select(username=username)
        userinfo = {'username':username}
        workouts = []
        for entry in entries:
            if entry['exercises'] == 'usercreated':
                userinfo['joined'] = entry['date']
            else:
                workouts.append({'date':entry['date'], 'exercises':[exercise['name'] for exercise in entry['exercises']]})
        return render_template('user.html', userinfo=userinfo, workouts=workouts)

    def post(self):
        pass
        """
        model = wo_model.get_model()
        username = request.form.get("username")
        entries = model.select(username=username)
        if len(entries) == 0:
            model.insert(username=username, date=str(date.today()), exercises='usercreated')
        return redirect(url_for('index'))
        """
