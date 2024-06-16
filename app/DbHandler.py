from cfg import db, app
from DbModels import UserDb
from Entities.Staff import Staff
from Entities.Root import Root


class DbHandler:
    class UserHandlerDb:
        @staticmethod
        def add_user(data: Staff):
            with app.app_context():
                user = UserDb(id = data.id,
                    location = data.location,
                    division = data.division,
                    departament = data.departament,
                    team = data.team,
                    profession = data.profession,
                    name = data.name,
                    job_type = data.job_type)
                
                db.session.add(user)
                db.session.commit()
                          
        def get_user(user_id: str) -> UserDb:
            with app.app_context():
                user = db.session.query(UserDb).get(user_id)
                return user
            
        def get_locations_children():
            with app.app_context():
                locations = db.session.query(UserDb).with_entities(UserDb.location).distinct().all()

                result = []

                for location in locations:

                    children = DbHandler.UserHandlerDb.get_children(db.session.query(UserDb).filter(UserDb.location == location[0]).with_entities(UserDb.division).distinct().all())

                    line = {
                        "name" : location[0],
                        "parents" : {"root" : "Брусника"},
                        "children" : children
                    }

                    result.append(line)

                return result
            
        def get_divisions_children():
            divisions = db.session.query(UserDb).with_entities(UserDb.division, UserDb.location).distinct().all()

            result = []

            for division in divisions:

                children = DbHandler.UserHandlerDb.get_children(db.session.query(UserDb).filter(UserDb.division == division[0]).with_entities(UserDb.departament).distinct().all())

                if division[0] == '':
                    line = {
                        "name" : "Отсутствует",
                        "parents" : {"root" : "Брусника",
                            "location" : division[1]
                        },
                        "children" : children
                    }
                else:
                    line = {
                        "name" : division[0],
                        "parents" : {"root" : "Брусника",
                            "location" : division[1]
                        },
                        "children" : children
                    }

                
                flag = False
                
                for i in result:
                    if i["name"] == line["name"]:
                        flag = True
                        break

                if flag:
                    continue
                else:
                    result.append(line)

            return result
            
        def get_departments_children():
            departments = db.session.query(UserDb).with_entities(UserDb.departament).distinct().all()

            result = []

            for department in departments:

                children = DbHandler.UserHandlerDb.get_children(db.session.query(UserDb).filter(UserDb.departament == department[0]).with_entities(UserDb.team).distinct().all())

                if department[0] == None:
                    example = db.session.query(UserDb).filter(UserDb.departament == department[0]).first()
                    ex_location = example.location if example.location else "Отсутствует"
                    ex_division = example.division if example.division else "Отсутствует"
                    line = {
                        "name" : "Отсутствует",
                        "parents" : {"root" : "Брусника",
                            "location" : ex_location,
                            "division" : ex_division,
                        },
                        "children" : children
                    }
                else:
                    example = db.session.query(UserDb).filter(UserDb.departament == department[0]).first()
                    ex_location = example.location if example.location else "Отсутствует"
                    ex_division = example.division if example.division else "Отсутствует"
                    line = {
                        "name" : department[0],
                        "parents" : {"root" : "Брусника",
                            "location" : ex_location,
                            "division" : ex_division,
                        },
                        "children" : children
                    }
                
                flag = False
                
                for i in result:
                    if i["name"] == line["name"]:
                        flag = True
                        break

                if flag:
                    continue
                else:
                    result.append(line)

            return result
        
        def get_groups_children():
            groups = db.session.query(UserDb).with_entities(UserDb.team).distinct().all()

            result = []

            for group in groups:

                if group[0] == None:
                    example = db.session.query(UserDb).filter(UserDb.team == group[0]).first()
                    ex_location = example.location if example.location else "Отсутствует"
                    ex_division = example.division if example.division else "Отсутствует"
                    ex_department = example.departament if example.departament else "Отсутствует"
                    line = {
                        "name" : "Отсутствует",
                        "parents" : {"root" : "Брусника",
                            "location" : ex_location,
                            "division" : ex_division,
                            "department" : ex_department
                        },
                        "children" : []
                    }
                else:
                    example = db.session.query(UserDb).filter(UserDb.team == group[0]).first()
                    ex_location = example.location if example.location else "Отсутствует"
                    ex_division = example.division if example.division else "Отсутствует"
                    ex_department = example.departament if example.departament else "Отсутствует"
                    line = {
                        "name" : group[0],
                        "parents" : {"root" : "Брусника",
                            "location" : ex_location,
                            "division" : ex_division,
                            "department" : ex_department
                        },
                        "children" : []
                    }
                
                flag = False
                
                for i in result:
                    if i["name"] == line["name"]:
                        flag = True
                        break

                if flag:
                    continue
                else:
                    result.append(line)

            return result

        def get_children(arr):
            children = []
            for child in arr:
                if child[0] == None or child[0] == '':
                    children.append("Отсутствует")
                else:
                    children.append(child[0])
            return children
                
        def get_locations():
            with app.app_context():
                
                location_query = db.session.query(UserDb)

                locations = [x[0] for x in location_query.with_entities(UserDb.location).distinct().all()]

                return locations
            
        def get_divisions(root: Root):
            with app.app_context():

                location_name = root.name

                division_query = db.session.query(UserDb).filter(UserDb.location == location_name)

                a = division_query.all()

                divisions = [x[0] for x in division_query.with_entities(UserDb.division).distinct().all() if (x[0] != '' and x[0] != None)]

                for div in division_query.filter(UserDb.division == '').with_entities(UserDb.departament).distinct().all():
                    if (div[0] != '' and div[0] != None):
                        divisions.append(div[0])

                for dep in division_query.filter(UserDb.division == '')\
                    .filter(UserDb.departament == None).with_entities(UserDb.team).distinct().all():
                    if (dep[0] != None):
                        divisions.append(dep[0])
                
                for line in division_query.filter(UserDb.division == '')\
                    .filter(UserDb.departament == None)\
                    .filter(UserDb.team == None).all():
                    if (line.team == None):
                        divisions.append(line.id)

                return divisions
            
        def get_departaments(root: Root):
            
            with app.app_context():

                division_name = root.name
                location_name = root.path.split('_')[1]
                
                departament_query = db.session.query(UserDb).filter(UserDb.location == location_name).filter(UserDb.division == division_name)

                a = departament_query.all()

                departaments = [x[0] for x in departament_query.with_entities(UserDb.departament).distinct().all() if x[0] != None]

                for dep in departament_query.filter(UserDb.departament == None).with_entities(UserDb.team).distinct().all():
                    if (dep[0] != None):
                        departaments.append(dep[0])

                for id in departament_query.filter(UserDb.departament == None).filter(UserDb.team == None).with_entities(UserDb.id).distinct().all():
                    if (id[0] != None):
                        departaments.append(id[0])

                return departaments