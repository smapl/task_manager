import psycopg2

from loguru import logger

from .utils import generate_token, give_args, definitions_user_id, correct_check_task


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
        self.status_list = ["new", "planned", "work", "completed"]

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
        if len(name) > 30:
            return "you have exceeded the character limit (30)"

        elif len(description) > 300:
            return "you have exceeded the character limit (300)"

        status = status.lower()
        if status not in self.status_list:
            return "entered status error"

        create_datetime = str(create_datetime)

        try:

            user_id = definitions_user_id(user_token)

            self.cursor.execute(
                f"""
                    INSERT INTO {self.table_name_task} 
                    (name, description, create_datetime, status, planned_completed, user_id) 
                    VALUES (%(name)s, %(description)s,'{create_datetime}',%(status)s, %(planned_completed)s, {user_id});
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

        user_id = definitions_user_id(user_token)

        if status_filter == None:
            self.cursor.execute(
                f"""
                    SELECT id, name, description, create_datetime, status, planned_completed 
                    FROM {self.table_name_task} 
                    WHERE user_id = {user_id};
                """
            )
            user_tasks = self.cursor.fetchall()

            tasks = correct_check_task(user_tasks)
            return tasks

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

            tasks = correct_check_task(user_tasks)
            return tasks

    def change_task_rows(self, task_id: int, user_token: str, new_values: dict):

        user_id = definitions_user_id(user_token)

        self.cursor.execute(
            f"""
                SELECT name FROM {self.table_name_task} 
                WHERE id = {task_id} AND user_id = {user_id};
            """,
        )
        validity = self.cursor.fetchall()

        if len(validity) == 0:
            return "access to this task is denied"

        else:
            change_query = ""
            for name_column in new_values:

                if (
                    name_column == "status"
                    and new_values[name_column] not in self.status_list
                ):
                    return "it is impossible to put such a status"

                change_query += f"{name_column} = '{new_values[name_column]}', "

            change_query = change_query[:-2]
            self.cursor.execute(
                f"""
                UPDATE {self.table_name_task}
                SET {change_query}
                WHERE id = {task_id} and user_id = {user_id};

            """
            )
            self.connection.commit()
            self._disconnect()

            return True

    def _disconnect(self):
        self.connection.close()

        return "disconnected"

