from dependency.core import ProviderModule, module
from example.plugins.module1 import Module1

@module(
    imports=[
        Module1
    ],
)
class MainModule(ProviderModule):
    def declare_providers(self):
        return []