from expfactory.defaults import EXPFACTORY_DATABASE

if EXPFACTORY_DATABASE == "filesystem":
    print("Importing filesystem functions")
    from .filesystem import *
elif EXPFACTORY_DATABASE == 'sqlite':
    print("Importing sqlite functions")
    from .sqlite import *
else:
    print("Database %s is not a supported type." %EXPFACTORY_DATABASE)
