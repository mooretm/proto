import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ Create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ Create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_project(conn, project):
    """ Insert new project into projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO projects(name, begin_date, end_date)
            VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()

    return cur.lastrowid


def create_task(conn, task):
    """ Create a new task
    :param conn:
    :param task:
    :return:
    """
    sql = ''' INSERT INTO tasks(name, priority, status_id, project_id, begin_date, end_date)
            VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()
    
    return cur.lastrowid


def update_task(conn, task):
    """ Update priority, begin_date, and end date of a task
    :param conn:
    :param task:
    :return: project id
    """
    sql = ''' UPDATE tasks
            SET priority = ? ,
                begin_date = ?,
                end_date = ?
            WHERE id = ? '''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()


def select_all_tasks(conn):
    """ Query all rows in the tasks table
        :param conn: the Connection object
        :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")

    rows = cur.fetchall()

    for row in rows:
        print(row)


def select_task_by_priority(conn, priority):
    """ Query tasks by priority
        :param conn: the Connection object
        :param priority:
        :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE priority=?", (priority,))

    rows = cur.fetchall()

    for row in rows:
        print(row)


def main():
    database = r"\\starfile\Public\Temp\MooreT\database\sqlite\test.db"

    # Create a database connection
    conn = create_connection(database)

    # Create tables
    # sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS projects (
    #                                     id integer PRIMARY KEY,
    #                                     name text NOT NULL,
    #                                     begin_date text,
    #                                     end_date text
    #                             );"""
    
    # sql_create_tasks_table = """ CREATE TABLE IF NOT EXISTS tasks (
    #                             id integer PRIMARY KEY,
    #                             name text NOT NULL,
    #                             priority integer,
    #                             status_id integer NOT NULL,
    #                             project_id integer NOT NULL,
    #                             begin_date text NOT NULL,
    #                             end_date text NOT NULL,
    #                             FOREIGN KEY (project_id) REFERENCES projects (id)
    #                         );"""

    # Enter data in tables
    # if conn is not None:
    #     with conn:
    #         # # Create projects table
    #         # create_table(conn, sql_create_projects_table)

    #         # # Create tasks table
    #         # create_table(conn, sql_create_tasks_table)

    #         # Create a new project
    #         project = ('Dynamic Edge Mode', '2022-04-25', '2023-06-01');
    #         project_id = create_project(conn, project)

    #         # Define tasks
    #         task_1 = ('Collect field data', 1, 1, project_id, '2023-04-05', '2023-04-28')
    #         task_2 = ('Collect lab data', 1, 1, project_id, '2023-05-01', '2023-05-15')

    #         # Create tasks
    #         create_task(conn, task_1)
    #         create_task(conn, task_2)
    # else:
    #     print("app: Error! Cannot create the database connection.")

    # Update data
    # with conn:
    #     update_task(conn, (2, '2023-05-07', '2023-05-20', 2))

    # Query data
    with conn:
        print("1. Query task by priority:")
        select_task_by_priority(conn, 1)

        print("2. Query all tasks")
        select_all_tasks(conn)


if __name__ == '__main__':
    main()
