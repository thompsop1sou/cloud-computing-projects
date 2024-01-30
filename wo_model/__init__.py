model_backend = 'datastore'
#model_backend = 'pylist'

if model_backend == 'pylist':
    from .model_pylist import model
elif model_backend == 'datastore':
    from .model_datastore import model
else:
    raise ValueError("No appropriate databackend configured. ")

appmodel = model()

def get_model():
    return appmodel
