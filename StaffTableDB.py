import mysql.connector
from mysql.connector import MySQLConnection, Error
from configparser import ConfigParser
from Entities.Staff import Staff

class StaffTableDB:

    def connect(self):
        try:

            self.connection = mysql.connector.connect(host='localhost',
                                        database='python_mysql',
                                        user='root',
                                        password='6124HuKuTa')
            if self.connection.is_connected():
                
                print('Connected to MySQL database')
                return self.connection

        except Error as e:
            print(e)
            return None

    def create_user_table(self):
        create_movies_table_query = """
        CREATE TABLE users(
            id varchar(20) PRIMARY KEY,
            location VARCHAR(100),
            division VARCHAR(100),
            departament VARCHAR(100),
            team VARCHAR(100),
            profession varchar(100),
            name VARCHAR(100),
            type varchar(100)
        )
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(create_movies_table_query)
                self.connection.commit()
                print('created')
        except Error as e:
            print(e)

    def delete_user_table(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""DROP TABLE users""")
                self.connection.commit()
                print("deleted")
        except Error as e:
            print(e)

    def insert_staff(self, staff: Staff):
        if self.contains(staff.id):
            return      
         
        query = f"INSERT INTO users(id, location, division, departament, team, name, profession, type) VALUES(\"{staff.id}\",\"{staff.location}\", \"{staff.division}\", \"{staff.departament}\", \"{staff.team}\", \"{staff.name}\", \"{staff.profession}\", \"{staff.type}\")"
        
        try:
   
            with self.connection.cursor() as cursor: 
                cursor.execute(query)
                self.connection.commit()
        except Error as e:
            print(e)

    def contains(self, id):
        select_movies_query = f"SELECT * FROM users WHERE id = \"{id}\""
        with self.connection.cursor() as cursor:
            cursor.execute(select_movies_query)
            result = cursor.fetchall()
            return len(result) > 0

    def get_staff(self):
        select_movies_query = "SELECT * FROM users"
        with self.connection.cursor() as cursor:
            cursor.execute(select_movies_query)
            result = cursor.fetchall()
            for row in result:
                print(row)
    
    def get_staff_by_id(self, id) -> Staff:
        try:
            staff = Staff(None, None, None)
            select_movies_query = f"SELECT * FROM users WHERE id = \"{id}\""
            with self.connection.cursor() as cursor:
                cursor.execute(select_movies_query)
                result = cursor.fetchall()
                for row in result:
                    staff = Staff(row[0], row[6], row[5])
                    staff.set_location(row[1])
                    staff.set_division(row[2])
                    staff.set_departament(row[3])
                    staff.set_team(row[4])
                    staff.set_type(row[7])
                
        except Error as e:
            return staff
        finally:
            return staff
        
    def get_location_subgroups(self):
        pass

    def get_division_subgroups(self):
        pass

    def get_departament_subgroups(self):
        pass

    def get_staff_by_group(self):
        pass


if __name__ == '__main__':
    
    table = StaffTableDB()

    table.connect()
    #table.delete_user_table()
    table.create_user_table()

    while True:
        request = input()
        if request.split()[0] == "add":
            table.insert_staff(request.split()[1], request.split()[2])
        elif request.split()[0] == "get":
            table.get_staff()
        elif request.split()[0] == "getby":
            print(table.get_staff_by_id(request.split()[1]).name)
        elif request.split()[0] == "con":
            table.contains(request.split()[1])
        else:
            table.connection.close()
            break