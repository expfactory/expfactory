from expfactory.defaults import EXPFACTORY_DATABASE

if EXPFACTORY_DATABASE == "filesystem":
    from .filesystem import *
elif EXPFACTORY_DATABASE == 'sqlite':
    from .sqlite import *
else:
    print("Database %s is not a supported type." %EXPFACTORY_DATABASE)
