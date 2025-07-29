import pymysql
from pymysql.cursors import DictCursor 

# def get_db_connection():
#     return pymysql.connect(
#         host='localhost',
#         user='root',
#         password='root123',
#         database='hospital_db',
#         cursorclass=DictCursor
#     )


def get_db_connection():
    return pymysql.connect(
        host='hospitaldb.czccaimeyk2a.ap-south-1.rds.amazonaws.com',
        user='admin',
        password='admin12345678',
        database='hospital_db',
        cursorclass=DictCursor
    )

def get_hospital_name():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM settings WHERE name = 'hospital_name'")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result['value'] if result else "Default Hospital"
