import pkgutil
for (module_loader, name, _) in pkgutil.walk_packages(__path__):
    module_loader.find_module(name).load_module(name)
