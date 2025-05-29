from typing import Any
from .component import Component
from typing import overload
from .utils import PriorityList

class GameObject:
    components: dict[str, Component]
    components_to_run: PriorityList[Component]
    storage: dict[str, dict[str, Any]]

    @overload
    def get_storage(self, component: str) -> dict[str, Any]:
        ...

    @overload
    def get_storage(self, component: Component):
        ...

    def get_storage(self, component: str | Component) -> dict[str, Any]:
        if isinstance(component, Component):
            return self.get_storage(component.name)
        return self.storage.get(component, {})

    def add_component(self, component: Component) -> None:
        if component.name in self.components:
            raise ValueError(f"Component '{component.name}' already exists")
        self.components[component.name] = component
        self.storage[component.name] = component.get_default_storage()

    @overload
    def remove_component(self, component: str) -> None:
        ...

    @overload
    def remove_component(self, component: Component) -> None:
        ...

    def remove_component(self, component: str | Component) -> None:
        if isinstance(component, Component):
            self.remove_component(component.name)
        if component not in self.components:
            raise ValueError(f"Component '{component}' does not exist")
        del self.storage[component]
        del self.components[component]

