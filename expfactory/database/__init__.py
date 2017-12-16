from expfactory.defaults import EXPFACTORY_DATABASE

if EXPFACTORY_DATABASE == "filesystem":
    from .filesystem import *
else:
    from .relational import *
    if EXPFACTORY_DATABASE.startswith('sqlite'):
        from .sqlite import *
