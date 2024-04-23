import mysql.connector
from mysql.connector import MySQLConnection, Error
from configparser import ConfigParser

class UserTableDB:
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
            location INT,
            division INT,
            departament INT,
            team INT,
            name VARCHAR(100)
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

    def insert_user(self, id,  name, location = 0, division = 0, departament = 0, team = 0):
        query = f"INSERT INTO users(id, location, division, departament, team, name) VALUES(\"{id}\",{location}, {division}, {departament}, {team}, \"{name}\")"

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                self.connection.commit()
                print('added')
        except Error as e:
            print(e)

    def get_users(self):
        select_movies_query = "SELECT * FROM users"
        with self.connection.cursor() as cursor:
            cursor.execute(select_movies_query)
            result = cursor.fetchall()
            for row in result:
                print(row)
    
    def get_user_by_id(self, id):
        select_movies_query = f"SELECT name FROM users WHERE id = {id}"
        with self.connection.cursor() as cursor:
            cursor.execute(select_movies_query)
            result = cursor.fetchall()
            for row in result:
                print(row[0])

if __name__ == '__main__':
    table = UserTableDB()
    table.connect()
    table.delete_user_table()
    table.create_user_table()

    while True:
        request = input()
        if request.split()[0] == "add":
            table.insert_user(request.split()[1], request.split()[2])
        elif request.split()[0] == "get":
            table.get_users()
        elif request.split()[0] == "getby":
            table.get_user_by_id(request.split()[1])
        else:
            table.connection.close()
            break