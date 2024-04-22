import mysql.connector
from mysql.connector import Error

class UserTable:
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
            id INT AUTO_INCREMENT PRIMARY KEY,
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

    def insert_user(self):
        query = "INSERT INTO users(id,name) "
        pass

if __name__ == '__main__':
    table = UserTable()
    table.connect()
    table.create_user_table()
    