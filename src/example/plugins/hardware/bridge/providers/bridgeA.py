from dependency.core import provider, providers
from example.plugins.hardware.bridge import HardwareAbstraction, HardwareAbstractionComponent
from example.plugins.hardware.factory import HardwareFactory, HardwareFactoryComponent
from example.plugins.hardware.observer import HardwareObserver, HardwareObserverComponent
from example.plugins.hardware.observer.interfaces import EventHardwareOperation

@provider(
    component=HardwareAbstractionComponent,
    imports=[
        HardwareFactoryComponent
    ],
    provider = providers.Singleton
)
class HardwareAbstractionBridgeA(HardwareAbstraction):
    def __init__(self, config: dict) -> None:
        self.__factory: HardwareFactory = HardwareFactoryComponent.provide()
        self.__observer: HardwareObserver = HardwareObserverComponent.provide()
        print("AbstractionBridgeA initialized")

    def someOperation(self, product: str) -> None:
        instance = self.__factory.createHardware(product=product)
        instance.doStuff("someOperation")
        self.__observer.update(
            context=EventHardwareOperation(product=product, operation="someOperation"))

    def otherOperation(self, product: str) -> None:
        instance = self.__factory.createHardware(product=product)
        instance.doStuff("otherOperation")
        self.__observer.update(
            context=EventHardwareOperation(product=product, operation="otherOperation"))