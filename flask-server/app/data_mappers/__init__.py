import pkgutil, importlib


# Dynamically import all classes from modules in the data mappers package
for _, module_name, _ in pkgutil.iter_modules(__path__):
    # Dynamically import the module
    module = importlib.import_module(f".{module_name}", package="app.data_mappers")

    # Import only classes from the module
    for item_name in dir(module):
        item = getattr(module, item_name)
        # Check if it's a class (and not an import or other objects)
        if isinstance(item, type) and item.__module__ == module.__name__:
            globals()[item_name] = item  # Add the class to the global namespace
