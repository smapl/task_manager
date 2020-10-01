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
        self.table_name = "users_data"


    def create_user(self, login:str, password:str):
        token = generate_token()

        try:
            self.cursor.execute(f"""insert into {self.table_name} (login, password, authtoken) values (%(login)s, %(password)s, '{token}');""", {"login":login, "password":password})
            self.connection.commit()
            self._disconnect()

            return token

        except Exception as ex:
            logger.error(ex)
            return "error"
        
        
    def _disconnect(self):
        self.connection.close()

        return "disconnected"