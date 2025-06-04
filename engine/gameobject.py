from typing import Any
from .component import Component
from typing import overload
from .utils import PriorityList, Context

class GameObject:
    name: str
    components: dict[str, Component]
    components_to_run: PriorityList[Component]
    storage: dict[str, dict[str, Any]]
    priority: int
    active: bool

    def __init__(self, name: str, priority: int = 0) -> None:
        self.components = {}
        self.components_to_run = PriorityList()
        self.storage = {}
        self.name = name
        self.priority = priority
        self.active = True

    def reinit(self):
        self.storage = {}
        for component in self.components.values():
            self.storage[component.name] = component.get_default_storage()

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
        self.components_to_run.add(component, component.execution_order)

    @overload
    def remove_component(self, component: str) -> None:
        ...

    @overload
    def remove_component(self, component: Component) -> None:
        ...

    def remove_component(self, component: str | Component) -> None:
        if isinstance(component, Component):
            return self.remove_component(component.name)
        if component not in self.components:
            raise ValueError(f"Component '{component}' does not exist")
        self.components_to_run.remove(self.components[component])
        del self.storage[component]
        del self.components[component]

    def set_active(self, active: bool) -> None:
        self.active = active

    def run(self, ctx: Context) -> None:
        for component in self.components_to_run:
            ctx.gameObject = self
            component[0].run(ctx)
