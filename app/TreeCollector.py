import openpyxl
import openpyxl.worksheet
from app.StaffTableDB import StaffTableDB
from app.Entities.Root import Root
from app.Entities.Location import Location
from app.Entities.Departament import Departament
from app.Entities.Division import Division
from app.Entities.Group import Group
from app.Entities.Main import Main
from app.ExcelParser import ExcelParser


class TreeCollector:
    def __init__(self) -> None:
        self.database = StaffTableDB()
        try:
            self.database.create_db()
            self.database.connect()
            self.database.create_user_table()

            a = ExcelParser.get_rows("Tables/Structure.xlsx")
            
            for i in a:
                ExcelParser.insert_staff_db(i)
        except:
            print('tc_init_')
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
        

        