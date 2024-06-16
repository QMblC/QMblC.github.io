from ExcelParser import DbHandler, ExcelParser, UserDb
from Entities.Root import Root
from Entities.Location import Location
from Entities.Department import Department
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
        elif root_type is Department:
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
            return Department(path)
        elif "Группа" in name:
            return Group(path)
        
    def get_filter_data():

        locations = []

        return {
                "locations" : DbHandler.UserHandlerDb.get_locations_children(),
                "divisions" : DbHandler.UserHandlerDb.get_divisions_children(),
                "departments" : DbHandler.UserHandlerDb.get_departments_children(),
                "groups" : DbHandler.UserHandlerDb.get_groups_children()
        }

        

        