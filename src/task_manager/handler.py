import psycopg2

from loguru import logger

from .utils import generate_token, give_args


class work_db(object):
    def __init__(self):
        postgre_login, postgre_password = give_args()

        self.connection = psycopg2.connect(
                dbname="users", user=postgre_login, password=postgre_password, host="localhost"
            )
        self.cursor = self.connection.cursor()
        self.table_name_user = "users_data"
        self.table_name_task = "tasks"

    def create_user(self, login:str, password:str):
        token = generate_token()

        try:

            self.cursor.execute(
                                    f"""insert into {self.table_name_user} 
                                    (login, password, authtoken) 
                                    values (%(login)s, %(password)s, '{token}');""",
                                     {"login":login, "password":password}
                                )

            self.connection.commit()
            self._disconnect()

            return token

        except Exception as ex:
            logger.error(ex)
            return ex
        
    def create_task(self, name:str, description:str, status:str, create_datetime, planned_completed, user_token):
        try:
            user_id = self.cursor(f"SELECT id FROM users_data WHERE authtoken=%(user_token)s", {"user_token":user_token})
            self.cursor.execute(
                                    f"""insert into {self.table_name_task}/
                                    (name, description, create_datetime, status, planned_completed, user_id)/
                                    values (%(name)s, %(description)s,{create_datetime},%(status)s, %(planned_completed)s, '{user_id}');""",
                                    {"name":name, "description":description, "status":status, "planned_completed":planned_completed}
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