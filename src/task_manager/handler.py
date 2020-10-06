import time

import psycopg2

from loguru import logger
from datetime import datetime

from .utils import (
    generate_token,
    give_args,
    definitions_user_id,
    correct_check_task,
    correct_check_history,
)


class MainHandler(object):
    def __init__(
        self, postgre_login: str, postgre_password: str, host: str, db_name: str
    ):
        while True:
            try:
                self.connection = psycopg2.connect(
                    dbname=db_name,
                    user=postgre_login,
                    password=postgre_password,
                    host=host,
                )
                break

            except Exception as ex:
                logger.error(ex)

                logger.info("attempt to reconnect after 10 seconds")
                time.sleep(10)

        self.cursor = self.connection.cursor()
        self.table_name_user = "users_data"
        self.table_name_task = "tasks"
        self.table_old_version = "old_version"
        self.status_list = ["new", "planned", "work", "completed"]

    def create_user(self, login: str, password: str) -> str:
        token = generate_token()
        self.cursor.execute(
            f"""
                            SELECT id FROM {self.table_name_user} 
                            WHERE name = '{login}';
                            """
        )

        user_exist = self.cursor.fetchall()[0][0]
        if user_exist != None:
            return {"error": "user with the same username already exists"}

        try:
            self.cursor.execute(
                f"""
                    INSERT INTO {self.table_name_user} 
                    (login, password, authtoken) 
                    VALUES ('{login}', '{password}', '{token}');
                """
            )

        except Exception as ex:
            logger.error(ex)
            return {"error": ex}

        self.connection.commit()

        return {"user_token": token}

    def create_task(
        self,
        name: str,
        description: str,
        status: str,
        create_datetime,
        planned_completed,
        user_token,
    ):
        if len(name) > 100:
            return {"error": "you have exceeded the character limit (30)"}

        elif len(description) > 300:
            return {"error": "you have exceeded the character limit (300)"}

        status = status.lower()
        if status not in self.status_list:
            return {"error": "entered status error"}

        create_datetime = str(create_datetime)

        user_id = definitions_user_id(user_token)

        try:
            self.cursor.execute(
                f"""
                    INSERT INTO {self.table_name_task} 
                    (name, description, create_datetime, status, planned_completed, user_id) 
                    VALUES ('{name}', '{description}','{create_datetime}','{status}', '{planned_completed}', {user_id});
                """
            )

            self.connection.commit()

        except Exception as ex:
            logger.error(ex)

            return {"error": ex}

        return {"result": "success"}

    def check_task_status(self, user_token: str, status_filter: dict) -> dict:

        user_id = definitions_user_id(user_token)

        if status_filter == None:

            try:
                self.cursor.execute(
                    f"""
                        SELECT id, name, description, create_datetime, status, planned_completed 
                        FROM {self.table_name_task} 
                        WHERE user_id = {user_id};
                    """
                )
                user_tasks = self.cursor.fetchall()

                tasks = correct_check_task(user_tasks)
                return {"result": tasks}

            except Exception as ex:
                logger.error(ex)
                return {"error": ex}

        else:
            try:
                s_filter = ""
                for key in status_filter:
                    s_filter += f"{key}='{status_filter[key]}' AND "

                s_filter = s_filter[:-5]

                self.cursor.execute(
                    f"""
                        SELECT id, name, description, create_datetime, status, planned_completed 
                        FROM {self.table_name_task} 
                        WHERE user_id = {user_id} AND {s_filter};
                    """,
                )
                user_tasks = self.cursor.fetchall()

                tasks = correct_check_task(user_tasks)

                return {"result": tasks}

            except Exception as ex:
                logger.error(ex)

                return {"error": ex}

    def change_task_rows(self, task_id: int, user_token: str, new_values: dict):

        user_id = definitions_user_id(user_token)

        try:
            self.cursor.execute(
                f"""
                    SELECT name FROM {self.table_name_task} 
                    WHERE id = {task_id} AND user_id = {user_id};
                """,
            )

        except Exception as ex:
            logger.error(ex)

            return {"error": ex}

        validity = self.cursor.fetchall()
        if len(validity) == 0:
            return {"error": "access to this task is denied"}

        else:
            change_query = ""
            finish_datetime = None
            for name_column in new_values:

                if (
                    name_column == "status"
                    and new_values[name_column] not in self.status_list
                ):
                    return {"error": "it is impossible to put such a status"}

                if name_column == "status" and new_values[name_column] == "completed":
                    finish_datetime = str(datetime.now())
                    change_query += f"finish_datetime = '{finish_datetime}', "

                change_query += f"{name_column} = '{new_values[name_column]}', "

            change_query = change_query[:-2]
            try:
                self.cursor.execute(
                    f"""
                        SELECT id, name, description, status, planned_completed
                        FROM {self.table_name_task}
                        WHERE id = {task_id} and user_id = {user_id};  
                    """
                )
            except Exception as ex:
                logger.error(ex)

                return {"error": ex}

            old_version_task = self.cursor.fetchall()
            old_version_task = {
                "id": old_version_task[0][0],
                "name": old_version_task[0][1],
                "description": old_version_task[0][2],
                "status": old_version_task[0][3],
                "planned_completed": old_version_task[0][4],
            }

            try:
                self.cursor.execute(
                    f"""
                    UPDATE {self.table_name_task}
                    SET {change_query}
                    WHERE id = {task_id} and user_id = {user_id};

                """
                )
                self.connection.commit()

            except Exception as ex:
                logger.error(ex)

                return {"error": ex}

            changed_rows = [key for key in new_values]
            str_change_rows = ", ".join(changed_rows) + ", change_datetime, task_id"
            datetime_change = str(datetime.now())

            to_old_version = ""
            for key in changed_rows:

                to_old_version += f"'{old_version_task[key]}', "

            to_old_version = to_old_version + f"'{datetime_change}', {task_id}"

            try:
                self.cursor.execute(
                    f"""
                        INSERT INTO {self.table_old_version} ({str_change_rows})
                        VALUES ({to_old_version});
                    """
                )

                self.connection.commit()

            except Exception as ex:
                logger.error(ex)

                return {"error": ex}

            return {"result": "success"}

    def check_history_change(self, user_token, task_id):
        user_id = definitions_user_id(user_token)

        try:
            self.cursor.execute(
                f"""
                    SELECT name FROM {self.table_name_task} 
                    WHERE id = {task_id} AND user_id = {user_id};
                """,
            )
            validity = self.cursor.fetchall()

        except Exception as ex:
            logger.error(ex)

            return {"error": ex}

        if len(validity) == 0:
            return {"error": "access to this task is denied"}

        else:
            try:
                self.cursor.execute(
                    f"""
                        SELECT name, description, status, planned_completed, change_datetime
                        FROM {self.table_old_version}
                        WHERE task_id = {task_id};
                    """
                )
            except Exception as ex:
                logger.error(ex)

                return {"error": ex}

            history = self.cursor.fetchall()
            history_dict = correct_check_history(history)

            return {"resilt": history_dict}

    def _disconnect(self):
        self.connection.close()

        return "disconnected"

