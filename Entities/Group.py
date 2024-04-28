from Entities.Root import Root

class Group(Root):
    def __init__(self, name) -> None:
        return super().__init__(name)

    def add_child(self, key, value):
        return super().add_child(key, value)

    def get_child(self, key):
        return super().get_child(key)