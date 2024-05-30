import openpyxl
import openpyxl.worksheet
from StaffTableDB import StaffTableDB
from Entities.Root import Root
from Entities.Location import Location
from Entities.Departament import Departament
from Entities.Division import Division
from Entities.Group import Group
from Entities.Main import Main


class TreeCollector:
    def __init__(self) -> None:
        self.database = StaffTableDB()
        self.database.connect()

    def get_locations(self):
        root = Main("Брусника")
        children = self.database.get_company_subgroups()
        for child in children:
            root.add_child(child[0], Location(child[0]))

        return root


    def get_root(self, root_name: str) -> Root:
        root = self.determine_type(root_name)
        root_type = type(root)

        if root_type is Location:        
            children = self.database.get_location_subgroups(root.name)         
        elif root_type is Division:
            children = self.database.get_division_subgroups(root_name.replace("\"", "\\\""))    
        elif root_type is Departament:
            children = self.database.get_departament_subgroups(root_name.replace("\"", "\\\""))
        elif root_type is Group:
            children = self.database.get_staff_by_group(root_name.replace("\"", "\\\""))

        for child in children:
            root.add_child(child, root_type(child))

        return root

    def determine_type(self, root_name: str) -> Root:
        splitted_name = root_name.split()
        if len(splitted_name) < 2:
            return Location(root_name)
        elif splitted_name[0] == "Подразделение":
            return Division(root_name)
        elif splitted_name[0] == "Отдел":
            return Departament(root_name)
        elif splitted_name[0] == "Группа":
            return Group(root_name)
        

        