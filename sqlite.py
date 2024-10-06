import sqlite3


class Database:
    def __init__(self, path_to_db="db.sqlite3"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, id: int, telegram_id: int, phone_number: str):

        sql = """
        INSERT INTO bot_user(id, telegram_id, phone_number) VALUES(?, ?, ?)
        """
        self.execute(sql, parameters=(id, telegram_id, phone_number), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM bot_user
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM bot_user WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM bot_user;", fetchone=True)

    def update_user_data(self, user_data, id):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE bot_user SET {user_data}=? WHERE telegram_id=?
        """
        return self.execute(sql, parameters=(user_data, id), commit=True)

    def get_new_inventories(self, phone_number: str):
        sql = """
        SELECT inv.number FROM inventory as inv
        INNER JOIN inventory_action as ia
        ON inv.id = ia.inventory_id 
        WHERE inv.status = 1 AND ia.send_mgs = false AND inv.sender_phone = ?;
        """
        return self.execute(sql, parameters=(phone_number,), fetchall=True)


def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")
