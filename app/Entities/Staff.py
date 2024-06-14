class Staff:
    def __init__(self, id, name, profession) -> None:
        self.id = id
        self.location = ""
        self.division = ""
        self.departament = ""
        self.team = ""
        self.name = name
        self.profession = profession
        self.job_type = ""

    def set_location(self, value: str):
        if value == None:
            self.location = None
        else:
            self.location = value

    def set_division(self, value: str):
        if value == None:
            self.di = None
        else:
            self.division = value

    def set_departament(self, value: str):
        if value == None:
            self.departament = None
        else:
            self.departament = value

    def set_team(self, value: str):
        if value == None:
            self.team = None
        else:
            self.team = value

    def set_type(self, value: str):
        if value == None:
            self.job_type = None
        else:
            self.job_type = value