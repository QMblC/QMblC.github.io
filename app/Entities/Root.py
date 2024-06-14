class Root:
    def __init__(self, path: str) -> None:
        splitted = path.split('_')
        self.children = dict()
        self.name = splitted[-1]
        self.path = path

    def add_child(self, key, value):
        if not(key in self.children):
            self.children[key] = value


    def get_child(self, key):
        if key in self.children:
            return self.children[key]
        else:
            raise KeyError("Ключа нет")
        
    def toJSON(self):
        j = []
        for x in self.children:
            a = {"children" : self.children[x].toJSON()}
            j.append(a)
        return {
            "name" : self.name,
            "children": j
        }