from flask import render_template
from flask.views import MethodView
import gbmodel

class View(MethodView):
    def get(self):
        model = gbmodel.get_model()
        entries = [dict(name=row[0], description=row[1], street_address=row[2], type_of_service=row[3],
                        phone_number=row[4], hours_of_operation=row[5], reviews=row[6]) for row in model.select()]
        return render_template('view.html',entries=entries)