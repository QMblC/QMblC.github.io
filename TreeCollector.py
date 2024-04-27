import openpyxl
import openpyxl.worksheet
from StaffTableDB import StaffTableDB
from Entities.Root import Root
from Entities.Location import Location


class TreeCollector:
    def __init__(self) -> None:
        self.database = StaffTableDB()
        self.database.connect()

    def get_root(self, root_name):
        pass

    def determine_type(self, root_name: str) -> Root:
        splitted_name = root_name.split()
        if len(splitted_name) > 0:
            return Location(root_name)
        elif splitted_name[0] == "Подразделение":
            pass
        elif splitted_name[0] == "Отдел":
            pass
        elif splitted_name[0] == "Группа":
            pass
        