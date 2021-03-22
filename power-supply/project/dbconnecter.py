import os
import sqlite3
import datetime
import os

def DB_Connection():
    db_filename = os.getenv("PWD") + '/out/supply-table-%03d.db' % datetime.datetime.today().timetuple().tm_yday
    schema_filename = os.getenv("PWD") + '/inp/supply-schema.sql'
    print(db_filename, schema_filename)
    db_exists = not os.path.exists(db_filename)

    with sqlite3.connect(db_filename) as conn:
        if db_exists:
            print('Creating schema')
            with open(schema_filename, 'rt') as file:
                schema = file.read()
            conn.executescript(schema)
        else:
            print('DB already exists.')
    return conn;

