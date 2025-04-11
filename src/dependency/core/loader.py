import logging
from pprint import pformat
from typing import cast
from dependency.core.module import Module
from dependency.core.container import Container
from dependency.core.resolver import resolve_dependency_layers
logger = logging.getLogger("DependencyLoader")

def resolve_dependency(container: Container, appmodule: type[Module]) -> None:
    _appmodule = cast(Module, appmodule)
    logger.info("Resolving dependencies")

    unresolved_layers = _appmodule.init_providers()
    resolved_layers = resolve_dependency_layers(unresolved_layers)

    named_layers = pformat(resolved_layers)
    logger.info(f"Layers:\n{named_layers}")

    for resolved_layer in resolved_layers:
        for provider in resolved_layer:
            provider.resolve(container, unresolved_layers)
    
    container.check_dependencies()
    container.init_resources()
    _appmodule.init_bootstrap()
    logger.info("Dependencies resolved and injected")