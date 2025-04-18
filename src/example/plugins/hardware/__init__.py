from dependency.core import Module, module
from example.plugins.hardware.bridge import HardwareAbstractionComponent
from example.plugins.hardware.factory import HardwareFactoryComponent
from example.plugins.hardware.observer import HardwareObserverComponent

@module(
    declaration=[
        HardwareAbstractionComponent,
        HardwareFactoryComponent,
        HardwareObserverComponent,
    ]
)
class HardwareModule(Module):
    def declare_providers(self):
        # Common providers
        from example.plugins.hardware.bridge.providers.bridgeA import HardwareAbstractionBridgeA
        from example.plugins.hardware.factory.providers.creatorA import HardwareFactoryCreatorA
        from example.plugins.hardware.observer.providers.publisherA import HardwareObserverA