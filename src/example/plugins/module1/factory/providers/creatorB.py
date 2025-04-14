from dependency.core import provider, providers
from example.plugins.module1.factory import Factory, FactoryComponent
from example.plugins.module1.factory.interfaces import Product
from example.plugins.module1.factory.products.productB import ProductB
from example.plugins.module1.factory.products.productC import ProductC
from example.plugins.module1.observer import Observer, ObserverComponent
from example.plugins.module1.observer.interfaces import EventProductCreated

@provider(
    component=FactoryComponent,
    imports=[
        ObserverComponent
    ],
    dependents=[
        ProductB,
        ProductC
    ],
    provider = providers.Singleton
)
class FactoryCreatorB(Factory):
    def __init__(self, config: dict):
        self.__observer: Observer = ObserverComponent()
        print("FactoryCreatorB initialized")

    def createProduct(self, product: str) -> Product:
        match product:
            case "B":
                self.__observer.update(
                    context=EventProductCreated(product="B"))
                return ProductB()
            case "C":
                self.__observer.update(
                    context=EventProductCreated(product="C"))
                return ProductC()
            case _:
                raise ValueError(f"Unknown product type: {product}")