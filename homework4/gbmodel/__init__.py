model_backend = 'datastore'

if model_backend == 'sqlite3':
    from .model_sqlite3 import model
elif model_backend == 'datastore':
    from .model_datastore import model

appmodel = model()

def get_model():
    return appmodel
