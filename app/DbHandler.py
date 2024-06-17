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
            
        def get_locations():
            with app.app_context():
                locations = [x[0] for x in db.session.query(UserDb).with_entities(UserDb.location).distinct().all()]

                return locations
            
        def get_divisions():
            divisions = db.session.query(UserDb).with_entities(UserDb.division).distinct().all()

            result = []

            for division in divisions:
     
                if division[0] == '':
                    result.append("Отсутствует")
                else:
                    result.append(division[0])

            return result
            
        def get_departments():
            departments = db.session.query(UserDb).with_entities(UserDb.departament).distinct().all()

            result = []

            for department in departments:          

                if department[0] == None:
                    result.append("Отсутствует")
                else:
                    result.append(department[0])

            return result
        
        def get_groups():
            groups = db.session.query(UserDb).with_entities(UserDb.team).distinct().all()

            result = []

            for group in groups:

                if group[0] == None:
                    result.append("Отсутствует")
                else:
                    result.append(group[0])

            return result

        def get_path(data_type: str, data: str):
            if data_type == "локация":
                request = db.session.query(UserDb).filter(UserDb.location == data)
                divisions = DbHandler.UserHandlerDb.fill_arr(request.with_entities(UserDb.division).distinct().all())
                departments = DbHandler.UserHandlerDb.fill_arr(request.with_entities(UserDb.departament).distinct().all())
                groups = DbHandler.UserHandlerDb.fill_arr(request.with_entities(UserDb.team).distinct().all())

                return{
                    "locations" : data,
                    "divisions" : divisions,
                    "departments" : departments,
                    "groups" : groups
                }
            elif data_type == "подразделение":
                request = db.session.query(UserDb).filter(UserDb.division == data)
                departments = DbHandler.UserHandlerDb.fill_arr(request.with_entities(UserDb.departament).distinct().all())
                locations = DbHandler.UserHandlerDb.fill_arr(request.with_entities(UserDb.location).distinct().all())
                groups = DbHandler.UserHandlerDb.fill_arr(request.with_entities(UserDb.team).distinct().all())

                return{
                    "departments" : departments,
                    "divisions" : data,
                    "locations" : locations,
                    "groups" : groups
                }
            elif data_type == "отдел":
                request = db.session.query(UserDb).filter(UserDb.departament == data)
                divisions = DbHandler.UserHandlerDb.fill_arr(request.with_entities(UserDb.division).distinct().all())
                locations = DbHandler.UserHandlerDb.fill_arr(request.with_entities(UserDb.location).distinct().all())
                groups = DbHandler.UserHandlerDb.fill_arr(request.with_entities(UserDb.team).distinct().all())

                return{
                    "divisions" : divisions,
                    "departments" : data,
                    "locations" : locations,
                    "groups" : groups
                }
            elif data_type == "группа":
                request = db.session.query(UserDb).filter(UserDb.team == data)
                divisions = DbHandler.UserHandlerDb.fill_arr(request.with_entities(UserDb.division).distinct().all())
                locations = DbHandler.UserHandlerDb.fill_arr(request.with_entities(UserDb.location).distinct().all())
                departments = DbHandler.UserHandlerDb.fill_arr(request.with_entities(UserDb.departament).distinct().all())

                return{
                    "divisions" : divisions,
                    "locations" : locations,
                    "groups" : data,
                    "departments" : departments
                }
            
        def fill_arr(arr):
            result = []
            for i in arr:
                if i[0] == '' or i[0] == None:
                    result.append("Отсутствует")
                else:
                    result.append(i[0])
            
            return result
        
        def get_root(path: dict):
            query = db.session.query(UserDb)

            if path["destination"] == "root":

                result = DbHandler.UserHandlerDb.get_root_children(path, query)

                return result

            elif path["destination"] == "location":
                query = query.filter(UserDb.location == path["location"])

                result = DbHandler.UserHandlerDb.get_location_children(path, query)

                return result
            
            elif path["destination"] == "division":
                query = query.filter(UserDb.location == path["location"]).filter(UserDb.division == path["division"])

                result = DbHandler.UserHandlerDb.get_division_children(path, query)

                return result
            
            elif path["destination"] == "department":
                query = query.filter(UserDb.location == path["location"]).filter(UserDb.division == path["division"]).filter(UserDb.departament == path["department"])

                result = DbHandler.UserHandlerDb.get_department_children(path, query)

                return result
            
            elif path["destination"] == "group":
                query = query.filter(UserDb.location == path["location"]).filter(UserDb.division == path["division"])\
                    .filter(UserDb.departament == path["department"]).filter(UserDb.team == path["group"])
                
                result = DbHandler.UserHandlerDb.get_group_children(path, query)

                return result
            
            elif path["destination"] == "person":
                person = query.get(path["person"])

                current_path = f"/api/get-root/{path['root']}_{path['location']}_"

                if path["division"] != '':
                    current_path += f"{path['division']}_"
                if path["department"] != None:
                    current_path += f"{path['department']}_"
                if path["group"] != None:
                    current_path += f"{path['group']}_"

                current_path += path["person"]

                result = {
                    "id" : person.id,
                    "name": person.name,
                    "profession": person.profession,
                    "type": person.job_type,
                    "children": [],
                    "path" : current_path
                }

                return result


        def get_root_children(path: str, query):
            locations = [x[0] for x in query.with_entities(UserDb.location).distinct().all()]

            result = {
                "name" : path["root"],
                "path" : f"/api/get-root/{path['root']}",
                "children" : []
            }

            for location in locations:
                location_query = db.session.query(UserDb).filter(UserDb.location == location)

                people_amount = len(location_query.all())

                divisions = location_query.with_entities(UserDb.division).distinct().all()
                division_amount = len([x[0] for x in divisions if x[0] != None and x[0] != ''])

                departments = location_query.with_entities(UserDb.departament).distinct().all()
                department_amount = len([x[0] for x in departments if x[0] != None] )

                groups = location_query.with_entities(UserDb.team).distinct().all()
                group_amount = len([x[0] for x in groups if x[0] != None])

                child = {
                    "name" : location,
                    "info" : {
                        "people" : people_amount,
                        "divisions" : division_amount,
                        "departments" : department_amount,
                        "groups" : group_amount
                    },
                    "path-to-children" : f"/api/get-root/{path['root']}_{location}"
                }

                result["children"].append(child)
            
            return result

        def get_location_children(path: str, query):
            divisions = [x[0] for x in query.with_entities(UserDb.division).distinct().all() if x[0] != None and x[0] != '']

            result = {
                "name" : path["location"],
                "path" : f"/api/get-root/{path['root']}_{path['location']}",
                "children" : []
            }

            for division in divisions:
                division_query = query.filter(UserDb.division == division)

                people_amount = len(division_query.all())

                departments = division_query.with_entities(UserDb.departament).distinct().all()
                department_amount = len([x[0] for x in departments if x[0] != None] )

                groups = division_query.with_entities(UserDb.team).distinct().all()
                group_amount = len([x[0] for x in groups if x[0] != None])

                child = {
                    "name" : division,
                    "info" : {
                        "people" : people_amount,
                        "divisions" : None,
                        "departments" : department_amount,
                        "groups" : group_amount
                    },
                    "path-to-children" : f"{result['path']}_{division}"
                }

                result["children"].append(child)
            
            remaining_departments = [x[0] for x in query.filter(UserDb.division == '').with_entities(UserDb.departament).distinct().all() if x[0] != None and x[0] != '']

            for department in remaining_departments:
                department_query = query.filter(UserDb.division == '').filter(UserDb.departament == department)

                people_amount = len(department_query.all())

                groups = department_query.with_entities(UserDb.team).distinct().all()
                group_amount = len([x[0] for x in groups if x[0] != None])

                child = {
                    "name" : department,
                    "info" : {
                        "people" : people_amount,
                        "divisions" : None,
                        "departments" : None,
                        "groups" : group_amount
                    },
                    "path-to-children" : f"{result['path']}_{department}"
                }

                result["children"].append(child)
            
            remaining_groups = [x[0] for x in query.filter(UserDb.division == '').filter(UserDb.departament == None).with_entities(UserDb.team).distinct().all() if x[0] != None]
            
            for group in remaining_groups:
                group_query = query.filter(UserDb.division == '').filter(UserDb.departament == None).filter(UserDb.team == group)

                people_amount = len(group_query.all())

                child = {
                    "name" : group,
                    "info" : {
                        "people" : people_amount,
                        "divisions" : None,
                        "departments" : None,
                        "groups" : None
                    },
                    "path-to-children" : f"{result['path']}_{group}"
                }

                result["children"].append(child)

            remaining_people = query.filter(UserDb.division == '').filter(UserDb.departament == None).filter(UserDb.team == None).with_entities(UserDb.id).distinct().all()
            
            for person in remaining_people:

                child = {
                    "name" : person[0],
                    "info" : {
                        "people" : None,
                        "divisions" : None,
                        "departments" : None,
                        "groups" : None
                    },
                    "path-to-children" : f"{result['path']}_{person[0]}"
                }

                result["children"].append(child)

            return result
        
        def get_division_children(path: str, query):
            departments = [x[0] for x in query.with_entities(UserDb.departament).distinct().all() if x[0] != None and x[0] != '']

            current_path = f"/api/get-root/{path['root']}_{path['location']}_{path['division']}"

            result = {
                "name": path["division"],
                "path" : current_path,
                "children" : []
            }

            for department in departments:
                department_query = query.filter(UserDb.departament == department)

                people_amount = len(department_query.all())

                groups = department_query.with_entities(UserDb.team).distinct().all()
                group_amount = len([x[0] for x in groups if x[0] != None])

                child = {
                    "name" : department,
                    "info" : {
                        "people" : people_amount,
                        "divisions" : None,
                        "departments" : None,
                        "groups" : group_amount
                    },
                    "path-to-children" : f"{result['path']}_{department}"
                }

                result["children"].append(child)

            remaining_groups = [x[0] for x in query.filter(UserDb.departament == None).with_entities(UserDb.team).distinct().all() if x[0] != None]
            
            for group in remaining_groups:
                group_query = query.filter(UserDb.departament == None).filter(UserDb.team == group)

                people_amount = len(group_query.all())

                child = {
                    "name" : group,
                    "info" : {
                        "people" : people_amount,
                        "divisions" : None,
                        "departments" : None,
                        "groups" : None
                    },
                    "path-to-children" : f"{result['path']}_{group}"
                }

                result["children"].append(child)

            remaining_people = query.filter(UserDb.departament == None).filter(UserDb.team == None).with_entities(UserDb.id).distinct().all()
        
            for person in remaining_people:

                child = {
                    "name" : person[0],
                    "info" : {
                        "people" : None,
                        "divisions" : None,
                        "departments" : None,
                        "groups" : None
                    },
                    "path-to-children" : f"{result['path']}_{person[0]}"
                }

                result["children"].append(child)

            return result
        
        def get_department_children(path: str, query):
            if path["division"] == '':
                current_path = f"/api/get-root/{path['root']}_{path['location']}_{path['department']}"
            else:
                current_path = f"/api/get-root/{path['root']}_{path['location']}_{path['division']}_{path['department']}"

            result = {
                "name": path["department"],
                "path" : current_path,
                "children" : []
            }

            groups = [x[0] for x in query.with_entities(UserDb.team).distinct().all() if x[0] != None and x[0] != '']

            for group in groups:
                department_query = query.filter(UserDb.team == group)

                people_amount = len(department_query.all())

                child = {
                    "name" : group,
                    "info" : {
                        "people" : people_amount,
                        "divisions" : None,
                        "departments" : None,
                        "groups" : None
                    },
                    "path-to-children" : f"{result['path']}_{group}"
                }

                result["children"].append(child)

            return result
        
        def get_group_children(path: str, query):
            current_path = f"/api/get-root/{path['root']}_{path['location']}_"

            if path["division"] != '':
                current_path += f"{path['division']}_"
            if path["department"] != None:
                current_path += f"{path['department']}_"
            
            current_path += path["group"]

            result = {
                "name": path["group"],
                "path" : current_path,
                "children" : []
            }

            people = [x[0] for x in query.with_entities(UserDb.id).distinct().all() if x[0] != None and x[0] != '']

            for person in people:
                child = {
                    "name" : person,
                    "info" : {
                        "people" : None,
                        "divisions" : None,
                        "departments" : None,
                        "groups" : None
                    },
                    "path-to-children" : f"{result['path']}_{person}"
                }

                result["children"].append(child)

            return result     


