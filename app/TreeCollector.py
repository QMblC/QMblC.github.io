
from ExcelParser import DbHandler, ExcelParser, UserDb
from Entities.Root import Root
from Entities.Location import Location
from Entities.Departament import Departament
from Entities.Division import Division
from Entities.Group import Group
from Entities.Main import Main


class TreeCollector:


    def get_root(path: str) -> Root:
        splitted_path = path.split('_')
        root = TreeCollector.determine_type(path)
        root_type = type(root)

        if root_type is Main:
            children = DbHandler.UserHandlerDb.get_locations()
        elif root_type is Location:
            children = DbHandler.UserHandlerDb.get_divisions(root)   
        elif root_type is Division:
            children = DbHandler.UserHandlerDb.get_departaments(root)    
        elif root_type is Departament:
            pass
        elif root_type is Group:
            pass

        for child in children:
            root.add_child(child, root_type(child))

        return root

    def determine_type(path: str) -> Root:
        splitted_path = path.split('_')
        name = splitted_path[-1]

        if name == 'Брусника':
            return Main(path)
        elif '.' in name or name == "Дирекция" or name == "Штаб":
            return Location(path)
        elif len(name.split()) >= 2 and name.split()[1] == 'область':
            return Location(path)
        elif "Подразделение" in name:
            return Division(path)
        elif "Отдел" in name:
            return Departament(path)
        elif "Группа" in name:
            return Group(path)
        

        