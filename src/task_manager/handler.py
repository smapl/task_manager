import psycopg2

from loguru import logger

from .utils import generate_token, give_args


class work_db(object):
    def __init__(self, postgre_login: str, postgre_password):

        self.connection = psycopg2.connect(
            dbname="users",
            user=postgre_login,
            password=postgre_password,
            host="localhost",
        )
        self.cursor = self.connection.cursor()
        self.table_name_user = "users_data"
        self.table_name_task = "tasks"

    def create_user(self, login: str, password: str):
        token = generate_token()

        try:

            self.cursor.execute(
                f"""
                    INSERT INTO {self.table_name_user} 
                    (login, password, authtoken) 
                    VALUES (%(login)s, %(password)s, '{token}');
                """,
                {"login": login, "password": password},
            )

            self.connection.commit()
            self._disconnect()

            return token

        except Exception as ex:
            logger.error(ex)
            return ex

    def create_task(
        self,
        name: str,
        description: str,
        status: str,
        create_datetime,
        planned_completed,
        user_token,
    ):

        status_list = ["new", "planned", "work", "completed"]
        status = status.lower()
        if status not in status_list:
            return "entered status error"

        create_datetime = str(create_datetime)

        print(f"\n{create_datetime}\n{planned_completed}\n")

        try:

            self.cursor.execute(
                f"""
                    SELECT id FROM {self.table_name_user} 
                    WHERE authtoken = %(user_token)s;
                """,
                {"user_token": user_token},
            )
            user_id = self.cursor.fetchall()[0][0]

            logger.info(create_datetime)
            logger.info(planned_completed)
            logger.info(user_token)
            logger.info(user_id)

            self.cursor.execute(
                f"""
                    INSERT INTO {self.table_name_task} 
                    (name, description, create_datetime, status, planned_completed, user_id) 
                    VALUES (%(name)s, %(description)s,'{create_datetime}',%(status)s, %(planned_completed)s, '{user_id}');
                """,
                {
                    "name": name,
                    "description": description,
                    "status": status,
                    "planned_completed": planned_completed,
                },
            )

            self.connection.commit()
            self._disconnect()

            return True

        except TypeError as ex:
            logger.error(ex)
            return str(ex)

    def check_task_status(self, user_token: str, status_filter: str):

        self.cursor.execute(
            f"""
                SELECT id FROM {self.table_name_user} 
                WHERE authtoken = %(user_token)s;
            """,
            {"user_token": user_token},
        )
        user_id = self.cursor.fetchall()[0][0]

        if status_filter == None:
            self.cursor.execute(
                f"""
                    SELECT name, description, create_datetime, status, planned_completed 
                    FROM {self.table_name_task} 
                    WHERE user_id = '{user_id}';
                """
            )
            user_tasks = self.cursor.fetchall()

            return user_tasks

        else:
            self.cursor.execute(
                f"""
                    SELECT id, name, description, create_datetime, status, planned_completed 
                    FROM {self.table_name_task} 
                    WHERE user_id = {user_id} AND status = %(status_filter)s;
                """,
                {"status_filter": status_filter},
            )
            user_tasks = self.cursor.fetchall()

            return user_tasks

    def change_task_status(self, task_id: int, user_token: str, new_status: str):
        self.cursor.execute(
            f"""
                SELECT id FROM {self.table_name_user} 
                WHERE authtoken = %(user_token)s;
            """,
            {"user_token": user_token},
        )
        user_id = self.cursor.fetchall()[0][0]

        try:
            self.cursor.execute(
                f"""
                UPDATE {self.table_name_task} 
                SET status = '{new_status}'
                WHERE id = {task_id} and user_id = {user_id}
            
            """
            )
            self.connection.commit()
            self._disconnect()

            return True

        except Exception as ex:
            logger.error(ex)
            return ex

    def _disconnect(self):
        self.connection.close()

        return "disconnected"

