from functools import wraps

class SessionSaveDecorator(object):

    def __init__(self, vars):
        self.vars = vars
        
    def __call__(self, view_func):
        @wraps(view_func)
        def inner(request, *args, **kwargs):
            session_backup = {}
            for var in self.vars:
                try:
                    session_backup[var] = request.session[var]
                except KeyError:
                    pass
            response = view_func(request, *args, **kwargs)
            for var, value in session_backup.items():
                request.session[var] = value
            return response
        return inner