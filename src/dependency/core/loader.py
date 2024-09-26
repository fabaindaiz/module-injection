from pprint import pformat
from dependency.core import Module
from dependency.core.container import Container
from dependency.core.resolver import resolve_dependency_layers

def resolve_dependency(container: Container, module: Module):
    print("Resolving dependencies")

    unresolved_layers = module.get_providers()
    resolved_layers = resolve_dependency_layers(unresolved_layers)

    named_layers = pformat(resolved_layers)
    print(f"Layers:\n{named_layers}")

    for resolved_layer in resolved_layers:
        for provider in resolved_layer:
            provider.provider.populate_container(container)
    
    module.do_bootstrap()
    
    container.check_dependencies()
    container.init_resources()
    print("Dependencies resolved and injected")