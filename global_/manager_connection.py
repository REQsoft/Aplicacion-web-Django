import psycopg2, psycopg2.extras
import pymysql
import cx_Oracle

class ManagerConnection:
    # Constructor
    def __init__(self, manager_db, user, passwd, port, host, dbname=None):

        self.manager_db = manager_db

        self.config_connection = {
            "user": user,
            "password": passwd,
            "host": host,
            "port": int(port),
        }

        if dbname is not None:
            self.config_connection["database"] = dbname
            self.config_oracle = (
                user + "/" + passwd + "@" + host + ":" + str(port) + "/" + dbname
            )
        else:
            self.config_oracle = user + "/" + passwd + "@" + host + ":" + port + "/"

    # Verifica si la connection es correcta
    def check_connection(self):
        if self.manager_db == "mysql":
            try:
                conn = pymysql.connect(**self.config_connection)
                conn.close()
                return True
            except:
                return False

        if self.manager_db == "postgresql":
            try:
                conn = psycopg2.connect(**self.config_connection)
                conn.close()
                return True
            except:
                return False

        if self.manager_db == "oracle":
            try:
                conn = cx_Oracle.connect(self.config_oracle)
                conn.close()
                return True
            except:
                return False

    # Consulta las bases de datos de un gestor
    def list_db(self):
        if self.manager_db == "mysql":
            if self.check_connection():
                conn = pymysql.connect(**self.config_connection)
                cursor = conn.cursor()
                query = "show databases"
                cursor.execute(query)
                data = [row[0] for row in cursor.fetchall()]
                conn.close()
                return data
            return None

        if self.manager_db == "postgresql":
            if self.check_connection():
                conn = psycopg2.connect(**self.config_connection)
                cursor = conn.cursor()
                """query2 = select d.datname,
                        (select string_agg(u.usename, ',' order by u.usename) 
                        from pg_user u 
                        where has_database_privilege(u.usename, d.datname, 'CONNECT')) as allowed_users
                        from pg_database d
                        order by d.datname"""
                query = (
                    "SELECT datname FROM pg_database PD,pg_user PU WHERE usename= '"
                    + self.config_connection["user"]
                    + "' AND PD.datdba=PU.usesysid order by 1"
                )
                cursor.execute(query)
                data = [row[0] for row in cursor.fetchall()]
                conn.close()
                return data
            return None

        if self.manager_db == "oracle":
            conn = cx_Oracle.connect(self.config_oracle)
            cursor = conn.cursor()
            query = "select APPLICATION_NAME from APEX_APPLICATIONS"
            cursor.execute(query)
            data = [row[0] for row in cursor.fetchall()]
            conn.close()
            return data
        return None

    # Ejecuta consultas para una conexion
    def managerSQL(self, query, input=None):
        if self.manager_db == "mysql":
            if self.check_connection():
                try:
                    conn = pymysql.connect(**self.config_connection)
                    cursor = conn.cursor(pymysql.cursors.DictCursor)
                    cursor.execute(query, input)
                    data = cursor.fetchone()
                    print(cursor._last_executed)
                    conn.close()
                    return data
                except Exception as e:
                    print(e)
                    return None

        if self.manager_db == "postgresql":
            try:
                conn = psycopg2.connect(**self.config_connection)
                cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                cursor.execute(query, input)
                data = cursor.fetchall()
                print(cursor.query)
                conn.close()
                return data
            except Exception as e:
                    print(e)
                    return None

        if self.manager_db == "oracle":
            pass

    def getColumns(self, query):
        if self.manager_db == "mysql":
            if self.check_connection():
                try:
                    conn = pymysql.connect(**self.config_connection)
                    cursor = conn.cursor()
                    cursor.execute(query)
                    columns = [column[0] for column in cursor.description]
                    conn.close()
                    return columns
                except:
                    return None

        if self.manager_db == "postgresql":
            try:
                conn = psycopg2.connect(**self.config_connection)
                cursor = conn.cursor()
                cursor.execute(query)
                columns = [column.name for column in cursor.description]
                conn.close()
                return columns
            except:
                return None

        if self.manager_db == "oracle":
            pass

    def get_type(self, type_code):
        conn = psycopg2.connect(**self.config_connection)
        cursor = conn.cursor()
        cursor.execute("select typname from pg_type where oid=" + type_code)
        cursor.close()
        return cursor.fetchall()

