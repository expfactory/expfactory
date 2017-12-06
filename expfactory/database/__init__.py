from expfactory.defaults import EXPFACTORY_DATABASE

if EXPFACTORY_DATABASE == "filesystem":
    print("Importing filesystem functions")
    from .filesystem import *
else:
    from .relational import *
    if EXPFACTORY_DATABASE.startswith('sqlite'):
        from .sqlite import *

# Shared functions across database types
from .shared import *
