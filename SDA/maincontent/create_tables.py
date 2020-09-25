import psycopg2
from sql_queries import create_table_queries, drop_table_queries

def create_database():
    
    #connect to default database
    try:
        conn.close()
    except:
        pass


    conn = psycopg2.connect("host=127.0.0.1 user=postgres password=846213579")
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    try:
        cur.execute("DROP DATABASE IF EXISTS smartdashboard") 
        cur.execute("CREATE DATABASE smartdashboard WITH ENCODING 'utf8' TEMPLATE template0")
    except psycopg2.Error as e:
        print("The database is already exists !")
        print(e)


    conn.close()

    conn = psycopg2.connect("host=127.0.0.1 dbname=smartdashboard user=postgres password=846213579")
    cur = conn.cursor()

    return cur, conn

def drop_tables(cur, conn):
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()

def create_tables(cur, conn):
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()

def main():
    try:
        conn.close()
    except:
        pass

    cur, conn = create_database()
    
    drop_tables(cur, conn)
    create_tables(cur, conn)

    cur.close();
    conn.close();
    print('Create Database Successfully')

if __name__ == "__main__":
    main()





