from ExcelParser import DbHandler, ExcelParser, UserDb
from Entities.Root import Root
from Entities.Location import Location
from Entities.Department import Department
from Entities.Division import Division
from Entities.Group import Group
from Entities.Main import Main


class TreeCollector:


    def get_root(path: str) -> Root:
        splitted_path = TreeCollector.split_path(path)

        root = DbHandler.UserHandlerDb.get_root(splitted_path)
        return root
    
    def split_path(path: str):
        splitted_path = path.split('_')

        result = {
            "root" : None,
            "location" : None,
            "division" : '',
            "department" : None,
            "group" : None,
            "destination" : None,
            "person" : None
        }

        for index, name in enumerate(splitted_path):
            data_type = TreeCollector.determine_type(name)
            result[data_type] = name
            if index == len(splitted_path) - 1:
                result["destination"] = data_type

        

        return result


    def determine_type(name: str) -> Root:

        if name == 'Брусника':
            return "root"
        elif '.' in name or name == "Дирекция" or name == "Штаб":
            return "location"
        elif len(name.split()) >= 2 and name.split()[1] == 'область':
            return "location"
        elif "Подразделение" in name:
            return "division"
        elif "Отдел" in name:
            return "department"
        elif "Группа" in name:
            return "group"
        elif "БСЗ" in name:
            return "person"
        
    def get_filter_data():

        return {
                "locations" : DbHandler.UserHandlerDb.get_locations(),
                "divisions" : DbHandler.UserHandlerDb.get_divisions(),
                "departments" : DbHandler.UserHandlerDb.get_departments(),
                "groups" : DbHandler.UserHandlerDb.get_groups()
        }
    
    def get_path():
        return DbHandler.UserHandlerDb.get_path("отдел", "Отдел \"Бельгия\"")
   


     
        