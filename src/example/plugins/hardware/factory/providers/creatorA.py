from dependency.core import provider, providers
from example.plugins.hardware.factory import HardwareFactory, HardwareFactoryComponent
from example.plugins.hardware.factory.interfaces import Hardware
from example.plugins.hardware.factory.products.productA import HardwareA
from example.plugins.hardware.factory.products.productB import HardwareB
from example.plugins.hardware.observer import HardwareObserver, HardwareObserverComponent
from example.plugins.hardware.observer.interfaces import EventHardwareCreated

@provider(
    component=HardwareFactoryComponent,
    imports=[
        HardwareObserverComponent
    ],
    dependents=[
        HardwareA,
        HardwareB,
    ],
    provider = providers.Singleton
)
class HardwareFactoryCreatorA(HardwareFactory):
    def __init__(self, config: dict):
        self.__observer: HardwareObserver = HardwareObserverComponent.provide()
        print("FactoryCreatorA initialized")

    def createHardware(self, product: str) -> Hardware:
        instance: Hardware
        match product:
            case "A":
                instance = HardwareA()
                self.__observer.update(
                    context=EventHardwareCreated(product="A"))
                return instance
            case "B":
                instance = HardwareB()
                self.__observer.update(
                    context=EventHardwareCreated(product="B"))
                return instance
            case _:
                raise ValueError(f"Unknown product type: {product}")