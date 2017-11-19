from expfactory.defaults import EXPFACTORY_DATABASE

if EXPFACTORY_DATABASE == "filesystem":
    print("Importing filesystem functions")
    from .filesystem import *
elif EXPFACTORY_DATABASE == 'sqlite':
    print("Importing sqlite functions")
    from .sqlite import *
elif EXPFACTORY_DATABASE == 'mysql':
    print("Importing mysql functions")
    from .mysql import *
elif EXPFACTORY_DATABASE == 'postgres':
    print("Importing postgres functions")
    from .postgres import *
else:
    print("Database %s is not a supported type." %EXPFACTORY_DATABASE)
