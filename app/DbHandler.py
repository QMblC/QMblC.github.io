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